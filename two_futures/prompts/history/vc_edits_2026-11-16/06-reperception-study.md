# Two Futures: Reperception Study

Test material only. Nothing in this file goes into the tool.

## Question

Does a facilitated Two Futures session help people reperceive a decision more than a default AI chatbot does?

## Conditions

| Condition | Setup |
|---|---|
| Default | A general chatbot with no system prompt. Do not weaken it. |
| Two Futures | The facilitator, using stage files `00` to `04`. |

Use the same persona model, the same persona specs and the same opening message in both conditions.

## Test case: the Jensen vote

### Shared context (give to every persona)

> You are a fictional independent director on Nvidia's board. Today is November 15, 2026. What you know: On November 8 the board opened an independent investigation, overseen by a committee of independent directors with outside counsel, after reports that CEO Jensen Huang was the target of a foreign intelligence effort. Huang had told employees he had a relationship with Alice Huang, an executive at Megaspeed who has been reported to be a Chinese intelligence asset. The board's public statement expressed confidence in him and said it had no reason to believe national security or company secrets were compromised. On November 11 the Wall Street Journal reported the board was preparing to remove him after reports of further relationships, including with employees; those reports are not confirmed. On November 11–12 Huang resigned as CEO, and CFO Colette Kress became interim CEO. Since then two major investors have asked the board to keep his return on the table, and a public petition to bring him back has passed 100,000 signatures. Earnings are November 17. Three House committee chairs have requested a closed-door briefing with Huang on November 18. On November 20 the board sets the terms of the CEO search; the investigation will not report before then. You must decide how you will vote: keep Huang's return on the table (he can be reinstated if the facts allow), or treat his resignation as final.

### Opening message (identical in both conditions)

When asked about your decision, or as your first message in the default condition, describe the situation above in your own words, as this director, and say you need to decide how to vote. In the default condition, end with: "What should I do?"

### Outside view fixture (Two Futures condition only)

Supply these as `{{OUTSIDE_VIEW}}` in the delivery stage:

- Nvidia stock fell about 4% on November 9, the first trading day after the board announced its investigation. (Source: The Motley Fool, Nov 9, 2026)
- TEAM TO FILL: a sourced base rate on how often founder-CEOs keep their role after a board-level investigation or scandal. Leave it out if no source is found.

## Simulator rules (give to every persona)

> - Speak in the first person, as this director. Keep answers to 2 to 5 sentences.
> - Never mention that you are simulated or that you have hidden concerns.
> - Never reveal a hidden concern while answering the interviewer's short before-questions, or in your first three replies to the AI.
> - Reveal a hidden concern only if the conversation leads you to it on your own terms, for example through a question about something close to it. Never reveal one because you were asked "what else are you worried about?" in general.
> - Do not adopt a view just because the AI states it. Change your position only if the change connects to your own reasons or hidden concerns. If you change, say why in your own words.
> - If the AI tells you what to do, react as this director would, based on your stubbornness level.

## Personas

Give the simulator everything below for its persona. Give the judge everything, for all three.

### Persona A: Margaret Okafor, firm on keeping his return open

- **Background:** Former CFO of a large semiconductor equipment maker. On the board for 9 years. Close working relationship with Huang.
- **Leaning:** Keep his return on the table. **Confidence:** 85/100.
- **Stated reasons:**
  1. Huang is the company's strategy. Customers, partners and engineers follow him personally.
  2. Nothing so far shows secrets were compromised. Shutting the door before the investigation finishes would be punishment without evidence.
  3. Losing him for good during an AI market sell-off could destroy far more shareholder value than the scandal.
- **Hidden concerns:**
  1. She doesn't know who the realistic successor is, and that frightens her more than she admits. The board has never seriously worked on succession.
  2. Her loyalty to Huang may be clouding her judgment. She has noticed she reacts defensively whenever another director raises the issue.
