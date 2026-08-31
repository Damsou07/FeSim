from FeSim.database.entities.character import Character
from FeSim.database.repositories.character_repository import CharacterRepository
from FeSim.database.repositories.game_class_repository import GameClassRepository


class CharacterService:

    def __init__(
        self,
        character_repository: CharacterRepository,
        game_class_repository: GameClassRepository,
    ):
        self.character_repository = character_repository
        self.game_class_repository = game_class_repository

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_all_characters(self):
        return self.character_repository.get_all()

    def get_character(self, character_id: int):
        return self.character_repository.get_by_id(character_id)

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def create_character(self, data: dict):
        data = data.copy()

        game = data.pop("game", "")
        class_name = data.pop("class_name", "")

        data["game_class_id"] = self._get_game_class_id(
            game,
            class_name,
        )

        return self.character_repository.create(**data)

    def update_character(self, character_id: int, data: dict):
        data = data.copy()

        game = data.pop("game", "")
        class_name = data.pop("class_name", "")

        data["game_class_id"] = self._get_game_class_id(
            game,
            class_name,
        )

        return self.character_repository.update(
            character_id,
            **data,
        )

    def delete_character(self, character_id: int):
        return self.character_repository.delete(character_id)

    # ------------------------------------------------------------------
    # Business logic
    # ------------------------------------------------------------------

    def _get_game_class_id(
        self,
        game: str,
        class_name: str,
    ) -> int:

        if game and class_name:
            game_class = self.game_class_repository.get_or_create(
                game,
                class_name,
            )

            return game_class.id

        # Classe "Inconnu"
        default_class = self.game_class_repository.get_or_create(
            "Inconnu",
            "Inconnu",
        )

        return default_class.id

    # ------------------------------------------------------------------
    # Presentation mapping
    # ------------------------------------------------------------------

    @staticmethod
    def to_dict(character: Character) -> dict:
        game_class = character.game_class

        return {
            "id": character.id,
            "name": character.name,
            "level": character.level,

            "game": (
                game_class.game
                if game_class
                else ""
            ),

            "class_name": (
                game_class.class_name
                if game_class
                else ""
            ),

            "hp": character.hp,
            "str": character.str,
            "mag": character.mag,
            "skl": character.skl,
            "spd": character.spd,
            "lck": character.lck,
            "defense": character.defense,
            "res": character.res,

            "hp_growth": character.hp_growth,
            "str_growth": character.str_growth,
            "mag_growth": character.mag_growth,
            "skl_growth": character.skl_growth,
            "spd_growth": character.spd_growth,
            "lck_growth": character.lck_growth,
            "defense_growth": character.defense_growth,
            "res_growth": character.res_growth,
        }
