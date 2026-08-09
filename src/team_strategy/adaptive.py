"""Deterministic, zero-token strategies built for the 7x7 orthogonal game.

The agents use only information allowed by the protocol: their own state and the
opponent belief heatmap.  They never inspect the opponent's true position.
"""

from __future__ import annotations

from police_thief.constants import Direction, MoveType
from police_thief.domain.brains import PoliceBrain, ThiefBrain


def _expected_distance(cell, board, probabilities) -> float:
    return sum(
        probability * board.distance(cell, (row, col))
        for row, values in enumerate(probabilities)
        for col, probability in enumerate(values)
    )


def _probability(cell, probabilities) -> float:
    return probabilities[cell[0]][cell[1]]


def _mobility(cell, state, extra_barrier=None) -> int:
    barriers = set(state.barriers)
    if extra_barrier is not None:
        barriers.add(extra_barrier)
    return len(state.board.neighbors(cell, barriers))


class AdaptiveThiefBrain(ThiefBrain):
    """Evade the whole belief distribution while preserving future escape routes."""

    def _pick_move(self, moves, state, belief):
        probabilities = belief.as_matrix()
        size = state.board.size

        def score(item):
            _direction, cell = item
            expected_safety = _expected_distance(cell, state.board, probabilities)
            immediate_risk = _probability(cell, probabilities)
            mobility = _mobility(cell, state)
            on_edge = cell[0] in (0, size - 1) or cell[1] in (0, size - 1)
            in_corner = cell in {
                (0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)
            }
            revisit = cell in state.visited
            # Safety dominates. Mobility prevents self-trapping; edge/corner and
            # revisit penalties keep the route diverse and harder to predict.
            return (
                3.0 * expected_safety
                - 8.0 * immediate_risk
                + 0.9 * mobility
                - 0.7 * revisit
                - 0.35 * on_edge
                - 1.1 * in_corner
            )

        return max(moves, key=lambda item: (score(item), item[0].value))


class AdaptivePoliceBrain(PoliceBrain):
    """Pursue expected thief location and place only tactically useful barriers."""

    def _pick_move(self, moves, state, belief):
        probabilities = belief.as_matrix()

        def score(item):
            _direction, cell = item
            expected_distance = _expected_distance(cell, state.board, probabilities)
            local_probability = _probability(cell, probabilities)
            mobility = _mobility(cell, state)
            revisit = cell in state.visited
            return (
                -3.0 * expected_distance
                + 10.0 * local_probability
                + 0.15 * mobility
                - 0.1 * revisit
            )

        return max(moves, key=lambda item: (score(item), item[0].value))

    def _decide_move(self, state, belief, barriers_max):
        moves = state.board.legal_moves(state.position, state.barriers)
        if not moves:
            return MoveType.HOLD, None

        move_direction, move_cell = self._pick_move(moves, state, belief)
        probabilities = belief.as_matrix()
        target = belief.most_likely()
        confidence = _probability(target, probabilities)
        distance_to_target = state.board.distance(state.position, target)

        if state.my_barriers < barriers_max and confidence >= 0.10 and distance_to_target <= 3:
            candidates: list[tuple[float, Direction]] = []
            for direction, cell in moves:
                # Never wall the best capture cell or the chosen pursuit step.
                if cell in (target, move_cell):
                    continue
                before = _mobility(target, state)
                after = _mobility(target, state, extra_barrier=cell)
                mobility_reduction = before - after
                if mobility_reduction <= 0 or _mobility(state.position, state, cell) < 1:
                    continue
                value = 4.0 * mobility_reduction - 5.0 * _probability(cell, probabilities)
                candidates.append((value, direction))
            if candidates:
                value, direction = max(candidates, key=lambda item: (item[0], item[1].value))
                if value > 0:
                    return MoveType.BARRIER, direction

        return MoveType.MOVE, move_direction