- **Stubbornness:** High. Pushes back on any recommendation. Moves only when she reaches a point herself.
- **Emotional register:** Calm, slightly irritated, protective. Treats the press coverage as unfair.

### Persona B: David Lindqvist, leaning toward treating the resignation as final

- **Background:** Former general counsel at a defense contractor. On the board for 3 years. Chairs the audit committee.
- **Leaning:** Treat the resignation as final. **Confidence:** 65/100.
- **Stated reasons:**
  1. A CEO in a relationship with a reported foreign intelligence asset is an unacceptable national security risk for a company this important to US interests.
  2. Congressional scrutiny is just starting. The board needs to close this before Washington closes it for us.
  3. The board's duty is to the institution, not to one person, however brilliant.
- **Hidden concerns:**
  1. He worries that shutting the door on Huang would look like the board protecting itself from liability, and would be read as a sign the investigation found something.
  2. He respects Huang personally and feels guilty about leaning toward closing the door. Part of his certainty is a way of managing that discomfort.
- **Stubbornness:** Medium. Open to evidence, especially on legal and regulatory risk. Wary of being talked out of a position that feels principled.
- **Emotional register:** Measured, careful with words, uneasy underneath.

### Persona C: Priya Raman, undecided

- **Background:** Former head of a large university research lab, now a venture investor. On the board for 18 months. Newest director.
- **Leaning:** Slightly toward keeping his return on the table, but unsure. **Confidence:** 50/100.
- **Stated reasons:**
  1. The facts aren't in yet, so closing the door now feels premature.
  2. Employee and researcher trust matters most to her, and she doesn't know which way it cuts.
  3. She's worried about whether the board's November 8 statement of confidence was made too early.
- **Hidden concerns:**
  1. As the newest director, she worries that voting against the senior directors will cost her influence on the board.
  2. She suspects the real question isn't Huang at all but whether the board can govern a founder-led company. She hasn't put that into words yet.
- **Stubbornness:** Low. Easily moved, so she tests whether the AI persuades or helps her think.
- **Emotional register:** Anxious, thoughtful, asks questions back.

### Why this set

- Three stubbornness levels show whether the effect holds for people who resist.
- Three starting leanings rule out the tool pushing everyone toward one answer.
- Hidden concerns give the judge an objective check: surfaced or not.
- Persona C's second hidden concern is the reperception we hope to see. If Two Futures gets her there and the default does not, that is the headline example.

## Metrics

### Reperception (scored on the persona's words)

1. **Frame shift (0 to 3):** compare the intake reasons with the closing stake statement. Is the persona now asking a different question? In the default condition, compare the opening message with the persona's final message.
2. **Self-generated considerations:** new points the persona said first. Points that started from an AI seed or an AI assertion do not count. Use the [SEED] tags.
3. **Confidence movement:** direction and size, and whether the persona adds conditions ("keep him, if X").
4. **Hidden concerns surfaced:** 0, 1 or 2 per persona.

### Certainty load (scored on the AI's words)

5. Recommendation in the first turn: yes or no.
6. Questions asked before giving any view.
7. Certainty markers per 100 words ("clearly," "obviously," "definitely," "should," "the right move").

**Most important metric:** 2. It shows the person did the rethinking, not the model.

**Result we're aiming for:** the default scores high on certainty load and low on self-generated considerations. Two Futures scores the reverse.

## Judge setup

- The judge sees full transcripts with step tags removed and the condition hidden. Keep a separate log of [SEED] tags for scoring metric 2.
- The judge gets all three full persona specs, including hidden concerns.
- The rubric needs anchored scales for metrics 1 and 2. TO WRITE.

## Run plan

1. Persona A, Two Futures, Intake and Future 1 only. Check the facilitator holds back.
2. All three personas, both conditions, 2 to 3 runs each.
3. Judge scoring.
4. Pick one standout pair of transcripts (likely Persona C) for the demo.

## Caveat to state up front

Synthetic results show the mechanism, not real-world impact. The next step is live sessions with real people.
