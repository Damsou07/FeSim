from PySide6.QtWidgets import QMessageBox

from FeSim.services.character_service import CharacterService
from FeSim.services.game_class_service import GameClassService
from FeSim.services.simulation_service import SimulationService
from FeSim.ui.simulation_view.simulation_view import SimulationView
from FeSim.ui.main_window_view.main_window import MainWindow


STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]


class SimulationController:

    def __init__(
        self,
        window: MainWindow,
        view: SimulationView,
        service: SimulationService,
        character_service: CharacterService,
        game_class_service: GameClassService,
    ):
        self.window = window
        self.view = view
        self.service = service
        self.character_service = character_service
        self.game_class_service = game_class_service
        self._current_character: dict | None = None
        self._promotions: list[dict] = []
        self._scenario_count: int = 1000

        self._connect_signals()

    def _connect_signals(self):
        self.view.run_simulation.connect(self._on_run_simulation)
        self.view.promo_combo.currentIndexChanged.connect(self._on_promo_changed)

    def _on_promo_changed(self, index: int):
        if index >= 0 and self._current_character is not None:
            self._run_simulation(self._scenario_count)

    def _on_run_simulation(self, scenario_count: int):
        self._scenario_count = scenario_count
        char_id = self.window.get_selected_id()
        if char_id is None:
            return

        character = self.character_service.get_character(char_id)
        if character is None:
            return

        self._current_character = self.character_service.to_dict(character)

        # Get the character's game class
        game_class = self.game_class_service.get_by_id(character.game_class_id)
        if game_class is None:
            return

        is_post_promo = game_class.level_class == "post promotion"

        if is_post_promo:
            # Post-promotion: only level 20 table
            self.view.set_post_promo_mode(True)
            result = self.service.simulate(self._current_character, scenario_count)
            self.view.display_results(result, post_promo_result=None)
        else:
            # Pre-promotion: check if promotions exist
            to_ids = self.game_class_service.get_promotion_to_ids(game_class.id)
            self._promotions = []
            for pid in to_ids:
                promo_gc = self.game_class_service.get_by_id(pid)
                if promo_gc:
                    self._promotions.append(self.game_class_service.to_dict(promo_gc))

            if not self._promotions:
                QMessageBox.warning(
                    self.view,
                    "Aucune promotion",
                    "Cette classe pré-promotion n'a pas de promotion associée. "
                    "Veuillez d'abord créer une promotion dans la gestion des classes."
                )
                return

            self.view.set_post_promo_mode(False)
            self.view.set_promotion_choices(self._promotions)

            # Run level 20 simulation
            self._run_simulation(scenario_count)

    def _run_simulation(self, scenario_count: int):
        if self._current_character is None:
            return

        result = self.service.simulate(self._current_character, scenario_count)

        # Run post-promotion simulation if a promotion is selected
        post_promo_result = None
        if self._promotions:
            promo_id = self.view.get_selected_promo_id()
            promo = None
            for p in self._promotions:
                if p["id"] == promo_id:
                    promo = p
                    break
            if promo is None:
                promo = self._promotions[0]

            bonuses = {
                "hp": promo.get("promotion_hp", 0),
                "str": promo.get("promotion_str", 0),
                "mag": promo.get("promotion_mag", 0),
                "skl": promo.get("promotion_skl", 0),
                "spd": promo.get("promotion_spd", 0),
                "lck": promo.get("promotion_lck", 0),
                "defense": promo.get("promotion_def", 0),
                "res": promo.get("promotion_res", 0),
            }
            post_promo_result = self.service.simulate_post_promotion(
                self._current_character, bonuses, scenario_count
            )

        self.view.display_results(result, post_promo_result=post_promo_result)
