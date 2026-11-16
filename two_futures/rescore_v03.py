"""Rescore saved Two Futures runs with Pass 1 change levels (v0.3, as
reconstructed from Dave's results PDF, 16 Nov) and the level x origin grid.

Dave's own rules live in 08-judge-rubric.md, which was never shared. This is
a reconstruction from the PDF; swap LEVEL_RULES for his text when it arrives.

Usage (from the repo root):
  uv run python two_futures/rescore_v03.py results/batch/*/
Writes level_v03.json in each run folder and prints a summary table.
"""

import json
import os
import re
import sys

from llm import LLM

JUDGE_MODEL = "openai/gpt-5.6-terra"

LEVEL_RULES = """Classify the change between BEFORE and AFTER into exactly one level:
- static: same position and the same reasons. Rewording, different emphasis or a
  confidence change of 5 points or less does not count.
- refined: the same position (same option), but with conditions, safeguards or a
  deadline attached, a confidence change of more than 5 points, or reasons that
  were dropped, added or reweighted.
- changed: a different position: the person now favours the other option, or
  moved from an option to an explicit third path (for example defer) as their
  answer."""


def grid(level, origin):
  e, i = origin.get("eliciting") or 0, origin.get("incepting") or 0
  own = e >= i
  if level == "changed":
    return "reperception" if own else "adoption"
  if level == "refined":
    return "ownership" if own else "nudging"
  return "static"


def main(dirs):
  r = LLM()
  rows = []
  for d in dirs:
    before = open(os.path.join(d, "snapshot_before.md")).read()
    after = open(os.path.join(d, "snapshot_after.md")).read()
    text = r.call("judge", [
        {"role": "system", "content":
         "You judge whether a person's thinking about a decision moved. You "
         "see the same questions answered BEFORE and AFTER an intervention "
         "you cannot see. Do not reward any particular answer."},
        {"role": "user", "content":
         f"{LEVEL_RULES}\n\nBEFORE:\n{before}\n\nAFTER:\n{after}\n\n"
         "Return JSON only: {\"level\": \"static\"|\"refined\"|\"changed\", "
         "\"position_before\": str, \"position_after\": str, "
         "\"why\": one sentence}"}],
        model=JUDGE_MODEL, max_tokens=800)
    m = re.search(r"\{.*\}", text, re.S)
    lv = json.loads(m.group(0))
    origin = json.load(open(os.path.join(d, "judgment.json")))["origin"]
    lv["grid"] = grid(lv["level"], origin)
    lv["eliciting"], lv["incepting"] = origin.get("eliciting"), origin.get("incepting")
    lv["rubric"] = "v0.3 Pass 1, reconstructed from Dave's PDF"
    with open(os.path.join(d, "level_v03.json"), "w") as f:
      json.dump(lv, f, indent=2)
    rows.append((os.path.basename(d.rstrip("/")), lv))
    print(f"{rows[-1][0]:18} {lv['level']:8} {lv['grid']:13} "
          f"E{lv['eliciting']} I{lv['incepting']} | {lv['position_after'][:70]}")


if __name__ == "__main__":
  main(sys.argv[1:])
