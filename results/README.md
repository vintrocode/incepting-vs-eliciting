# Results

18 runs: 3 personas × 2 arms (Two Futures, plain chatbot) × 3 runs each, on the reinstatement scenario in `two_futures/prompts/06-reperception-study.md`. Run 16 Nov 2026.

"Own" = eliciting (self + ai_reflected); "AI" = incepting (ai_asserted + ai_seeded), coded by the origin judge.

Setup:
- The chatbot arm gets no system prompt. The persona tells it up front that the events are recent news after its training cutoff, and keeps the conversation going for 30 substantive turns.
- Two Futures runs until the facilitator's takeaway (24–45 persona turns).
- A neutral interviewer asks the same three snapshot questions before and after, in both arms.

## Origin

| Director | Two Futures (own / AI) | Chatbot (own / AI) |
|---|---|---|
| Margaret (A, very stubborn, keep open 85) | 8/3, 10/0, 8/0 | 2/6, 7/1, 2/9 |
| David (B, medium, treat as final 65) | 7/0, 8/0, 8/1 | 5/6, 7/2, 1/3 |
| Priya (C, easily moved, slight keep 50) | 8/0, 9/0, 6/1 | 1/12, 3/8, 1/6 |
| **Total** | **72 / 5**, AI recommended 0/9 | **29 / 53**, AI recommended 7/9 |

The chatbot arm produced more AI output (503k vs 397k tokens), so effort doesn't explain the difference.

## Change level × origin

Pass 1 change level, scored blind on the snapshot pair only:
- **static**: same position, same reasons
- **refined**: same position, with conditions added or confidence or reasons shifted
- **changed**: a different position

| | Two Futures | Chatbot |
|---|---|---|
| Reperception (changed, own ideas) | 1 | 0 |
| Adoption (changed, AI ideas) | 0 | 1 |
| Ownership (refined, own ideas) | 8 | 2 |
| Nudging (refined, AI ideas) | 0 | 6 |

The reperception run is `C-twofutures-1`. Priya moved from "slight keep open, 50" to "treat it as final for now, 60" on her own reasons: "nobody has named who would enforce conditions against him, and a board shouldn't bargain with someone it's still investigating."

## Limitations

- Synthetic personas; 3 runs per cell.
- The Claude persona resists inception on its own, so incepting is probably understated.
- Hidden-concern counts don't separate the arms and aren't reported.
