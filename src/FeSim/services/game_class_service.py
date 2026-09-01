from FeSim.database.entities.game_class import GameClass
from FeSim.database.repositories.game_class_repository import GameClassRepository
from FeSim.database.repositories.promotion_repository import PromotionRepository


class GameClassService:
    def __init__(self, repository: GameClassRepository, promotion_repository: PromotionRepository):
        self.repository = repository
        self.promotion_repository = promotion_repository

    def get_all(self) -> list[GameClass]:
        return self.repository.get_all()

    def get_by_id(self, class_id: int) -> GameClass | None:
        return self.repository.get_by_id(class_id)

    def create(self, data: dict) -> GameClass:
        promo_to_ids = data.pop("promotion_to_ids", [])
        gc = self.repository.create(**data)
        if promo_to_ids:
            self.promotion_repository.set_promotions(gc.id, promo_to_ids)
        return gc

    def update(self, class_id: int, data: dict) -> GameClass | None:
        promo_to_ids = data.pop("promotion_to_ids", None)
        gc = self.repository.update(class_id, **data)
        if gc is not None and promo_to_ids is not None:
            self.promotion_repository.set_promotions(class_id, promo_to_ids)
        return gc

    def delete(self, class_id: int):
        game_class = self.repository.get_by_id(class_id)
        if game_class is None:
            return False
        if game_class.characters:
            raise ValueError(
                "Impossible de supprimer cette classe : "
                "des personnages lui sont associés."
            )
        # Delete related promotions
        self.promotion_repository.set_promotions(class_id, [])
        self.repository.delete(class_id)
        return True

    def get_promotion_to_ids(self, from_class_id: int) -> list[int]:
        promos = self.promotion_repository.get_by_from_class(from_class_id)
        return [p.to_game_class_id for p in promos]

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
