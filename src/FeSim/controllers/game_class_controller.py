from PySide6.QtWidgets import QMessageBox

from FeSim.services.game_class_service import GameClassService
from FeSim.ui.confirm_dialog import confirm_delete
from FeSim.ui.game_class_view.game_class_view import GameClassView


class GameClassController:

    def __init__(self, view: GameClassView, service: GameClassService):
        self.view = view
        self.service = service
        self._editing_id: int | None = None
        self._previous_data: dict | None = None
        self._on_changed_callback = None
        self._on_form_refresh_callback = None

        self._connect_signals()
        self._refresh()

    def set_on_changed(self, callback):
        self._on_changed_callback = callback

    def set_on_form_refresh(self, callback):
        self._on_form_refresh_callback = callback

    def _notify_changed(self):
        if self._on_changed_callback is not None:
            self._on_changed_callback()
        if self._on_form_refresh_callback is not None:
            self._on_form_refresh_callback()

    def _connect_signals(self):
        self.view.add_class_btn.clicked.connect(self._on_add_class)
        self.view.edit_btn.clicked.connect(self._on_edit)
        self.view.delete_btn.clicked.connect(self._on_delete)
        self.view.form.saved.connect(self._on_save)
        self.view.form.cancelled.connect(self._on_cancel)

    # ------------------------------------------------------------------ actions
    def _on_add_class(self):
        self._editing_id = None
        self._previous_data = None
        all_classes = [self.service.to_dict(gc) for gc in self.service.get_all()]
        self.view.form.set_all_classes(all_classes)
        self.view.form.set_promotion_choices(exclude_id=None)
        self.view.show_form(editing=False)

    def _on_edit(self):
        class_id = self.view.get_selected_class_id()
        if class_id is None:
            return
        gc = self.service.get_by_id(class_id)
        if gc is None:
            return
        self._editing_id = class_id
        self._previous_data = self.service.to_dict(gc)
        self._previous_data["promotion_to_ids"] = self.service.get_promotion_to_ids(class_id)
        all_classes = [self.service.to_dict(gc) for gc in self.service.get_all()]
        self.view.form.set_all_classes(all_classes)
        self.view.form.set_promotion_choices(exclude_id=class_id)
        self.view.form.load(self._previous_data)
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
        self._previous_data = None
        self._refresh()
        self._notify_changed()

    def _on_save(self):
        data = self.view.form.get_data()
        edit_id = data.pop("id", None)

        class_changed = False

        if edit_id is not None:
            if self._previous_data is not None:
                old_game = self._previous_data.get("game", "")
                old_class = self._previous_data.get("class_name", "")
                new_game = data.get("game", "")
                new_class = data.get("class_name", "")
                class_changed = (
                    old_game != new_game or old_class != new_class
                )
            self.service.update(edit_id, data)
        else:
            self.service.create(data)
            class_changed = True

        self._editing_id = None
        self._previous_data = None
        self.view.hide_form()
        self._refresh()

        if class_changed:
            self._notify_changed()

    def _on_cancel(self):
        self._editing_id = None
        self._previous_data = None
        self.view.hide_form()

    # ------------------------------------------------------------------ helpers
    def _refresh(self):
        all_gc = self.service.get_all()
        all_dicts = [self.service.to_dict(gc) for gc in all_gc]
        self.view.set_classes(all_dicts)
        self.view.form.set_all_classes(all_dicts)
