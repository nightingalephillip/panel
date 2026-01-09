from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User

from . import service
from .schemas import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseListResponse,
)

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("/", response_model=CaseListResponse)
async def list_cases(
    status: Optional[List[str]] = Query(None),
    priority: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all cases with optional filters."""
    cases, total = await service.get_cases(
        db,
        status=status,
        priority=priority,
        tags=tags,
        search=search,
        page=page,
        page_size=page_size,
    )

    return CaseListResponse(
        items=cases,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new case."""
    case = await service.create_case(db, case_data, current_user.id)
    return case


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single case by ID."""
    case = await service.get_case_by_id(db, case_id)

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: UUID,
    case_data: CaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a case."""
    case = await service.get_case_by_id(db, case_id)

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    updated_case = await service.update_case(db, case, case_data)
    return updated_case


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a case."""
    case = await service.get_case_by_id(db, case_id)

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    await service.delete_case(db, case)
