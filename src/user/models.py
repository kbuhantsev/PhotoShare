import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String, MetaData

from src.models import Base


class Role(enum.Enum):
    USER = 0
    ADMIN = 1
    MODERATOR = 2


class User(Base):
    __tablename__ = "users"
    role: Mapped[Enum] = mapped_column(Enum(Role), default=Role.USER)
    username: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f"User(name={self.username}, role={self.role})"
