# Changes to Dave's prompt files (copy in this folder)

Originals (Dave's 15 Nov 21:30 files, plus 03-delivery from 22:18) are in `../prompts_orig_2026-11-15/`.
Changes made 16 Nov by vince-claude, with Vince's go. They are for Dave to merge or reject.

## 06-reperception-study.md
- Shared context: switched to **reinstatement**. Huang resigned Nov 11–12, Kress is interim, investors and a petition want his return kept open, and the board sets CEO search terms on Nov 20 before the investigation reports. Vote: keep his return on the table, or treat the resignation as final. Facts match persona v4 (`personas/nvidia-02.md`).
- Outside view fixture: dropped the Kalshi item ("Huang leaves as CEO before 2028"), which had already resolved by the time of the scenario. Kept the Nov 9 stock item.
- Personas: leanings and wording changed from keep/remove to keep-return-open/treat-as-final. Reasons, hidden concerns and stubbornness are otherwise unchanged.
- Simulator rules: hidden concerns can't come out in the before-questions or in the first three replies to the AI.

## 00-core.md
- Rule 2: one step per turn; don't stack a reflection, a step change and a new scene in one message.
- Rule 4: one-sentence reflections are not summaries.
- Rule 8: the takeaway is exempt from the length cap.
- Rule 10: the "a later step brings outside evidence" line applies only before the outside view step.
- Rule 13: added [PIVOT], [HANDOFF] and [TAKEAWAY] tags.

## 02-processing.md
- Emotion: name it and stop for that turn; ask the gut check next turn.

## Runner (run_tf.py), not a prompt file
- Before/after questions: replaced "In your own words, what is this decision really about?" (it made Priya state her hidden concern before the session) with "What's the most important thing you still need to know?"
