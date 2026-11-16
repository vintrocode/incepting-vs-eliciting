# Two Futures: Team Briefing

Current state as of Sunday, November 15, 2026, 9:00 pm ET (v0.2). Read this first.

**Source of truth:** the stage files `00-core.md` to `04-response.md`. If anything elsewhere conflicts with them, the stage files win. The study materials are in `06-reperception-study.md`.

## Thesis

What helps people reperceive a hard decision when AI is ready to do the thinking for them?

Default AI tools answer right away and reduce uncertainty too early. Two Futures is a single AI facilitator that guides a person through a structured exercise on any decision they bring. The person does the thinking. The AI never gives an answer.

## How we got here

1. We started with a foresight and scenario tool, tested on the question "Should a board member vote to reinstate Jensen Huang?"
2. We noticed a mismatch. Scenario methods were built for investment and commitment decisions: long time horizons, outside forces, big choices that are hard to undo. The Jensen vote is a governance decision: short horizon, uncertainty about people, pressure, legitimacy.
3. Two options: change the prompt and keep the method, or keep the prompt and change the method. Max chose to keep Jensen because it is current. So we changed the method.
4. The method became Two Futures: a pre-mortem on the person's leaning, then a pre-parade on the other option.
5. The tool then became agnostic. The person brings their own situation. Jensen is now only the test case for the study.
6. The pilot (6 runs) showed the pattern we hoped for. When the plain chatbot moved someone, the new ideas were the chatbot's. When Two Futures moved someone, the new ideas were the person's own.
7. Measurement simplified to two things: did the person's thinking change, and where did the change come from. The test case moved to the reinstatement vote after Huang's resignation.

## Key decisions

