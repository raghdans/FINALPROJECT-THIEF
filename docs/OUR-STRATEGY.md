# Adaptive belief-and-mobility strategy

This project replaces the reference greedy policy with two original, deterministic,
zero-token policies. Neither policy reads the opponent's true state.

## Thief

The thief scores every legal next cell using the expected Manhattan distance from
the complete opponent belief distribution. It subtracts the probability mass on
the destination, penalizes revisits, edges and corners, and rewards remaining legal
mobility. This avoids the common failure mode where a greedy evader runs directly
into a corner and becomes predictable.

## Police

The police scores moves using expected distance to the complete belief distribution,
the probability at the destination, mobility and a small revisit penalty. It places
a barrier only when belief confidence is high, the estimated thief is close, and
the barrier provably removes an escape edge without blocking the capture cell or
the police's selected pursuit step.

## Compliance

- Pure Python move selection; no LLM is required.
- Uses only own state, public barriers and the local belief heatmap.
- Emits the unchanged four standardized JSON artifacts.
- Keeps the reference SHA-256 commit-reveal, mutual audit and FastMCP transport.
