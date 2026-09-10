#!/usr/bin/env python3
"""Reject obsolete network instructions and known contradictory policy claims."""

import re
import sys
from pathlib import Path


PATTERNS = {
    "obsolete network instructions": r"\b(?:devnet\d*|testnet)\b",
    "obsolete account API": r"\buser_app_key\b|/(?:createUser|rotateAppKey|checkBalance)\b",
    "obsolete node binary command": r"\./pop\b",
    "retired payout parameters": r"\b(?:CDN_RATE_USD_PER_TB|STORAGE_RATE_USD_PER_TB_MONTH|STAKING_COMMISSION_BPS|E_cap_month|net_pipe_i|gross_pipe_i)\b",
    "incorrect PIPE minimum": r"(?<![\d,])(?:100|1[,_]?000)\s+(?:underlying\s+)?PIPE\b",
    "unconfirmed burn percentage": r"\b93\s*%",
    "incorrect fixed withdrawal period": r"\b(?:is|has|uses)\s+(?:a\s+)?(?:fixed\s+)?30[- ]day\s+(?:cooldown|lock)\b",
    "retired reward program": r"scarcity-based reward|location-based rewards|referral rewards",
}

RETIRED = (
    "docs/nodes/devnet-2.md", "docs/nodes/devnet-2/troubleshooting.md",
    "docs/nodes/testnet.md", "docs/appendix/old-guardian-node.md",
    "docs/appendix/solana-snapshots.md", "docs/cdn-api/api-documentation.md",
    "docs/pipe-firestarter-storage.md", "docs/mica.pdf",
    "docs/internal/tokenomics-internal-ops.md", "docs/test-vectors",
    "docs/scripts/run_tokenomics_test_vectors.py",
)


def check_text(content: str) -> list[str]:
    return [label for label, pattern in PATTERNS.items() if re.search(pattern, content, re.I)]


def main() -> None:
    # Empty, untracked directories are harmless; old published files are not.
    errors = [f"Remove retired artifact: {path}" for path in RETIRED
              if Path(path).is_file() or (Path(path).is_dir() and any(Path(path).rglob('*.*')))]
    for path in [Path("README.md"), *sorted(Path("docs").rglob("*.md"))]:
        if Path("docs/archive") in path.parents:
            continue
        for label in check_text(path.read_text()):
            errors.append(f"{path}: {label}")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("mainnet-content-check-passed")


if __name__ == "__main__":
    main()
