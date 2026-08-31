from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..connection import Base

if TYPE_CHECKING:
    from FeSim.database.entities.game_class import GameClass


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Classe / jeu
    game_class_id: Mapped[int] = mapped_column(
        ForeignKey("game_classes.id"),
        nullable=False,
    )

    # Stats actuelles
    hp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    str: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mag: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    skl: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    spd: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lck: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    defense: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    res: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Growth rates
    hp_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    str_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mag_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    skl_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    spd_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lck_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    defense_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    res_growth: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    game_class: Mapped[GameClass] = relationship(
        back_populates="characters"
    )