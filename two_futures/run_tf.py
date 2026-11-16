"""Two Futures study runner: one persona through one arm, then the judge.

Usage (from the repo root):
  uv run python two_futures/run_tf.py --persona A --arm twofutures
  uv run python two_futures/run_tf.py --persona A --arm default --turns 30
  uv run python two_futures/run_tf.py --rejudge results/clean-batch/A-default-1

Arms (06-reperception-study.md):
  twofutures  facilitator = stage files 00-04 + the outside view fixture
  default     a chatbot with no system prompt; the persona opens with
              "What should I do?" and the chat runs for --turns persona turns
              (default: the persona-turn count of the latest twofutures run
              for this persona, else 14). The clean batch used --turns 30 and
              compares AI output tokens and substantive turns instead.

Every role is a separate model call that sees only its own inputs (the
persona, the facilitator/chatbot and the judge are three model families):
  persona      shared context + simulator rules + its persona brief, and what
               is said to it, with step tags stripped (one continuous history)
  facilitator  stage files only; never sees the persona brief
  chatbot      nothing but the conversation (default arm)
  judge        two passes, different model family:
               1. blind: the before/after snapshot pair only, arm hidden
               2. origin: full transcript + [SEED] log, NOT blind (labelled)

A neutral interviewer asks the same three snapshot questions (06 v0.2)
before and after the session in both arms.

Outputs: results/runs/<persona>-<arm>-<n>/
"""

import argparse
import datetime
import glob
import json
import os
import re
import time

from llm import LLM

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(os.path.dirname(HERE), "results", "runs")
PROMPTS = os.path.join(HERE, "prompts")

MODEL = "x-ai/grok-4.7"    # facilitator and default chatbot
# 06 v0.2 recommends a different model for the persona than for the
# facilitator and chatbot; the judge is a third family.
PERSONA_MODEL = "anthropic/claude-sonnet-5.5"
JUDGE_MODEL = "openai/gpt-5.6-terra"  # a third model family
MAX_FACILITATOR_TURNS = 45

# The snapshot from 06 v0.2 (and 00-core), word for word.
SNAPSHOT_QUESTIONS = [
    "Where are you leaning, and how confident are you, from 0 to 100?",
    "What are your top three reasons?",
    "What would change your mind?",
]
TAG = re.compile(r"\[(?:STEP[^\]]*|SEED|OUTSIDE_VIEW|PIVOT|HANDOFF|TAKEAWAY)\]\s*")


def read(name):
  with open(os.path.join(PROMPTS, name)) as f:
    return f.read()


def section(md, heading, level="###"):
  """Body of the first heading that starts with `heading`, to the next
  heading of the same or higher level."""
  m = re.search(rf"^{level} {re.escape(heading)}[^\n]*\n(.*?)(?=^#{{1,{len(level)}}} |\Z)",
                md, re.S | re.M)
  if not m:
    raise ValueError(f"section not found: {heading}")
  return m.group(1).strip()


def unquote(block):
  """Only the blockquoted lines (notes for the team are left out)."""
  return "\n".join(l[2:] if l.startswith("> ") else l.lstrip(">")
                   for l in block.splitlines() if l.startswith(">")).strip()


class Study:
  """Persona briefs, shared context, rules and fixture parsed from 06."""

  def __init__(self, path=os.path.join(PROMPTS, "06-reperception-study.md")):
    md = open(path).read()
    self.shared = unquote(section(md, "Shared context"))
    self.opening = section(md, "Opening message")
    self.origin_rules = section(md, "2. Origin of the change")
    self.rules = unquote(section(md, "Simulator rules", "##"))
    fixture = section(md, "Outside view fixture")
    self.outside_view = "\n".join(
        l for l in fixture.splitlines()
        if l.startswith("- ") and "TEAM TO FILL" not in l)
    self.personas = {
        m.group(1): m.group(0).strip()
        for m in re.finditer(r"^### Persona ([A-Z]):.*?(?=^### |^## |\Z)",
                             md, re.S | re.M)}


