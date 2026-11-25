---
name: fpl-co-manager
description: >-
  Fantasy Premier League (FPL) Co-Manager skill powered by a 21-Rule
  Mathematical Selection Engine, Shin's devigged sharp bookmaker odds,
  expected points (xP) ROI optimization, and adversarial consensus auditing.
  Use when building FPL squads, evaluating transfers, choosing captains, or
  devigging match odds to expected points.
---

# FPL Co-Manager — 21-Rule Mathematical Selection Engine

## Overview

Data-driven Fantasy Premier League (FPL) squad builder and transfer auditor. Converts sharp bookmaker odds into true implied probabilities via **Shin's devigging method**, enforces 21 hard mathematical squad-construction rules, and eliminates hype/covariance traps.

## Quick Start

```bash
# Devig two-way bookmaker decimal odds (e.g. Clean Sheet Yes/No) using Shin's method
uv run scripts/fpl_math.py shin --odds 2.40 1.62 --output /tmp/shin.json

# Compute player xP ROI efficiency and sub-60 minute decay penalty
uv run scripts/fpl_math.py roi --xp 5.8 --cost 7.5 --hook-risk high --output /tmp/roi.json
```

## Utility Scripts

`scripts/fpl_math.py` uses Python 3 standard library only (`math`, `json`, `argparse`).

- **`shin --odds <d1> <d2> --output <path.json>`**: Computes Shin's insider-trading parameter $z$, true devigged probabilities $P_1, P_2$, bookmaker overround, and Poisson goal intensity $\lambda = -\ln(1 - P_1)$.
- **`roi --xp <expected_points> --cost <price_m> --hook-risk <low|high> --output <path.json>`**: Applies the Rule 9 sub-60' minute decay multiplier ($\lambda = 0.85$ for high hook-risk full-backs/wingers) and checks the Rule 6 $\ge 0.50\text{ xP/£m/GW}$ efficiency threshold.

---

## Core 21-Rule Mathematical Selection Engine

Every candidate squad and transfer recommendation MUST satisfy these 21 rules:

1. **Automated Health Hard-Filter:** `status === 'a'` AND `chance_of_playing_next_round === 100` (or `null`). Zero tolerance for injured/flagged players.
2. **90-Minute Starter & Minutes Floor:** Minimum 1,500+ minutes in prior PL season or 90%+ start rate.
3. **Goalkeeper Dual-Starter Hard Filter:** Both `GKP1` and `GKP2` must be nailed PL starters (zero backup GKPs).
4. **Team Concentration & Covariance Cap:** Max 1 player from any mid-table club; max 2 from any top-tier club to avoid single match-script covariance traps.
5. **Active Bench Playing Floor:** All 4 bench slots (`GKP2`, `DEF3`, `DEF4`, `MID5`) must be active starters with reliable 2-point floors.
6. **Marginal xP Efficiency per £1m:** $\text{ROI} = \frac{xP_{\text{GW}}}{\text{Cost}} \ge 0.50\text{ xP/£m/GW}$.
7. **Sharp Bookmaker Devigging (Shin's Method):** Convert Pinnacle/Betfair implied probabilities using Shin's Method directly to $xP$ and $\lambda_{\text{goal}} = -\ln(1 - P(\text{AGS}))$.
8. **CBIT Floor vs Attacking Ceiling:** Defenders must provide either strong Clearances/Blocks/Interceptions/Tackles floor ($\ge 3.5/\text{match}$) OR attacking return ceiling ($xGI/90 \ge 0.25$).
9. **Sub-60' Hook & Minute Decay Penalty:** Apply $\lambda = 0.85$ to players with high early-substitution risk.
10. **Creator Consensus Bias Neutralization:** Require underlying Opta xG/xA validation before backing hyped content-creator picks.
11. **5-FT Rolling Shadow Value vs Hit Math:** Hold Free Transfers early; enforce a $+1.33\text{ xP/GW}$ hurdle rate for `-4` hits.
12. **Price Change Velocity & Price Lock Protection:** Track daily transfer velocity and Red-to-Unflagged 8-day price lock windows (`192h`).
13. **SGW Super-Fixture vs DGW Hurdle:** Captain elite SGW talismans over DGW volume assets whenever $xGI_{\text{SGW}} \ge 1.30$.
14. **Dynamic Formation Matrix:** Evaluate all 8 legal FPL formations (`3-5-2`, `3-4-3`, `4-4-2`, `4-3-3`, `4-5-1`, `5-3-2`, `5-4-1`, `5-2-3`) to maximize expected points.
15. **Opponent High-Line & Transition xG Exploitation:** Boost expected points multiplier for runners facing high-line / high-xGA defenses.
16. **Set-Piece & Penalty Monopoly Enforcement:** Prioritize 100% penalty and direct set-piece takers.
17. **International Break Flag Shield:** Verify travel fatigue and flag resets during international breaks before executing transfers.
18. **Effective Ownership (EO) Rank Shielding:** Respect `70%+` EO captaincy assets to avoid catastrophic rank tail-risk.
19. **Automated Lineup & Bench Priority Ordering:** Sort starters and bench by $xP$ (`Slot 12: GKP2 > Slot 13 > Slot 14 > Slot 15`) with 3-DEF structural lockout guard.
20. **Pre-Deadline T-4h Line Steam Gate:** Verify final odds movements and late team leaks 2–4 hours before deadline.
21. **Adversarial Consensus Audit:** Stress-test every transfer by comparing marginal return ($\Delta xP / \Delta £$) against template rank-protection risk before confirming.

---

## Optional Browser Execution SOP (via `chrome-devtools`)

If the user explicitly asks to execute transfers in their logged-in FPL browser tab, use `POST /api/transfers/` or `POST /api/my-team/<TEAM_ID>/` with the active `X-CSRFToken` header—and **always confirm the exact transfer list with the user before submitting**.
