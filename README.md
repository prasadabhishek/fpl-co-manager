# FPL Co-Manager

Agent skill and Python 3 stdlib math CLI for Fantasy Premier League: 21-Rule Mathematical Selection Engine, Shin's bookmaker devigging, xP/£m ROI optimization, and adversarial transfer auditing.

## Install as an Agent Skill

```bash
npx skills add prasadabhishek/fpl-co-manager
```

## Standalone CLI Usage

```bash
# Devig two-way bookmaker decimal odds using Shin's method
uv run scripts/fpl_math.py shin --odds 2.40 1.62 --output /tmp/shin.json

# Compute Rule 6 ROI & Rule 9 sub-60' hook decay
uv run scripts/fpl_math.py roi --xp 5.8 --cost 7.5 --hook-risk high --output /tmp/roi.json
```

## License

MIT