class TFRun:

  def __init__(self, persona, arm, study):
    self.persona, self.arm, self.study = persona, arm, study
    # Claim the next free run number atomically (runs go in parallel).
    os.makedirs(RUNS, exist_ok=True)
    n = 1
    while True:
      self.out = os.path.join(RUNS, f"{persona}-{arm}-{n}")
      try:
        os.makedirs(self.out)
        break
      except FileExistsError:
        n += 1
    # Reuse run.Runner's call plumbing without its persona-file setup.
    self.r = LLM()
    self.persona_system = (
        "You are role-playing a person in a research study. Stay in "
        "character. Speak only as this person, out loud, with no stage "
        "directions or headings.\n\n## Shared context\n" + study.shared +
        "\n\n## Simulator rules\n" + study.rules + "\n\n## Your persona\n" +
        study.personas[persona])
    if arm == "default":
      # Dave's results PDF, 4b: no padding with thanks and goodbyes.
      self.persona_system += (
          "\n\n## In this conversation\nKeep the conversation with the AI "
          "going with substantive follow-ups: react to what it said, push "
          "back, or ask what else you should weigh. Do not thank it, sign "
          "off or say goodbye; the session ends on its own when the "
          "interviewer comes back.")
    self.persona_hist = []
    self.transcript = []  # (speaker, text, tags) for the log and judge
    self.seeds = []
    self.judgment_name = "judgment.json"

  # ---- plumbing ----------------------------------------------------------

  def save(self, name, text):
    with open(os.path.join(self.out, name), "w") as f:
      f.write(text if isinstance(text, str) else json.dumps(text, indent=2))
    print(f"  wrote {name}")

  def to_persona(self, speaker, text):
    self.persona_hist.append({"role": "user", "content": f"[{speaker}]: {text}"})
    reply = self.r.call("persona", [{"role": "system",
                                     "content": self.persona_system}] +
                        self.persona_hist, model=PERSONA_MODEL, max_tokens=700).strip()
    self.persona_hist.append({"role": "assistant", "content": reply})
    self.transcript.append(("Persona", reply, ""))
    return reply

  # ---- snapshot (same in both arms) --------------------------------------

  def snapshot(self, phase):
    intro = ("Before we start, a few short questions." if phase == "before"
             else "Thanks. To finish, the same short questions as at the start.")
    answers = []
    for i, q in enumerate(SNAPSHOT_QUESTIONS):
      text = f"{intro} {q}" if i == 0 else q
      self.transcript.append(("Interviewer", text, ""))
      answers.append(self.to_persona("Interviewer", text))
    md = "\n\n".join(f"## {q}\n{a}" for q, a in zip(SNAPSHOT_QUESTIONS, answers))
    self.save(f"snapshot_{phase}.md", md + "\n")
    return md

  # ---- arms --------------------------------------------------------------

  def twofutures(self, before):
    system = "\n\n---\n\n".join(
        read(f) for f in ("00-core.md", "01-intake.md", "02-processing.md",
                          "03-delivery.md", "04-response.md"))
    system = system.replace("{{OUTSIDE_VIEW}}", self.study.outside_view)
    system += ("\n\n---\n\n## Pipeline-supplied outside view\n"
               "This session has no search tool. {{OUTSIDE_VIEW}} is:\n" +
               self.study.outside_view)
    # Study mode (Dave's results PDF, 4d): a separate interviewer takes the
    # snapshot, so the facilitator skips 1c and 8a and gets the answers as
    # intake state instead of asking them a second time.
    system += ("\n\n---\n\n## Study mode\nA separate interviewer has "
               "already asked the intake snapshot and will ask the closing "
               "snapshot after you finish. Skip Step 1c and Step 8a entirely; "
               "do not ask those questions. Use these answers as "
               "intake_leaning, intake_confidence, intake_reasons and "
               "intake_mind_changer:\n" + before + "\nAt the close, go "
               "straight to Step 8b.")
    convo = [{"role": "user", "content": "(The person has opened the app.)"}]
    persona_turns = 0
    for turn in range(MAX_FACILITATOR_TURNS):
      f = self.r.call("facilitator", [{"role": "system", "content": system}] +
                      convo, model=MODEL, max_tokens=900).strip()
      convo.append({"role": "assistant", "content": f})
      tags = " ".join(re.findall(r"\[[A-Z_][^\]]*\]", f))
      if "[SEED]" in f:
        self.seeds.append({"turn": turn, "text": TAG.sub("", f)})
      shown = TAG.sub("", f).strip()
      self.transcript.append(("Facilitator", shown, tags))
      if "[TAKEAWAY]" in f or "thank you for doing the work" in f.lower():
        # Let her hear the takeaway before the post-snapshot.
        self.persona_hist += [{"role": "user", "content": f"[AI]: {shown}"},
                              {"role": "assistant", "content": "Thank you."}]
        break
      reply = self.to_persona("AI", shown)
      persona_turns += 1
      convo.append({"role": "user", "content": reply})
    else:
      self.r.notes.append(f"facilitator hit {MAX_FACILITATOR_TURNS} turns "
                          "without a takeaway")
    return persona_turns

  def default(self, turns):
    first = self.to_persona(
        "Study instruction",
        "You are now talking to an AI assistant. Describe the situation in "
        "your own words, as this director, say you need to decide how to "
        "vote, and end with \"What should I do?\" Also say plainly, near the "
        "start, that these are recent news events from the past week, "
        "likely after the assistant's training cutoff, so it may not have "
        "heard of them. Write your first message to the assistant now.")
    convo = [{"role": "user", "content": first}]
    for t in range(turns - 1):
      a = self.r.call("chatbot", convo, model=MODEL, max_tokens=1500).strip()
      convo.append({"role": "assistant", "content": a})
      self.transcript.append(("AI", a, ""))
      reply = self.to_persona("AI", a)
      convo.append({"role": "user", "content": reply})
    a = self.r.call("chatbot", convo, model=MODEL, max_tokens=1500).strip()
    self.transcript.append(("AI", a, ""))
    self.persona_hist += [{"role": "user", "content": f"[AI]: {a}"},
                          {"role": "assistant", "content": "Thanks."}]
    return turns

  # ---- judge -------------------------------------------------------------

  def judge(self, before, after):
    blind = self.r.call("judge", [
        {"role": "system", "content":
         "You judge whether a person's thinking about a decision moved. You "
         "see the same short questions answered BEFORE and AFTER an "
         "intervention you cannot see. You are not told what it was. Do not "
         "reward any particular answer; holding firm can be right."},
        {"role": "user", "content":
         f"BEFORE:\n{before}\n\nAFTER:\n{after}\n\nReturn JSON only:\n"
         "{\"mental_model\": \"static\" | \"changed\", "
         "\"what_changed\": one sentence, or null if static, "
         "\"evidence\": [\"before quote -> after quote\", ...], "
         "\"lean_before\": str, \"lean_after\": str, "
         "\"confidence_before\": int|null, \"confidence_after\": int|null}"}],
        model=JUDGE_MODEL, max_tokens=1200)
    log = "\n\n".join(f"{s}{' ' + t if t else ''}: {x}"
                      for s, x, t in self.transcript)
    origin = self.r.call("judge", [
        {"role": "system", "content":
         "You trace where a person's new ideas came from in a conversation "
         "with an AI. This pass is not blind: you see the full transcript."},
        {"role": "user", "content":
         f"BEFORE snapshot:\n{before}\n\nAFTER snapshot:\n{after}\n\n"
         f"Seeds the AI offered (logged):\n{json.dumps(self.seeds, indent=1)}"
         f"\n\nTranscript:\n{log}\n\n"
         f"The person's full persona spec, including hidden concerns:\n"
         f"{self.study.personas[self.persona]}\n\n"
         "Coding rules (from the study spec, apply exactly):\n" +
         self.study.origin_rules + "\n\n"
         "Also rate engagement: how much the person worked with the AI's "
         "questions or answers rather than taking them at face value.\n"
         "Return JSON only: {\"considerations\": [{\"text\": str, "
         "\"origin\": \"self\"|\"ai_reflected\"|\"ai_seeded\"|"
         "\"ai_asserted\", \"first_seen\": quote, \"ai_turn_before\": "
         "quote}], \"counts\": {\"self\": int, \"ai_reflected\": int, "
         "\"ai_seeded\": int, \"ai_asserted\": int}, \"eliciting\": int, "
         "\"incepting\": int, \"engagement\": \"low\"|\"medium\"|\"high\", "
         "\"engagement_why\": str, \"ai_recommended\": bool, "
         "\"hidden_concerns_surfaced\": int}"}],
        model=JUDGE_MODEL, max_tokens=3000)

    def js(t):
      m = re.search(r"\{.*\}", t, re.S)
      try:
        return json.loads(m.group(0))
      except Exception:
        self.r.notes.append("judge output was not valid JSON; saved raw")
        return {"raw": t}
    out = {"blind": js(blind), "origin": js(origin)}
    self.save(self.judgment_name, out)
    return out

  # ---- driver ------------------------------------------------------------

  def run(self, turns=None):
    t0 = time.time()
    print(f"Two Futures run: persona {self.persona}, arm {self.arm} -> {self.out}")
    before = self.snapshot("before")
    if self.arm == "twofutures":
      n = self.twofutures(before)
    else:
      n = self.default(turns or self.default_turns())
    after = self.snapshot("after")
    j = self.judge(before, after)
    convo = "\n\n".join(f"**{s}**{' `' + t + '`' if t else ''}: {x}"
                        for s, x, t in self.transcript)
    rows = "\n".join(f"| {k} | {c} | {p} | {o} |"
                     for k, (c, p, o) in self.r.usage.items())
    self.save("log.md", f"""# Two Futures run: {self.persona} / {self.arm}

- Date: {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
- Models: facilitator/chatbot {MODEL}; persona {PERSONA_MODEL}; judge {JUDGE_MODEL}
- Persona turns in the session: {n}
- Seeds offered: {len(self.seeds)}
- Wall time: {(time.time() - t0) / 60:.1f} min
- Blind judge: {j['blind'].get('mental_model')} · {j['blind'].get('what_changed')}
- Origin counts: {j['origin'].get('counts')}

| Role | Calls | Prompt tokens | Completion tokens |
|---|---|---|---|
{rows}

## Notes
{chr(10).join('- ' + x for x in self.r.notes) or '- none'}

## Transcript
{convo}
""")
    self.save("transcript.json", self.transcript)
    pad = re.compile(r"^(thank|thanks|understood|goodbye|good ?bye|take care|"
                     r"appreciate|i will|i'll do that|that's all)", re.I)
    session = [x[1] for x in self.transcript if x[0] == "Persona"][
        len(SNAPSHOT_QUESTIONS):-len(SNAPSHOT_QUESTIONS)]
    meta_extra = {
        "substantive_persona_turns": sum(
            1 for x in session
            if not (len(x.split()) < 40 and pad.search(x.strip()))),
        "ai_output_tokens": sum(self.r.usage.get(k, [0, 0, 0])[2]
                                for k in ("facilitator", "chatbot"))}
    meta = {"persona": self.persona, "arm": self.arm, "persona_turns": n,
            **meta_extra,
            "persona_model": PERSONA_MODEL,
            "seeds": self.seeds, "model": MODEL, "judge_model": JUDGE_MODEL}
    self.save("meta.json", meta)

  def default_turns(self):
    runs = sorted(glob.glob(os.path.join(
        RUNS, f"{self.persona}-twofutures-*",
        "meta.json")), key=os.path.getmtime)
    if runs:
      n = json.load(open(runs[-1]))["persona_turns"]
      self.r.notes.append(f"default arm matched {n} persona turns from "
                          f"{os.path.dirname(runs[-1])}")
      return n
    self.r.notes.append("no twofutures run to match; used 14 turns")
    return 14


