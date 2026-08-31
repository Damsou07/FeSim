from sqlalchemy.orm import Session

import FeSim.database.entities  # noqa: F401 – ensure all entities are registered
from FeSim.database.entities.game_class import GameClass


class GameClassRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[GameClass]:
        return self.session.query(GameClass).all()

    def get_by_id(self, class_id: int) -> GameClass | None:
        return self.session.query(GameClass).filter(GameClass.id == class_id).first()

    def get_or_create(self, game: str, class_name: str) -> GameClass:
        existing = (
            self.session.query(GameClass)
            .filter(GameClass.game == game, GameClass.class_name == class_name)
            .first()
        )
        if existing:
            return existing
        game_class = GameClass(game=game, class_name=class_name)
        self.session.add(game_class)
        self.session.commit()
        self.session.refresh(game_class)
        return game_class
