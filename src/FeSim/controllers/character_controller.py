from FeSim.services.character_service import CharacterService
from FeSim.services.game_class_service import GameClassService
from FeSim.ui.confirm_dialog import confirm_delete
from FeSim.ui.main_window import MainWindow


class CharacterController:

    def __init__(
        self,
        window: MainWindow,
        service: CharacterService,
        game_class_service: GameClassService,
    ):
        self.window = window
        self.service = service
        self.game_class_service = game_class_service
        self._editing_id: int | None = None

        self._connect_signals()
        self._refresh_table()

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    def _connect_signals(self):
        self.window.add_btn.clicked.connect(self._on_add)
        self.window.edit_btn.clicked.connect(self._on_edit)
        self.window.delete_btn.clicked.connect(self._on_delete)

        self.window.form_panel.character_saved.connect(
            self._on_save
        )

        self.window.form_panel.cancelled.connect(
            self._on_cancel
        )

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _on_add(self):
        self._editing_id = None
        self._refresh_game_classes()
        self.window.show_form(editing=False)

    def _on_edit(self):
        char_id = self.window.get_selected_id()

        if char_id is None:
            return

        character = self.service.get_character(char_id)

        if character is None:
            return

        self._editing_id = char_id

        self._refresh_game_classes()
        self.window.form_panel.load_character(
            char_id,
            self.service.to_dict(character),
        )

        self.window.show_form(editing=True)

    def _on_delete(self):
        char_id = self.window.get_selected_id()

        if char_id is None:
            return

        character = self.service.get_character(char_id)

        if character is None:
            return

        if confirm_delete(self.window, character.name):
            self.service.delete_character(char_id)
            self._refresh_table()

    def _on_save(self, data: dict):
        if self._editing_id is not None:
            self.service.update_character(
                self._editing_id,
                data,
            )
        else:
            self.service.create_character(data)

        self._editing_id = None

        self.window.hide_form()
        self._refresh_table()

    def _on_cancel(self):
        self._editing_id = None
        self.window.hide_form()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _refresh_game_classes(self):
        all_gc = self.game_class_service.get_all()
        gc_dicts = [self.game_class_service.to_dict(gc) for gc in all_gc]
        self.window.form_panel.set_game_classes(gc_dicts)

    def _refresh_table(self):
        characters = self.service.get_all_characters()

        rows = [
            self.service.to_dict(character)
            for character in characters
        ]

        self.window.load_characters(rows)

