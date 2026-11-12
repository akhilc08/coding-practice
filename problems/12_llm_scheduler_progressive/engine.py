"""Inference engine primitives. SYSTEM CODE: DO NOT MODIFY.

The scheduler decides *what* runs each step; these functions do the actual
work and enforce the engine's invariants. Calling them in an invalid order
raises EngineError, which means your scheduler has a bug.
"""

from __future__ import annotations

from dataclasses import dataclass


class EngineError(RuntimeError):
    pass


@dataclass
class Request:
    req_id: int
    prompt_len: int
    max_tokens: int
    prefix_id: str | None = None  # used from Level 3
    prefix_len: int = 0           # used from Level 3
    prefilled: int = 0            # prompt tokens whose KV has been computed
    generated: int = 0            # output tokens produced so far

    @property
    def prefill_done(self) -> bool:
        return self.prefilled == self.prompt_len

    @property
    def done(self) -> bool:
        return self.generated >= self.max_tokens


def prefill(req: Request, n: int | None = None) -> int:
    """Compute KV for the next `n` prompt tokens (default: all remaining).

    Returns the work units used, which equals the number of tokens computed.
    """
    remaining = req.prompt_len - req.prefilled
    if n is None:
        n = remaining
    if n <= 0 or n > remaining:
        raise EngineError(f"req {req.req_id}: bad prefill n={n}, remaining={remaining}")
    req.prefilled += n
    return n


def load_prefix(req: Request) -> None:
    """Copy `req.prefix_len` tokens of cached KV into the request. Costs no work.

    Only valid before any prefill has happened on the request.
    """
    if req.prefix_id is None or req.prefilled != 0:
        raise EngineError(f"req {req.req_id}: load_prefix not allowed here")
    req.prefilled = req.prefix_len


def decode_one(req: Request) -> int:
    """Generate one output token. Returns the work units used (always 1)."""
    if not req.prefill_done:
        raise EngineError(f"req {req.req_id}: decode before prefill finished")
    if req.done:
        raise EngineError(f"req {req.req_id}: decode past max_tokens")
    req.generated += 1
    return 1


def reset(req: Request) -> None:
    """Throw away all KV and generated tokens (used when preempting)."""
    req.prefilled = 0
    req.generated = 0
