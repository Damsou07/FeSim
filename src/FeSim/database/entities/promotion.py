from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..connection import Base

if TYPE_CHECKING:
    from FeSim.database.entities.game_class import GameClass


class Promotion(Base):
    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(primary_key=True)

    from_game_class_id: Mapped[int] = mapped_column(
        ForeignKey("game_classes.id"),
        nullable=False,
    )

    to_game_class_id: Mapped[int] = mapped_column(
        ForeignKey("game_classes.id"),
        nullable=False,
    )

    # Relations vers les deux GameClass
    from_game_class: Mapped["GameClass"] = relationship(
        "GameClass",
        foreign_keys=[from_game_class_id],
        back_populates="promotions_from",
    )

    to_game_class: Mapped["GameClass"] = relationship(
        "GameClass",
        foreign_keys=[to_game_class_id],
        back_populates="promotions_to",
    )