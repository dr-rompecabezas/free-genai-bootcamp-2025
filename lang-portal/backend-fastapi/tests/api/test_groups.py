import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_group(client: AsyncClient):
    """Test creating a new group."""
    group_data = {
        "name": "JLPT N5",
        "description": "Basic vocabulary for JLPT N5"
    }
    response = await client.post("/api/v1/groups/", json=group_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == group_data["name"]
    assert data["description"] == group_data["description"]
    assert "id" in data
    assert "created_at" in data

async def test_read_group(client: AsyncClient, test_group: dict):
    """Test retrieving a group by ID."""
    response = await client.get(f"/api/v1/groups/{test_group['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_group["name"]
    assert data["description"] == test_group["description"]

async def test_read_nonexistent_group(client: AsyncClient):
    """Test retrieving a nonexistent group."""
    response = await client.get("/api/v1/groups/999")
    assert response.status_code == 404

async def test_read_groups(client: AsyncClient, test_group: dict):
    """Test retrieving a list of groups."""
    response = await client.get("/api/v1/groups/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(g["id"] == test_group["id"] for g in data)

async def test_update_group(client: AsyncClient, test_group: dict):
    """Test updating a group."""
    update_data = {
        "description": "Updated description"
    }
    response = await client.put(f"/api/v1/groups/{test_group['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == update_data["description"]
    assert data["name"] == test_group["name"]  # Name should remain unchanged

async def test_delete_group(client: AsyncClient, test_group: dict):
    """Test deleting a group."""
    response = await client.delete(f"/api/v1/groups/{test_group['id']}")
    assert response.status_code == 200
    
    # Verify group is deleted
    response = await client.get(f"/api/v1/groups/{test_group['id']}")
    assert response.status_code == 404

async def test_create_group_duplicate_name(client: AsyncClient, test_group: dict):
    """Test creating a group with a duplicate name."""
    group_data = {
        "name": test_group["name"],
        "description": "Another description"
    }
    response = await client.post("/api/v1/groups/", json=group_data)
    # Note: Current implementation might allow duplicate names
    # If we want to enforce unique names, we should add a unique constraint
    # and update this test accordingly
    assert response.status_code == 200