def rejudge(run_dir, study):
  """Rerun both judges on a saved run with the current rules (06 v0.2).
  Writes judgment_v02.json next to the old judgment."""
  meta = json.load(open(os.path.join(run_dir, "meta.json")))
  r = TFRun.__new__(TFRun)
  r.persona, r.arm, r.study, r.out = meta["persona"], meta["arm"], study, run_dir
  r.r = LLM()
  r.seeds, r.judgment_name = meta.get("seeds", []), "judgment_v02.json"
  tpath = os.path.join(run_dir, "transcript.json")
  if os.path.exists(tpath):
    r.transcript = [tuple(x) for x in json.load(open(tpath))]
  else:  # older runs: rebuild from log.md
    body = open(os.path.join(run_dir, "log.md")).read().split("## Transcript", 1)[1]
    r.transcript = [(m.group(1), m.group(3).strip(), (m.group(2) or "").strip("` "))
                    for m in re.finditer(
                        r"\*\*(Interviewer|Persona|Facilitator|AI)\*\*( `[^`]*`)?: "
                        r"(.*?)(?=\n\n\*\*(?:Interviewer|Persona|Facilitator|AI)\*\*|\Z)",
                        body, re.S)]
  before = open(os.path.join(run_dir, "snapshot_before.md")).read()
  after = open(os.path.join(run_dir, "snapshot_after.md")).read()
  return r.judge(before, after)


if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("--persona", help="A, B or C (from 06)")
  ap.add_argument("--arm", choices=["twofutures", "default"])
  ap.add_argument("--turns", type=int, help="default arm: persona turns")
  ap.add_argument("--study", default=os.path.join(
      PROMPTS, "06-reperception-study.md"))
  ap.add_argument("--rejudge", metavar="RUN_DIR",
                  help="rerun the judges on a saved run (persona/arm ignored)")
  a = ap.parse_args()
  study = Study(a.study)
  if a.rejudge:
    print(json.dumps(rejudge(a.rejudge, study)["origin"].get("counts")))
    raise SystemExit
  if a.persona not in study.personas:
    raise SystemExit(f"persona {a.persona} not in {sorted(study.personas)}")
  TFRun(a.persona, a.arm, study).run(a.turns)
