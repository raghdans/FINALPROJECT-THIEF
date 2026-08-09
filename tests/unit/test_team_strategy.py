from police_thief.constants import MoveType, Role
from police_thief.domain.belief import BeliefGrid
from police_thief.domain.own_state import OwnGameState
from team_strategy import AdaptivePoliceBrain, AdaptiveThiefBrain


def _view(role, start):
    state = OwnGameState(role, start, 7, ["N", "S", "E", "W", "STAY"])
    belief = BeliefGrid(7, orthogonal=True)
    belief.observe_smell({"3,3": 1.0, "3,4": 0.8, "2,3": 0.6})
    return state, belief


def test_thief_returns_legal_non_barrier_move():
    state, belief = _view(Role.THIEF, (3, 3))
    decision = AdaptiveThiefBrain().decide(state, belief, "", "", 14)
    assert decision.move_type is MoveType.MOVE
    assert state.board.step(state.position, decision.direction, state.barriers) is not None


def test_police_returns_legal_action():
    state, belief = _view(Role.POLICE, (2, 2))
    decision = AdaptivePoliceBrain().decide(state, belief, "", "", 14)
    assert decision.move_type in (MoveType.MOVE, MoveType.BARRIER)
    assert state.board.step(state.position, decision.direction, state.barriers) is not None


def test_strategies_are_deterministic_for_same_view():
    first_state, first_belief = _view(Role.THIEF, (3, 3))
    second_state, second_belief = _view(Role.THIEF, (3, 3))
    first = AdaptiveThiefBrain().decide(first_state, first_belief, "", "", 14)
    second = AdaptiveThiefBrain().decide(second_state, second_belief, "", "", 14)
    assert (first.move_type, first.direction) == (second.move_type, second.direction)
