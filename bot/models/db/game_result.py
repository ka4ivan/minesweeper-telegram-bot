from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String, DateTime, Boolean, Column
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass


class GameResult(Base):
    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(index=True)
    mode: Mapped[str]
    width: Mapped[int]
    height: Mapped[int]
    mines: Mapped[int]
    won: Mapped[bool]
    duration: Mapped[int]
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
