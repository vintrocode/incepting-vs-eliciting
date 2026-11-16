# Two Futures runner: change log

- 16 Nov 02:00: prompts switched to Dave's v0.2 files (prompts/). Persona on anthropic/claude-sonnet-5.5; facilitator and chatbot on x-ai/grok-4.7; judge openai/gpt-5.6-terra. Runs [ABC]-{twofutures,default}-[1-3].
- 16 Nov 03:06: chatbot arm rerun with turns matched to each Two Futures twin: [ABC]-default-[4-6].
- 16 Nov 04:10 (Vince): the chatbot kept insisting Huang had not resigned. The default-arm opening now has the persona say these are recent news events, likely after the assistant's training cutoff. Runs from [ABC]-default-7 on.
- 16 Nov 04:25 (Vince's go; Dave's own proposed fixes from his results PDF, applied to our copy; his v0.2 files kept in prompts_dave_v02_2026-11-16/):
  - 02-processing: pivot merged with the Future 2 setup and carries the frame ("...the one where you went the other way... it turned out to be the right call") (his 4a).
  - 00-core rule 8: every facilitator turn ends with a question except the final handoff (his 4c).
  - Runner, study mode: the facilitator gets the interviewer's before-snapshot as intake state and is told to skip steps 1c and 8a (his 4d).
  - Runner, chatbot arm: the persona keeps engaging with substantive follow-ups and does not sign off early; turns fixed at 30; substantive persona turns and AI output tokens are recorded per run (his 4b). The recent-news line stays (Vince, 4f).

Paths above refer to the original workspace (`sim/two_futures/`, `runs/two-futures/`). In this repo: prompts → `two_futures/prompts/`, runs → `results/`.
