from PySide6.QtWidgets import QApplication, QMessageBox

from FeSim.services.character_service import CharacterService
from FeSim.services.game_class_service import GameClassService
from FeSim.services.simulation_service import SimulationService
from FeSim.ui.simulation_view.simulation_view import SimulationView
from FeSim.ui.main_window_view.main_window import MainWindow


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
        self._game_class = None
        self._promotions: list[dict] = []
        self._scenario_count: int = 1000

        self._connect_signals()

    def _connect_signals(self):
        self.view.run_simulation.connect(self._on_run_simulation)

    def prepare_view(self):
        """Prepare promotion choices and character data when entering the simulation view."""
        char_id = self.window.get_selected_id()
        if char_id is None:
            return

        character = self.character_service.get_character(char_id)
        if character is None:
            return

        self._current_character = self.character_service.to_dict(character)
        self._game_class = self.game_class_service.get_by_id(character.game_class_id)
        if self._game_class is None:
            return

        is_post_promo = self._game_class.level_class == "post promotion"

        if is_post_promo:
            self.view.set_post_promo_mode(True)
            self._promotions = []
        else:
            to_ids = self.game_class_service.get_promotion_to_ids(self._game_class.id)
            self._promotions = []
            for pid in to_ids:
                promo_gc = self.game_class_service.get_by_id(pid)
                if promo_gc:
                    self._promotions.append(self.game_class_service.to_dict(promo_gc))

            self.view.set_post_promo_mode(False)
            self.view.set_promotion_choices(self._promotions)

    def _on_run_simulation(self, scenario_count: int):
        self._scenario_count = scenario_count
        char_id = self.window.get_selected_id()
        if char_id is None:
            return

        character = self.character_service.get_character(char_id)
        if character is None:
            return

        self._current_character = self.character_service.to_dict(character)
        self._game_class = self.game_class_service.get_by_id(character.game_class_id)
        if self._game_class is None:
            return

        is_post_promo = self._game_class.level_class == "post promotion"

        if not is_post_promo:
            if not self._promotions:
                to_ids = self.game_class_service.get_promotion_to_ids(self._game_class.id)
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

        # Show loading progress bar
        self.view.show_progress()
        self.view.set_progress(20)
        QApplication.processEvents()

        self.view.set_progress(50)
        QApplication.processEvents()

        self._run_simulation()

        self.view.set_progress(100)
        QApplication.processEvents()

        self.view.hide_progress()

    def _run_simulation(self):
        if self._current_character is None:
            return

        is_pre_promo = self._game_class and self._game_class.level_class == "pre promotion"

        # Caps for phase 1 (current class)
        caps_phase1 = self._get_caps_from_gc(self._game_class)

        promotion_bonuses = None
        caps_phase2 = None

        if is_pre_promo and self._promotions:
            promo_id = self.view.get_selected_promo_id()
            promo = None
            for p in self._promotions:
                if p["id"] == promo_id:
                    promo = p
                    break
            if promo is None and self._promotions:
                promo = self._promotions[0]

            if promo:
                promotion_bonuses = {
                    "hp": promo.get("promotion_hp", 0),
                    "str": promo.get("promotion_str", 0),
                    "mag": promo.get("promotion_mag", 0),
                    "skl": promo.get("promotion_skl", 0),
                    "spd": promo.get("promotion_spd", 0),
                    "lck": promo.get("promotion_lck", 0),
                    "defense": promo.get("promotion_def", 0),
                    "res": promo.get("promotion_res", 0),
                }
                # Caps for phase 2 (promoted class)
                promo_gc = self.game_class_service.get_by_id(promo["id"])
                caps_phase2 = self._get_caps_from_gc(promo_gc)

        result = self.service.simulate_matrix(
            self._current_character,
            self._scenario_count,
            promotion_bonuses,
            caps_phase1,
            caps_phase2,
        )
        result["caps_phase1"] = caps_phase1
        result["caps_phase2"] = caps_phase2 or caps_phase1
        self.view.display_matrices(result)

    def _get_caps_from_gc(self, game_class) -> dict:
        """Extract caps dict from a GameClass entity or None."""
        if game_class is None:
            return {key: 999 for key in ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]}
        return {
            "hp": game_class.cap_hp,
            "str": game_class.cap_str,
            "mag": game_class.cap_mag,
            "skl": game_class.cap_skl,
            "spd": game_class.cap_spd,
            "lck": game_class.cap_lck,
            "defense": game_class.cap_def,
            "res": game_class.cap_res,
        }