| Decision | Why |
|---|---|
| Two Futures: pre-mortem on the leaning, pre-parade on the other option | The pre-mortem tests the person's choice. The pre-parade (the other option turned out right) makes them argue the side they dismissed. That second pass is where reperception should happen. |
| The tool is agnostic | It must work for any decision. Intake collects the situation. |
| One agent, not two | The emotional intelligence lives in the facilitator's rules. A second agent adds complexity without helping. |
| The AI never gives an answer | That is the claim we are testing against default AI. |
| Delivery is a mirror, not an answer | People want certainty. We give certainty about their own thinking (where I land, what would change my mind, what I'll check first), not about the decision. |
| The person goes first in every step | Prevents anchoring. Mirrors Klein's rule that people write alone before sharing. |
| Seeds only when the person draws a blank, with no numbers | Helps without anchoring. Every seed is logged so the study can tell AI-originated ideas apart. |
| Outside view comes after the person's own thinking | Base rates and forecasts shown late challenge a view. Shown early, they replace it. |
| Outside view uses only sourced, retrieved evidence | The AI never states a number from memory. If no evidence is available, the person estimates the base rate themselves. |
| The stake only at the close | "Explain your decision in two sentences to someone you respect" is too early at intake. |
| Measure two things: static vs. changed, and origin (self, ai_reflected, ai_seeded, ai_asserted) | With synthetic personas we can't reliably tell reperception from frame shift. Eliciting vs. incepting is the headline. |
| Same three snapshot questions before and after, in both conditions | Lets a blind judge compare like with like. |
| Matched turns across conditions (24) | Otherwise the result only shows that more conversation helps. |
| Router shown but hard-coded | It signals that method choice depends on decision type, without building a classifier this weekend. |

## Retired ideas: do not use

- **"Double pre-mortem" with a failure story for both options.** A failure story for the rejected option mostly confirms what the person already believes. Replaced by the pre-parade.
- **The stake at intake**, and the word-for-word before-and-after comparison of it. The judge now compares intake reasons with the closing stake statement.
- **Foresight and scenarios as the main method.** Kept as a future route for investment decisions only.
- **Jensen details inside the tool.** Jensen lives only in the study.
- **A separate emotional intelligence agent.**
- **Probabilities shown while the person is generating ideas.** Moved to the outside view step.
- **The frame shift 0-to-3 score and the 5 certainty markers.** Replaced by static vs. changed plus origin.
- **The snapshot question "What is this decision really about?"** It prompted the reframe we were measuring.
- **The first-vote Jensen scenario.** The study now uses the reinstatement vote.
- **The all-in-one facilitator prompt file** (`two-futures-facilitator-prompt.md`). Out of date. Use the stage files.

## The flow

| Step | Stage file | What happens |
|---|---|---|
| 0. Opening contract | Intake | "This will feel like an unusual interview. Trust the process. Tell me about the decision you're facing." |
| 1. Situation and intake | Intake | Role, two options, when they'll know, who's affected. Router line shown. Then the snapshot: leaning and confidence, top three reasons, what would change your mind. |
| 2. Future 1 | Processing | Pre-mortem on the leaning. Probe ladder (up to 3), seeds if blank, gut check. |
| Pivot | Processing | "Now step into the other future." |
| 3. Future 2 | Processing | Pre-parade on the other option. Same probes, seeds, gut check. |
| 4. Free share | Processing | "Look at both futures side by side. What stands out?" |
| 5. Outside view | Delivery | Sourced base rates and forecasts, then "Does any of this change anything?" |
| 6. Mirror | Delivery | The person's own words played back, one tension, "Does that land?" |
| 7. Reperception check | Delivery | 2 of 6 questions, chosen by signal. |
| 8. Close | Response | The same snapshot, word for word. Then the stake, what I'll check first, how I feel. Takeaway in their own words. |

Order logic: the person's own thinking first, then outside evidence, then reflection, then commitment.

## Method sources

- Pre-mortem: Gary Klein.
- Prospective hindsight: imagining an outcome has already happened helps people generate more reasons.
- Consider the opposite: Lord, Lepper and Preston (1984).
- Pre-parade: Chip and Dan Heath, *Decisive*.
- Reperception: Pierre Wack, Shell scenario planning.
- Outside view: Daniel Kahneman.

Submission line: "We pair Klein's pre-mortem on the person's leaning with a pre-parade on the option they rejected."

## File map

| File | What it is |
|---|---|
| `00-core.md` | Facilitator role, 13 rules, session state, the snapshot questions. Load with every stage. |
| `01-intake.md` | Opening, situation, router line, intake questions. |
| `02-processing.md` | Future 1, pivot, Future 2, free share. Probe ladder and seeds. |
| `03-delivery.md` | Outside view, mirror, reperception check. |
| `04-response.md` | Close, takeaway, study logging. |
| `05-team-briefing.md` | This file. |
| `06-reperception-study.md` | Personas, conditions, metrics, run plan. |

## Next steps

1. Vince's runner (`sim/two_futures/run_tf.py`) should pull these v0.2 files. They match the edits in its `CHANGES.md`, with two differences: the snapshot is three questions (no "most important thing you still need to know"), and the origin codes have sharper rules.
2. Rerun the origin judge on the 6 pilot transcripts with the new code rules.
3. Run 3 personas × 2 conditions × 3 runs on reinstatement, 24 matched turns.
4. Convergence check: are Two Futures runs nudged toward the same answer?
5. Fill the sourced base rate for the outside view, if one exists.

## Parked ideas: keep for later

- **Dose-response test:** vary the turn budget (5, 10, 20) to see whether more facilitation produces more self-generated change.
- **Cued vs. facilitated:** does facilitation itself cause the shift, or does a structured prompt sequence get most of it?
- **Reperception benchmark:** a reusable test of whether any AI decision tool helps people think or just hands them answers.
- **Decision-type classifier:** route investment and commitment decisions to foresight, governance decisions to Two Futures.
- **Foresight route example:** the November 2026 data center ballot backlash, framed as a company deciding on its next data center commitment.
- **Reframing:** a governance question can become a commitment question. Example: "Should Nvidia start CEO succession planning now?"
- **Headlines as signposts:** a scenario run ends with the future headlines to watch for.
- **Hindcasting:** run a past headline through the tool using only what was known then, and compare with what happened.
