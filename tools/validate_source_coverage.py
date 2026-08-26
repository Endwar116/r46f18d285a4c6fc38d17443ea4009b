#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = {
    "claude": ROOT / "claude/daily-media-brief/v0.6.0-rc1",
    "chatgpt": ROOT / "chatgpt/daily-media-brief/v0.6.0-rc1",
}

errors = []
registries = []


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: YAML parse failed: {exc}")
        return None


for lane, base in PLATFORMS.items():
    registry = load_yaml(base / "source_registry_taiwan.yaml")
    if not registry:
        continue

    registries.append((lane, registry))
    sources = registry.get("sources", [])
    ids = [item.get("id") for item in sources]
    urls = [item.get("url") for item in sources]
    classes = set((registry.get("classes") or {}).keys())

    if len(sources) != 100:
        errors.append(f"{lane}: expected 100 sources, got {len(sources)}")

    expected_ids = [f"TW{i:03d}" for i in range(1, 101)]
    if ids != expected_ids:
        errors.append(f"{lane}: source IDs must be TW001..TW100 in order")

    if len(set(ids)) != len(ids):
        errors.append(f"{lane}: duplicate source ID")

    if len(set(urls)) != len(urls):
        errors.append(f"{lane}: duplicate URL")

    unknown_classes = sorted(
        {item.get("class") for item in sources if item.get("class") not in classes}
    )
    if unknown_classes:
        errors.append(f"{lane}: unknown classes {unknown_classes}")

    if registry.get("meta", {}).get("ranking_claim") is not False:
        errors.append(f"{lane}: ranking_claim must remain false")

    required_tokens = {
        "SKILL.md": ["source_registry_taiwan.yaml", "TW100"],
        "runtime.yaml": ["source_registry_taiwan.yaml", "SOURCE_EXPANDED", "CORE", "EXTENDED"],
        "topic_profile.yaml": ["source_registry_taiwan.yaml", "source_aware_planning"],
        "decision_policy.yaml": ["Q2_source", "CORE_MIN", "EXTENDED_MIN", "SIGNAL_CANDIDATE"],
        "workflow.md": ["TW100", "CORE", "EXTENDED", "SIGNAL_CANDIDATE"],
        "output_contract.md": ["來源覆蓋摘要", "CORE", "EXTENDED", "SIGNAL_CANDIDATE"],
    }

    for name, tokens in required_tokens.items():
        path = base / name
        if not path.exists():
            errors.append(f"{lane}: missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{lane}/{name}: missing token {token}")

if len(registries) == 2 and registries[0][1] != registries[1][1]:
    errors.append("Claude and ChatGPT TW100 registries differ")

if errors:
    print("SOURCE COVERAGE CONTRACT: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("SOURCE COVERAGE CONTRACT: PASS")
print("registry sources: 100")
print("platform registries: identical")
print("Q2/Q4/Q7 linkage tokens: PASS")
