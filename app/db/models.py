import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase, Mapped, backref, mapped_column,
                            relationship)


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Модель пользователя
    """

    ROLES = ("admin", "user")

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


class Salary(Base):
    """
    Модель зарплаты
    """

    __tablename__ = "salaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id",
                                                          ondelete="CASCADE"))
    current_salary: Mapped[float] = mapped_column(nullable=True)
    increase_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )

    user = relationship("User", backref=backref(
        "salary", uselist=False, lazy="joined"
    ))
