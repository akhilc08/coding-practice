# LLM Inference Scheduler — 5-level timed mock

Modeled on the Anthropic Fellows OA as candidates describe it: an existing
Python codebase, an LLM request scheduler with prefill/decode, caching, and
load balancing. Levels 2–5 are my own extrapolation; only the Level 1 rules
come from public write-ups.

**90 minutes total, no AI, no peeking ahead.** Open each `levelN.md` only after
`pytest test_levelN.py` passes. Earlier tests must keep passing.

Rough pacing: L1 15 min · L2 15 · L3 15 · L4 25 · L5 20.

- `engine.py` is **system code**: read it first, import from it, never edit it.
  It raises `EngineError` if your scheduler drives it wrong.
- `scheduler.py` is yours (Levels 1–4). `cluster.py` is yours (Level 5).
- Every new constructor option defaults to "off", so earlier levels' behavior
  must stay exactly the same.
