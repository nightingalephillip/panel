from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.auth.schemas import UserResponse


# Enums as string literals for API
CaseStatusType = str  # "open" | "in_progress" | "pending" | "closed" | "archived"
CasePriorityType = str  # "low" | "medium" | "high" | "critical"
TLPType = str  # "white" | "green" | "amber" | "red"


# Request schemas
class CaseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: CasePriorityType = "medium"
    tlp: TLPType = "amber"
    tags: List[str] = Field(default_factory=list)


class CaseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[CaseStatusType] = None
    priority: Optional[CasePriorityType] = None
    tlp: Optional[TLPType] = None
    tags: Optional[List[str]] = None
    assigned_to_id: Optional[UUID] = None


# Response schemas
class CaseResponse(BaseModel):
    id: UUID
    case_number: str
    title: str
    description: Optional[str]
    status: CaseStatusType
    priority: CasePriorityType
    tlp: TLPType
    tags: List[str]
    created_by: UserResponse
    assigned_to: Optional[UserResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CaseListResponse(BaseModel):
    items: List[CaseResponse]
    total: int
    page: int
    page_size: int


# Query params
class CaseFilters(BaseModel):
    status: Optional[List[CaseStatusType]] = None
    priority: Optional[List[CasePriorityType]] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
