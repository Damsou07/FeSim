from sqlalchemy.orm import Session

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

    def create(self, **kwargs) -> GameClass:
        game_class = GameClass(**kwargs)
        self.session.add(game_class)
        self.session.commit()
        self.session.refresh(game_class)
        return game_class

    def update(self, class_id: int, **kwargs) -> GameClass | None:
        game_class = self.get_by_id(class_id)
        if game_class is None:
            return None
        for key, value in kwargs.items():
            setattr(game_class, key, value)
        self.session.commit()
        self.session.refresh(game_class)
        return game_class

    def delete(self, class_id: int) -> bool:
        game_class = self.get_by_id(class_id)
        if game_class is None:
            return False
        self.session.delete(game_class)
        self.session.commit()
        return True
