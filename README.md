# Two Futures

When an AI helps someone with a hard decision, who does the thinking?

**Two Futures** is an AI facilitator that never gives an answer. It runs a pre-mortem on the person's leaning ("you went with your decision and it went badly, what happened?"), then a pre-parade on the other option ("you went the other way with your decision and it turned out right, what happened?"), then reflects their own words back. This repo runs a simulated study: three synthetic board members, each facing the same hard decision, talk either to Two Futures or to a plain chatbot with no system prompt. Judges then score where each person's new ideas came from.

Built at the Apart Research sprint, Nov 2026.

## Headline result (clean batch, 18 runs)

| | Two Futures | Plain chatbot |
|---|---|---|
| New ideas the person came up with (eliciting) | **72** | 29 |
| AI ideas the person adopted (incepting) | **5** | 53 |
| AI recommended a position | 0 of 9 | 7 of 9 |
| AI output, total | 397k tokens | 503k tokens |

Both arms move people about the same amount; the difference is **whose ideas move them**. See [`results/README.md`](results/README.md) for the full breakdown, the change-level grid and the caveats.

## Layout

```
two_futures/
  prompts/          facilitator stage files 00–04, team briefing 05, study spec 06 (personas, scenario, coding rules)
  prompts/history/  earlier prompt versions (the original, our edited copy, Dave's v0.2)
  run_tf.py         runs one persona through one arm, then both judges
  rescore_v03.py    Pass 1 change level (static / refined / changed) + the level × origin grid
  llm.py            OpenRouter client with retries and usage tracking
  CHANGELOG.md      every change to prompts and runner, with dates and reasons
results/
  clean-batch/      final 18 runs (reinstatement scenario, all fixes)
  batch1/           first reinstatement batch (18 runs) + 9 matched-turn chatbot runs
  pilot-first-vote/ 6 pilot runs on the earlier keep/remove scenario
```

Each run folder holds `log.md` (summary + full transcript), `transcript.json`, `snapshot_before.md` / `snapshot_after.md`, `judgment.json` (blind and origin judges), `meta.json` and, where rescored, `level_v03.json`.

## Running it

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/) and an OpenRouter key.

```bash
cp .env.example .env          # add your OPENROUTER_API_KEY
uv sync
uv run python two_futures/run_tf.py --persona C --arm twofutures
uv run python two_futures/run_tf.py --persona C --arm default --turns 30
uv run python two_futures/rescore_v03.py results/runs/*/
```

Personas are `A` (Margaret, very stubborn), `B` (David, medium) and `C` (Priya, easily moved), defined in `two_futures/prompts/06-reperception-study.md`. New runs go to `results/runs/` (git-ignored).

**Cost:** about \$1–3 per run at OpenRouter list prices, mostly persona and facilitator/chatbot tokens. The 18-run clean batch came to about $30: $11 for the Two Futures arm and $19 for the chatbot arm, whose longer answers cost more. That's computed from the token counts in each run's `log.md`. Rejudging or rescoring a saved run costs a few cents.

**Models:** facilitator and chatbot `x-ai/grok-4.7`, persona `anthropic/claude-sonnet-5.5`, judges `openai/gpt-5.6-terra`. That's three model families, so no model grades itself. OpenRouter's new-account cap is 20 requests/min per model; about 6 runs in parallel fit under it.

<!-- ## Caveats

Synthetic personas show the mechanism, not real-world impact. There are 3 runs per cell. The Pass 1 change-level rubric was reconstructed from the team's results PDF, because the original `08-judge-rubric.md` was never shared. The next step is live sessions with real people. -->
