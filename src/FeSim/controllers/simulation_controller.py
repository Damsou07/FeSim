from FeSim.services.character_service import CharacterService
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
    ):
        self.window = window
        self.view = view
        self.service = service
        self.character_service = character_service

        self._connect_signals()

    def _connect_signals(self):
        self.view.run_simulation.connect(self._on_run_simulation)

    def _on_run_simulation(self, scenario_count: int):
        char_id = self.window.get_selected_id()
        if char_id is None:
            return

        character = self.character_service.get_character(char_id)
        if character is None:
            return

        character_dict = self.character_service.to_dict(character)
        result = self.service.simulate(character_dict, scenario_count)
        self.view.display_results(result)
