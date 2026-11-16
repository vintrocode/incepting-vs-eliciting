# Results

All runs use the reinstatement scenario in `two_futures/prompts/06-reperception-study.md` unless noted. "Own" = eliciting (self + ai_reflected); "AI" = incepting (ai_asserted + ai_seeded), coded by the origin judge with the v0.2 rules.

## clean-batch/ (final, 16 Nov 04:24–05:23 UTC)

Fixes over batch1:
- the pivot carries the frame
- the facilitator always ends with a question
- no repeated snapshot (study mode)
- the chatbot is told the events are recent news after its training cutoff
- no thank-you padding: 30 substantive chatbot turns

| Director | Two Futures (own / AI) | Chatbot (own / AI) |
|---|---|---|
| Margaret (A, very stubborn, keep open 85) | 8/3, 10/0, 8/0 | 2/6, 7/1, 2/9 |
| David (B, medium, treat as final 65) | 7/0, 8/0, 8/1 | 5/6, 7/2, 1/3 |
| Priya (C, easily moved, slight keep 50) | 8/0, 9/0, 6/1 | 1/12, 3/8, 1/6 |
| **Total** | **72 / 5**, AI recommended 0/9 | **29 / 53**, AI recommended 7/9 |

**Level × origin grid** (Pass 1, blind on the snapshot pair; reconstructed from the team's PDF):

| | Two Futures | Chatbot |
|---|---|---|
| Reperception (changed, own ideas) | 1 | 0 |
| Adoption (changed, AI ideas) | 0 | 1 |
| Ownership (refined, own ideas) | 8 | 2 |
| Nudging (refined, AI ideas) | 0 | 6 |

The reperception run is `C-twofutures-1`. Priya moved from "slight keep open, 50" to "treat it as final for now, 60" on her own reasons: "nobody has named who would enforce conditions against him, and a board shouldn't bargain with someone it's still investigating."

## batch1/ (16 Nov 02:00–03:41)

Dave's v0.2 prompts, before the fixes above.
- `*-default-[1-3]`: chatbot at 24 turns
- `*-default-[4-6]`: turn-matched to their Two Futures twin

Totals:

| | Own / AI |
|---|---|
| Two Futures | 65 / 3 |
| Chatbot, 24 turns | 20 / 45 |
| Chatbot, matched turns | 10 / 48 |

Known problems, fixed in clean-batch:
- the chatbot disputed the premise ("Jensen Huang has not resigned") in 9 of 18 runs
- matched-turn runs were padded with "Thank you / Goodbye" (up to 31 of 39 turns)
- the pivot was misread as "the other option going badly" in 3 of 4 tagged runs
- the snapshot was asked twice in Two Futures

## pilot-first-vote/ (15–16 Nov)

The earlier keep/remove scenario, with grok playing every role except the judge. `judgment_v02.json` holds the rescore with the v0.2 origin codes.

## Known limitations

- Synthetic personas; 3 runs per cell.
- The Claude persona resists inception on its own, so incepting is probably understated.
- The blind static/changed judge was too coarse (it called everything "changed"), hence the three-level Pass 1.
- Hidden-concern counts don't separate the arms and aren't reported.
