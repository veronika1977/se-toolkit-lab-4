"""Unit tests for items router."""

import pytest
from pydantic import ValidationError
from app.models.item import ItemCreate


def test_post_item_empty_title_allowed() -> None:
    """Test that POST /items/ with empty title is allowed (model permits)."""
    item = ItemCreate(title="", description="Test")
    assert item.title == ""
    assert item.description == "Test"


def test_post_item_valid_title_passes() -> None:
    """Test that POST /items/ with valid title passes validation."""
    item = ItemCreate(title="Valid Title", description="Test")
    assert item.title == "Valid Title"
    assert item.description == "Test"
