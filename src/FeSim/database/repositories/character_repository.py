from sqlalchemy.orm import Session

from FeSim.database.entities.character import Character


class CharacterRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Character]:
        return self.session.query(Character).all()

    def get_by_id(self, character_id: int) -> Character | None:
        return self.session.query(Character).filter(Character.id == character_id).first()

    def create(self, **kwargs) -> Character:
        character = Character(**kwargs)
        self.session.add(character)
        self.session.commit()
        self.session.refresh(character)
        return character

    def update(self, character_id: int, **kwargs) -> Character | None:
        character = self.get_by_id(character_id)
        if character is None:
            return None
        for key, value in kwargs.items():
            setattr(character, key, value)
        self.session.commit()
        self.session.refresh(character)
        return character

    def delete(self, character_id: int) -> bool:
        character = self.get_by_id(character_id)
        if character is None:
            return False
        self.session.delete(character)
        self.session.commit()
        return True
