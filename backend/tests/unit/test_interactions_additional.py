"""Additional unit tests for interactions router."""

from app.routers.interactions import _filter_by_item_id
from app.models.interaction import InteractionLog


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_empty_for_nonexistent_item_id() -> None:
    """Test filtering by item_id that doesn't exist returns empty list."""
    interactions = [
        _make_log(1, learner_id=1, item_id=1),
        _make_log(2, learner_id=2, item_id=2),
    ]
    result = _filter_by_item_id(interactions, item_id=999)
    assert len(result) == 0
    assert result == []


def test_filter_returns_all_for_multiple_matching_item_ids() -> None:
    """Test filtering by item_id returns all interactions with that item_id."""
    interactions = [
        _make_log(1, learner_id=1, item_id=1),
        _make_log(2, learner_id=2, item_id=1),
        _make_log(3, learner_id=3, item_id=2),
        _make_log(4, learner_id=4, item_id=1),
    ]
    result = _filter_by_item_id(interactions, item_id=1)
    assert len(result) == 3
    assert {i.id for i in result} == {1, 2, 4}
