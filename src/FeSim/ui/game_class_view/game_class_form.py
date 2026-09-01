from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class GameClassForm(QWidget):
    """Small inline form for adding / editing a GameClass entry."""

    saved = Signal()
    cancelled = Signal()

    STAT_FIELDS = [
        "hp", "str", "mag", "skl", "spd", "lck", "def", "res",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(340)
        self._editing_id: int | None = None
        self._all_classes: list[dict] = []
        self._promo_labels: list[QLabel] = []
        self._promo_edits: list[QLineEdit] = []
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)

        title = QLabel("Ajouter une classe")
        title.setObjectName("titleLabel")
        self._title_label = title
        root.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self._form = QFormLayout(container)
        self._form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.game_edit = QLineEdit()
        self._form.addRow("Jeu :", self.game_edit)

        self.class_edit = QLineEdit()
        self._form.addRow("Classe :", self.class_edit)

        self.level_class_edit = QComboBox()
        self.level_class_edit.addItems(["pre promotion", "post promotion"])
        self.level_class_edit.currentIndexChanged.connect(self._on_level_changed)
        self._form.addRow("Niveau :", self.level_class_edit)

        # Promotion classes selection (for pre promotion classes)
        self._promo_list_label = QLabel("Classe(s) de\npromotion :")
        self.promotion_list = QListWidget()
        self.promotion_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.promotion_list.setMaximumHeight(120)
        self._promotion_ids: list[int] = []
        self._form.addRow(self._promo_list_label, self.promotion_list)

        # Promotion stats (only for post promotion)
        self._promo_stat_labels: list[QLabel] = []
        self._promo_stat_edits: list[QLineEdit] = []
        for s in self.STAT_FIELDS:
            lbl = QLabel(f"Promo {s.upper()} +(x) :")
            edit = QLineEdit("0")
            self._promo_stat_labels.append(lbl)
            self._promo_stat_edits.append(edit)
            self._form.addRow(lbl, edit)

        # Cap stats
        for s in self.STAT_FIELDS:
            setattr(self, f"cap_{s}_edit", QLineEdit("0"))
            self._form.addRow(f"Cap {s.upper()} :", getattr(self, f"cap_{s}_edit"))

        scroll.setWidget(container)
        root.addWidget(scroll, 1)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self._on_cancel)
        btn_row.addWidget(self.cancel_btn)
        root.addLayout(btn_row)

    def _on_level_changed(self):
        is_pre = self.level_class_edit.currentText() == "pre promotion"
        # Pre promotion: show promotion list, hide promo stats
        # Post promotion: hide promotion list, show promo stats
        self._promo_list_label.setVisible(is_pre)
        self.promotion_list.setVisible(is_pre)
        for lbl, edit in zip(self._promo_stat_labels, self._promo_stat_edits):
            lbl.setVisible(not is_pre)
            edit.setVisible(not is_pre)

    def reset(self):
        self._editing_id = None
        self._title_label.setText("Ajouter une classe")
        self.game_edit.clear()
        self.class_edit.clear()
        self.level_class_edit.setCurrentIndex(0)
        self.promotion_list.clear()
        self._promotion_ids = []
        for edit in self._promo_stat_edits:
            edit.setText("0")
        for s in self.STAT_FIELDS:
            getattr(self, f"cap_{s}_edit").setText("0")
        self._on_level_changed()

    def set_all_classes(self, classes: list[dict]):
        self._all_classes = classes

    def set_promotion_choices(self, exclude_id: int | None = None):
        self.promotion_list.clear()
        self._promotion_ids = []
        for gc in self._all_classes:
            if gc.get("level_class") != "post promotion":
                continue
            if gc.get("id") == exclude_id:
                continue
            self._promotion_ids.append(gc["id"])
            display = f"{gc['game']} – {gc['class_name']}"
            self.promotion_list.addItem(display)

    def load(self, data: dict):
        self._editing_id = data.get("id")
        self._title_label.setText(f"Modifier : {data.get('class_name', '')}")
        self.game_edit.setText(data.get("game", ""))
        self.class_edit.setText(data.get("class_name", ""))
        level = data.get("level_class", "pre promotion")
        idx = self.level_class_edit.findText(level)
        if idx >= 0:
            self.level_class_edit.setCurrentIndex(idx)
        for i, s in enumerate(self.STAT_FIELDS):
            self._promo_stat_edits[i].setText(str(data.get(f"promotion_{s}", 0)))
            getattr(self, f"cap_{s}_edit").setText(str(data.get(f"cap_{s}", 0)))
        # Select promotion classes
        promo_ids = data.get("promotion_to_ids", [])
        self.promotion_list.clearSelection()
        for i, pid in enumerate(self._promotion_ids):
            if pid in promo_ids:
                self.promotion_list.item(i).setSelected(True)
        self._on_level_changed()

    def _on_save(self):
        data: dict = {
            "id": self._editing_id,
            "game": self.game_edit.text().strip(),
            "class_name": self.class_edit.text().strip(),
            "level_class": self.level_class_edit.currentText(),
        }
        for i, s in enumerate(self.STAT_FIELDS):
            data[f"promotion_{s}"] = int(
                self._promo_stat_edits[i].text() or "0"
            )
            data[f"cap_{s}"] = int(
                getattr(self, f"cap_{s}_edit").text() or "0"
            )
        # Selected promotion class IDs (only for pre promotion)
        if data["level_class"] == "pre promotion" and self._promotion_ids:
            selected_rows = self.promotion_list.selectionModel().selectedRows()
            data["promotion_to_ids"] = [
                self._promotion_ids[i.row()] for i in selected_rows
                if 0 <= i.row() < len(self._promotion_ids)
            ]
        else:
            data["promotion_to_ids"] = []
        if not data["game"] or not data["class_name"]:
            return
        self.saved.emit()

    def _on_cancel(self):
        self.reset()
        self.cancelled.emit()

    def get_data(self) -> dict:
        data: dict = {
            "id": self._editing_id,
            "game": self.game_edit.text().strip(),
            "class_name": self.class_edit.text().strip(),
            "level_class": self.level_class_edit.currentText(),
        }
        for i, s in enumerate(self.STAT_FIELDS):
            data[f"promotion_{s}"] = int(
                self._promo_stat_edits[i].text() or "0"
            )
            data[f"cap_{s}"] = int(
                getattr(self, f"cap_{s}_edit").text() or "0"
            )
        # Selected promotion class IDs (only for pre promotion)
        if data["level_class"] == "pre promotion" and self._promotion_ids:
            selected_rows = self.promotion_list.selectionModel().selectedRows()
            data["promotion_to_ids"] = [
                self._promotion_ids[i.row()] for i in selected_rows
                if 0 <= i.row() < len(self._promotion_ids)
            ]
        else:
            data["promotion_to_ids"] = []
        return data
