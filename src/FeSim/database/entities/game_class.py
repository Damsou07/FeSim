from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..connection import Base


class GameClass(Base):
    __tablename__ = "game_classes"

    id: Mapped[int] = mapped_column(primary_key=True)

    game: Mapped[str] = mapped_column(String(100), nullable=False)
    class_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Bonus obtenus lors de la promotion
    promotion_hp: Mapped[int] = mapped_column(Integer, default=0)
    promotion_str: Mapped[int] = mapped_column(Integer, default=0)
    promotion_mag: Mapped[int] = mapped_column(Integer, default=0)
    promotion_skl: Mapped[int] = mapped_column(Integer, default=0)
    promotion_spd: Mapped[int] = mapped_column(Integer, default=0)
    promotion_lck: Mapped[int] = mapped_column(Integer, default=0)
    promotion_def: Mapped[int] = mapped_column(Integer, default=0)
    promotion_res: Mapped[int] = mapped_column(Integer, default=0)

    characters: Mapped[list["Character"]] = relationship(
        back_populates="game_class"
    )