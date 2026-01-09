from datetime import datetime
from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Case, CaseStatus, CasePriority, TLP
from .schemas import CaseCreate, CaseUpdate


def generate_case_number() -> str:
    """Generate a unique case number based on timestamp."""
    now = datetime.utcnow()
    return f"CASE-{now.strftime('%Y%m%d%H%M%S%f')[:17]}"


async def get_cases(
    db: AsyncSession,
    *,
    status: Optional[List[str]] = None,
    priority: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Tuple[List[Case], int]:
    """Get paginated list of cases with filters."""
    query = select(Case).options(
        selectinload(Case.created_by),
        selectinload(Case.assigned_to),
    )

    # Apply filters
    if status:
        status_enums = [CaseStatus(s) for s in status]
        query = query.where(Case.status.in_(status_enums))

    if priority:
        priority_enums = [CasePriority(p) for p in priority]
        query = query.where(Case.priority.in_(priority_enums))

    if tags:
        # Case must have at least one of the specified tags
        query = query.where(Case.tags.overlap(tags))

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Case.title.ilike(search_term),
                Case.description.ilike(search_term),
                Case.case_number.ilike(search_term),
            )
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Apply pagination and ordering
    query = query.order_by(Case.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    cases = result.scalars().all()

    return list(cases), total


async def get_case_by_id(db: AsyncSession, case_id: UUID) -> Optional[Case]:
    """Get a single case by ID."""
    query = select(Case).options(
        selectinload(Case.created_by),
        selectinload(Case.assigned_to),
    ).where(Case.id == case_id)

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_case_by_number(db: AsyncSession, case_number: str) -> Optional[Case]:
    """Get a single case by case number."""
    query = select(Case).options(
        selectinload(Case.created_by),
        selectinload(Case.assigned_to),
    ).where(Case.case_number == case_number)

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_case(
    db: AsyncSession,
    case_data: CaseCreate,
    user_id: UUID,
) -> Case:
    """Create a new case."""
    case = Case(
        case_number=generate_case_number(),
        title=case_data.title,
        description=case_data.description,
        priority=CasePriority(case_data.priority),
        tlp=TLP(case_data.tlp),
        tags=case_data.tags,
        created_by_id=user_id,
    )

    db.add(case)
    await db.commit()
    await db.refresh(case)

    # Reload with relationships
    return await get_case_by_id(db, case.id)


async def update_case(
    db: AsyncSession,
    case: Case,
    case_data: CaseUpdate,
) -> Case:
    """Update an existing case."""
    update_data = case_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "status" and value is not None:
            value = CaseStatus(value)
        elif field == "priority" and value is not None:
            value = CasePriority(value)
        elif field == "tlp" and value is not None:
            value = TLP(value)
        setattr(case, field, value)

    case.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(case)

    # Reload with relationships
    return await get_case_by_id(db, case.id)


async def delete_case(db: AsyncSession, case: Case) -> None:
    """Delete a case."""
    await db.delete(case)
    await db.commit()
