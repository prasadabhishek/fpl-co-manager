#!/usr/bin/env python3
"""FPL mathematical utilities: Shin's devigging method and xP/ROI calculator (stdlib only)."""

import argparse
import json
import math
import sys
from pathlib import Path


def cmd_shin(d1: float, d2: float, output: Path) -> None:
    if d1 <= 1.0 or d2 <= 1.0:
        print("Error: decimal odds must be > 1.0", file=sys.stderr)
        sys.exit(1)
    pi1 = 1.0 / d1
    pi2 = 1.0 / d2
    overround = pi1 + pi2
    denom = overround - (pi1 ** 2 + pi2 ** 2)
    z = (1.0 - (pi1 ** 2 + pi2 ** 2)) / denom if denom > 0 else 0.0
    p1 = (1.0 - z) * (pi1 ** 2) + z * pi1
    p2 = (1.0 - z) * (pi2 ** 2) + z * pi2
    norm = p1 + p2
    p1, p2 = p1 / norm, p2 / norm
    lam = -math.log(max(1e-9, 1.0 - p1))

    report = {
        "decimal_odds": [d1, d2],
        "raw_implied_probs": [round(pi1, 4), round(pi2, 4)],
        "overround_pct": round((overround - 1.0) * 100.0, 2),
        "shin_z": round(z, 6),
        "true_probs": [round(p1, 4), round(p2, 4)],
        "poisson_lambda_outcome1": round(lam, 4),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2))
    print(f"Success! Shin devig: P1={report['true_probs'][0]} (lambda={report['poisson_lambda_outcome1']}), P2={report['true_probs'][1]} -> {output}")


def cmd_roi(xp: float, cost: float, hook_risk: str, output: Path) -> None:
    if cost <= 0:
        print("Error: cost must be > 0", file=sys.stderr)
        sys.exit(1)
    decay = 0.85 if hook_risk == "high" else 1.0
    adj_xp = xp * decay
    roi = adj_xp / cost
    report = {
        "raw_xp": xp,
        "cost_m": cost,
        "hook_risk": hook_risk,
        "decay_multiplier": decay,
        "adjusted_xp": round(adj_xp, 3),
        "roi_xp_per_m": round(roi, 3),
        "passes_rule6_threshold_0_50": roi >= 0.50,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2))
    print(f"Success! Adjusted xP={report['adjusted_xp']}, ROI={report['roi_xp_per_m']} xP/£m (passes={report['passes_rule6_threshold_0_50']}) -> {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="FPL Co-Manager Math CLI (Shin Devigging & ROI)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_s = sub.add_parser("shin", help="Devig two-way decimal odds using Shin's method")
    p_s.add_argument("--odds", required=True, nargs=2, type=float)
    p_s.add_argument("--output", required=True, type=Path)

    p_r = sub.add_parser("roi", help="Compute xP/£m ROI with Rule 9 hook-risk decay")
    p_r.add_argument("--xp", required=True, type=float)
    p_r.add_argument("--cost", required=True, type=float)
    p_r.add_argument("--hook-risk", choices=["low", "high"], default="low")
    p_r.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "shin":
        cmd_shin(args.odds[0], args.odds[1], args.output)
    elif args.command == "roi":
        cmd_roi(args.xp, args.cost, args.hook_risk, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
