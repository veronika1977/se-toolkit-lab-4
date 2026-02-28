"""Unit tests for item router edge cases and boundary values."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.models.item import ItemCreate, ItemUpdate
from app.routers.items import get_item, put_item, post_item


@pytest.mark.asyncio
async def test_get_item_returns_404_when_not_found() -> None:
    """Test that fetching a non-existent item returns 404."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_item(item_id=999, session=mock_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not found"


@pytest.mark.asyncio
async def test_get_item_with_zero_id_returns_404() -> None:
    """Test boundary value: item_id=0 should return 404 if not found."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_item(item_id=0, session=mock_session)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_item_with_negative_id_returns_404() -> None:
    """Test boundary value: negative item_id should return 404 if not found."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await get_item(item_id=-1, session=mock_session)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_put_item_returns_404_when_item_not_found() -> None:
    """Test that updating a non-existent item returns 404."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(return_value=None)

    body = ItemUpdate(title="Updated Title", description="Updated description")

    with pytest.raises(HTTPException) as exc_info:
        await put_item(item_id=999, body=body, session=mock_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Item not found"


@pytest.mark.asyncio
async def test_post_item_with_empty_title_raises_integrity_error() -> None:
    """Test boundary value: creating item with empty title should raise IntegrityError."""
    mock_session = AsyncMock()

    # Simulate IntegrityError for invalid data
    with patch(
        "app.routers.items.create_item", new_callable=AsyncMock
    ) as mock_create:
        from sqlalchemy.exc import IntegrityError

        mock_create.side_effect = IntegrityError(
            statement="INSERT INTO item",
            params={"title": ""},
            orig="null value in column",
        )

        body = ItemCreate(type="step", parent_id=None, title="", description="")

        with pytest.raises(HTTPException) as exc_info:
            await post_item(body=body, session=mock_session)

        assert exc_info.value.status_code == 422
        assert (
            exc_info.value.detail
            == "parent_id does not reference an existing item"
        )
"""Unit tests for items router."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_item_nonexistent_id_returns_404():
    """Test that GET /items/999 returns 404 for non-existent item."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_post_item_empty_title_returns_422():
    """Test that POST /items/ with empty title returns validation error."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/items/",
            json={
                "title": "",  # пустой title
                "description": "Test description"
            }
        )
    assert response.status_code == 422
