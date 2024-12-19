import uuid
from datetime import datetime as dt
from datetime import timezone

from sqlalchemy import func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


def get_utc_now() -> dt:
    return dt.now(tz=timezone.utc)


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index(
            "idx_created_at_id",
            "created_at",
            "id",
            postgresql_using="btree",
            postgresql_ops={"created_at": "ASC", "id": "ASC"},
        ),
    )

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=False)
    email: Mapped[str] = mapped_column(unique=False)
    created_at: Mapped[dt] = mapped_column(server_default=func.now(), default=get_utc_now)
