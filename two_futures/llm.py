"""Minimal OpenRouter client: retries, token-limit handling, usage per role."""

import os
import time

from openai import OpenAI

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REASONING_TOKENS = 4000  # cap hidden reasoning so the visible answer fits
MAX_ATTEMPTS = 8         # OpenRouter rate limits (429) are retried with backoff


def api_key():
  """OPENROUTER_API_KEY from the environment, else from .env at the repo root."""
  if os.getenv("OPENROUTER_API_KEY"):
    return os.environ["OPENROUTER_API_KEY"]
  path = os.path.join(REPO, ".env")
  if os.path.exists(path):
    with open(path) as f:
      for line in f:
        if line.startswith("OPENROUTER_API_KEY="):
          return line.split("=", 1)[1].strip().strip('"')
  raise RuntimeError("Set OPENROUTER_API_KEY or put it in .env (see .env.example)")


class LLM:

  def __init__(self):
    self.client = OpenAI(base_url="https://openrouter.ai/api/v1",
                         api_key=api_key())
    self.usage = {}  # role -> [calls, prompt_tokens, completion_tokens]
    self.notes = []

  def call(self, role, messages, model, max_tokens=4000, temperature=None):
    extra = {"reasoning": {"max_tokens": REASONING_TOKENS}}
    max_tokens += REASONING_TOKENS
    for attempt in range(MAX_ATTEMPTS):
      try:
        r = self.client.chat.completions.create(
            model=model, messages=messages, max_tokens=max_tokens,
            extra_body=extra,
            **({} if temperature is None else {"temperature": temperature}))
        if not (r.choices[0].message.content or "").strip():
          raise RuntimeError(
              f"empty output (finish={r.choices[0].finish_reason})")
        if r.choices[0].finish_reason == "length" and attempt == 0:
          print(f"  {role}: hit token limit; retrying with double budget")
          max_tokens *= 2
          continue
        if r.choices[0].finish_reason == "length":
          self.notes.append(f"{role}: output truncated at token limit.")
        break
      except Exception as e:  # network / rate limit
        if attempt == MAX_ATTEMPTS - 1:
          raise
        print(f"  retry {role}: {type(e).__name__}: {str(e)[:120]}")
        time.sleep(5 * (attempt + 1))
    u = self.usage.setdefault(role, [0, 0, 0])
    u[0] += 1
    if r.usage:
      u[1] += r.usage.prompt_tokens or 0
      u[2] += r.usage.completion_tokens or 0
    return r.choices[0].message.content or ""
