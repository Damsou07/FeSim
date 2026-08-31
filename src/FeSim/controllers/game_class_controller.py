from FeSim.services.game_class_service import GameClassService
from FeSim.ui.confirm_dialog import confirm_delete
from FeSim.ui.game_class_view import GameClassView
from PySide6.QtWidgets import QMessageBox


class GameClassController:
    def __init__(self, view: GameClassView, service: GameClassService):
        self.view = view
        self.service = service
        self._editing_id: int | None = None

        self._connect_signals()
        self._refresh()

    def _connect_signals(self):
        self.view.add_class_btn.clicked.connect(self._on_add_class)
        self.view.edit_btn.clicked.connect(self._on_edit)
        self.view.delete_btn.clicked.connect(self._on_delete)
        self.view.form.saved.connect(self._on_save)
        self.view.form.cancelled.connect(self._on_cancel)

    # ------------------------------------------------------------------ actions
    def _on_add_class(self):
        game = self.view.get_selected_game()
        self.view.show_form(editing=False)
        if game:
            self.view.form.game_edit.setText(game)

    def _on_edit(self):
        class_id = self.view.get_selected_class_id()
        if class_id is None:
            return
        gc = self.service.get_by_id(class_id)
        if gc is None:
            return
        self._editing_id = class_id
        self.view.form.load(self.service.to_dict(gc))
        self.view.show_form(editing=True)

    def _on_delete(self):
        class_id = self.view.get_selected_class_id()
        if class_id is None:
            return
        game_class = self.service.get_by_id(class_id)
        if game_class is None:
            return
        if not confirm_delete(
            self.view,
            f"{game_class.game} – {game_class.class_name}",
        ):
            return
        try:
            self.service.delete(class_id)

        except ValueError as error:
            QMessageBox.warning(
                self.view,
                "Suppression impossible",
                str(error),
            )
            return
        self._editing_id = None
        self._refresh()

    def _on_save(self):
        data = self.view.form.get_data()
        edit_id = data.pop("id", None)

        if edit_id is not None:
            self.service.update(edit_id, data)
        else:
            self.service.create(data)

        self._editing_id = None
        self.view.hide_form()
        self._refresh()

    def _on_cancel(self):
        self._editing_id = None
        self.view.hide_form()

    # ------------------------------------------------------------------ helpers
    def _refresh(self):
        all_gc = self.service.get_all()
        self.view.set_classes([self.service.to_dict(gc) for gc in all_gc])
