import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import String, Text, DateTime, Enum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CaseStatus(str, PyEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    CLOSED = "closed"
    ARCHIVED = "archived"


class CasePriority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TLP(str, PyEnum):
    WHITE = "white"
    GREEN = "green"
    AMBER = "amber"
    RED = "red"


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    case_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[CaseStatus] = mapped_column(
        Enum(
            CaseStatus,
            values_callable=lambda x: [e.value for e in x],
            name="casestatus",
        ),
        default=CaseStatus.OPEN,
        nullable=False,
    )
    priority: Mapped[CasePriority] = mapped_column(
        Enum(
            CasePriority,
            values_callable=lambda x: [e.value for e in x],
            name="casepriority",
        ),
        default=CasePriority.MEDIUM,
        nullable=False,
    )
    tlp: Mapped[TLP] = mapped_column(
        Enum(
            TLP,
            values_callable=lambda x: [e.value for e in x],
            name="tlp",
        ),
        default=TLP.AMBER,
        nullable=False,
    )
    tags: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    created_by = relationship(
        "User",
        foreign_keys=[created_by_id],
        lazy="joined",
    )
    assigned_to = relationship(
        "User",
        foreign_keys=[assigned_to_id],
        lazy="joined",
    )
