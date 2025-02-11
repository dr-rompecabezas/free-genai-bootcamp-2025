from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base import get_db
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate, Group as GroupSchema

router = APIRouter()

@router.get("/", response_model=List[GroupSchema])
async def read_groups(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve groups.
    """
    async with db as session:
        result = await session.execute(
            select(Group).offset(skip).limit(limit)
        )
        groups = result.scalars().all()
        return groups

@router.post("/", response_model=GroupSchema)
async def create_group(
    group: GroupCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new group.
    """
    db_group = Group(
        name=group.name,
        description=group.description
    )
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group

@router.get("/{group_id}", response_model=GroupSchema)
async def read_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get group by ID.
    """
    async with db as session:
        result = await session.execute(
            select(Group).filter(Group.id == group_id)
        )
        group = result.scalar_one_or_none()
        
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/{group_id}", response_model=GroupSchema)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a group.
    """
    async with db as session:
        result = await session.execute(
            select(Group).filter(Group.id == group_id)
        )
        db_group = result.scalar_one_or_none()
        
        if db_group is None:
            raise HTTPException(status_code=404, detail="Group not found")
            
        update_data = group_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_group, field, value)
            
        await session.commit()
        await session.refresh(db_group)
        return db_group

@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a group.
    """
    async with db as session:
        result = await session.execute(
            select(Group).filter(Group.id == group_id)
        )
        group = result.scalar_one_or_none()
        
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")
            
        await session.delete(group)
        await session.commit()
        
    return {"ok": True}
