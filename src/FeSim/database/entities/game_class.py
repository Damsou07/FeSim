from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..connection import Base


if TYPE_CHECKING:
    from FeSim.database.entities.promotion import Promotion
    from FeSim.database.entities.character import Character


class GameClass(Base):
    __tablename__ = "game_classes"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Niveau de la classe à que deux valeurs possible "pre promotion" ou "post promotion"
    level_class: Mapped[str] = mapped_column(String, nullable=False)

    game: Mapped[str] = mapped_column(String(100), nullable=False)
    class_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Bonus obtenus lors de la promotion, concerne uniquement les classes post promotion
    promotion_hp: Mapped[int] = mapped_column(Integer, default=0)
    promotion_str: Mapped[int] = mapped_column(Integer, default=0)
    promotion_mag: Mapped[int] = mapped_column(Integer, default=0)
    promotion_skl: Mapped[int] = mapped_column(Integer, default=0)
    promotion_spd: Mapped[int] = mapped_column(Integer, default=0)
    promotion_lck: Mapped[int] = mapped_column(Integer, default=0)
    promotion_def: Mapped[int] = mapped_column(Integer, default=0)
    promotion_res: Mapped[int] = mapped_column(Integer, default=0)

    # Cap de classe
    cap_hp: Mapped[int] = mapped_column(Integer, default=0)
    cap_str: Mapped[int] = mapped_column(Integer, default=0)
    cap_mag: Mapped[int] = mapped_column(Integer, default=0)
    cap_skl: Mapped[int] = mapped_column(Integer, default=0)
    cap_spd: Mapped[int] = mapped_column(Integer, default=0)
    cap_lck: Mapped[int] = mapped_column(Integer, default=0)
    cap_def: Mapped[int] = mapped_column(Integer, default=0)
    cap_res: Mapped[int] = mapped_column(Integer, default=0)

    characters: Mapped[list["Character"]] = relationship(
        "Character",
        back_populates="game_class",
    )

    # Relations de promotion
    promotions_from: Mapped[list["Promotion"]] = relationship(
        "Promotion",
        foreign_keys="Promotion.from_game_class_id",
        back_populates="from_game_class",
    )

    promotions_to: Mapped[list["Promotion"]] = relationship(
        "Promotion",
        foreign_keys="Promotion.to_game_class_id",
        back_populates="to_game_class",
    )