from FeSim.database.entities.game_class import GameClass
from FeSim.database.repositories.game_class_repository import GameClassRepository


class GameClassService:
    def __init__(self, repository: GameClassRepository):
        self.repository = repository

    def get_all(self) -> list[GameClass]:
        return self.repository.get_all()

    def get_by_id(self, class_id: int) -> GameClass | None:
        return self.repository.get_by_id(class_id)

    def create(self, data: dict) -> GameClass:
        return self.repository.create(**data)

    def update(self, class_id: int, data: dict) -> GameClass | None:
        return self.repository.update(class_id, **data)

    def delete(self, class_id: int): 
        game_class = self.repository.get_by_id(class_id)
        if game_class is None: 
            return False 
        if game_class.characters: 
            raise ValueError( 
                "Impossible de supprimer cette classe : "
                "des personnages lui sont associés." 
            ) 
        self.repository.delete(class_id) 
        return True

    @staticmethod
    def to_dict(gc: GameClass) -> dict:
        return {
            "id": gc.id,
            "game": gc.game,
            "class_name": gc.class_name,
            "level_class": gc.level_class,
            "promotion_hp": gc.promotion_hp,
            "promotion_str": gc.promotion_str,
            "promotion_mag": gc.promotion_mag,
            "promotion_skl": gc.promotion_skl,
            "promotion_spd": gc.promotion_spd,
            "promotion_lck": gc.promotion_lck,
            "promotion_def": gc.promotion_def,
            "promotion_res": gc.promotion_res,
            "cap_hp": gc.cap_hp,
            "cap_str": gc.cap_str,
            "cap_mag": gc.cap_mag,
            "cap_skl": gc.cap_skl,
            "cap_spd": gc.cap_spd,
            "cap_lck": gc.cap_lck,
            "cap_def": gc.cap_def,
            "cap_res": gc.cap_res,
        }
