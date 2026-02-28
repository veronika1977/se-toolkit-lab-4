"""Additional unit tests for interactions router."""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_post_interaction_invalid_learner_returns_422():
    """Test that POST /interactions/ with invalid learner_id returns 422."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/interactions/",
            json={
                "learner_id": 999,  # несуществующий ID
                "item_id": 1,
                "kind": "attempt"
            }
        )
    assert response.status_code == 422
    assert "does not reference an existing record" in response.text
