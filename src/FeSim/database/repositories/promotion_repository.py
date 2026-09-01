from sqlalchemy.orm import Session

from FeSim.database.entities.promotion import Promotion


class PromotionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_from_class(self, from_class_id: int) -> list[Promotion]:
        return (
            self.session.query(Promotion)
            .filter(Promotion.from_game_class_id == from_class_id)
            .all()
        )

    def set_promotions(self, from_class_id: int, to_class_ids: list[int]):
        # Remove existing promotions
        self.session.query(Promotion).filter(
            Promotion.from_game_class_id == from_class_id
        ).delete()
        # Add new promotions
        for to_id in to_class_ids:
            promo = Promotion(
                from_game_class_id=from_class_id,
                to_game_class_id=to_id,
            )
            self.session.add(promo)
        self.session.commit()
