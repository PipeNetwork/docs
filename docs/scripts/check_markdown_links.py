#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(".").resolve()
FILES = [Path("README.md")] + sorted(Path("docs").rglob("*.md"))
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")


def normalize_anchor(text: str) -> str:
    text = text.strip()
    text = re.sub(r"`", "", text)
    text = re.sub(r"\s+#*$", "", text).strip()
    text = text.lower()
    text = re.sub(r"[^a-z0-9 _-]", "", text)
    text = text.replace(" ", "-")
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def strip_code_fences(md: str) -> str:
    return re.sub(r"```.*?```", "", md, flags=re.DOTALL)


def build_anchor_set(md: str) -> set[str]:
    anchors: set[str] = set()
    seen_counts: dict[str, int] = {}
    for line in md.splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = normalize_anchor(m.group(1))
        if not base:
            continue
        count = seen_counts.get(base, 0)
        seen_counts[base] = count + 1
        anchor = base if count == 0 else f"{base}-{count}"
        anchors.add(anchor)
    return anchors


def parse_target(raw_target: str) -> tuple[str, str]:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    # Drop optional markdown title part: path "title"
    if " " in target and not target.startswith("http"):
        target = target.split(" ", 1)[0].strip()
    target = unquote(target)
    if "#" in target:
        path, anchor = target.split("#", 1)
        return path, anchor
    return target, ""


def is_external(target: str) -> bool:
    lower = target.lower()
    return lower.startswith(("http://", "https://", "mailto:", "tel:"))


def main() -> None:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}

    for rel_file in FILES:
        file_path = (ROOT / rel_file).resolve()
        if not file_path.exists():
            continue
        md_raw = file_path.read_text()
        md = strip_code_fences(md_raw)

        for m in LINK_RE.finditer(md):
            raw_target = m.group(1).strip()
            if is_external(raw_target):
                continue

            path_part, anchor = parse_target(raw_target)
            if not path_part and not anchor:
                continue

            if not path_part:
                target_file = file_path
            elif path_part.startswith("/"):
                target_file = (ROOT / path_part.lstrip("/")).resolve()
            else:
                target_file = (file_path.parent / path_part).resolve()

            if not target_file.exists() or not target_file.is_file():
                errors.append(
                    f"{rel_file}: missing target `{raw_target}` resolved to `{target_file.relative_to(ROOT) if target_file.exists() else target_file}`"
                )
                continue

            if anchor:
                if target_file not in anchor_cache:
                    anchor_cache[target_file] = build_anchor_set(target_file.read_text())
                normalized = normalize_anchor(anchor)
                if normalized not in anchor_cache[target_file]:
                    errors.append(
                        f"{rel_file}: missing anchor `#{anchor}` in `{target_file.relative_to(ROOT)}`"
                    )

    if errors:
        print("markdown-link-check-failed")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("markdown-link-check-passed")


if __name__ == "__main__":
    main()
