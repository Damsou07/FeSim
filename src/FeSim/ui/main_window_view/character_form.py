from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class CharacterForm(QWidget):
    """Left-side panel form for adding / editing a character."""

    character_saved = Signal(dict)
    cancelled = Signal()

    STAT_FIELDS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(380)
        self._editing_id: int | None = None
        self._build_ui()

    # ------------------------------------------------------------------ ui
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)

        title = QLabel("Nouveau personnage")
        title.setObjectName("titleLabel")
        root.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        form = QFormLayout(container)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_edit = QLineEdit()
        form.addRow("Nom :", self.name_edit)

        self.level_edit = QLineEdit("1")
        form.addRow("Niveau :", self.level_edit)

        self.game_class_combo = QComboBox()
        self.game_class_combo.setMinimumWidth(200)
        form.addRow("Classe :", self.game_class_combo)

        # --- Base stats ---
        stats_group = QGroupBox("Stats")
        stats_form = QFormLayout(stats_group)
        self.stat_edits: dict[str, QLineEdit] = {}
        for s in self.STAT_FIELDS:
            e = QLineEdit("0")
            self.stat_edits[s] = e
            stats_form.addRow(f"{s.upper()} :", e)
        form.addRow(stats_group)

        # --- Growth rates ---
        growth_group = QGroupBox("Growth Rates (%)")
        growth_form = QFormLayout(growth_group)
        self.growth_edits: dict[str, QLineEdit] = {}
        for s in self.STAT_FIELDS:
            e = QLineEdit("0")
            self.growth_edits[s] = e
            growth_form.addRow(f"{s.upper()} :", e)
        form.addRow(growth_group)

        scroll.setWidget(container)
        root.addWidget(scroll, 1)

        # --- Buttons ---
        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.cancelled.emit)
        btn_row.addWidget(self.cancel_btn)
        root.addLayout(btn_row)

    # ------------------------------------------------------------------ public api
    def set_game_classes(self, game_classes: list[dict]):
        self.game_class_combo.clear()
        self.game_class_combo.addItem("-- Sélectionner une classe --", None)
        for gc in game_classes:
            display = f"{gc['game']} – {gc['class_name']}"
            self.game_class_combo.addItem(display, gc["id"])

    # ------------------------------------------------------------------ helpers
    def reset(self):
        self._editing_id = None
        self.name_edit.clear()
        self.level_edit.setText("1")
        if self.game_class_combo.count() > 0:
            self.game_class_combo.setCurrentIndex(0)
        for e in self.stat_edits.values():
            e.setText("0")
        for e in self.growth_edits.values():
            e.setText("0")

    def load_character(self, char_id: int, data: dict):
        self._editing_id = char_id
        self.name_edit.setText(data.get("name", ""))
        self.level_edit.setText(str(data.get("level", 1)))
        
        game_class_id = data.get("game_class_id")
        if game_class_id is not None:
            for i in range(self.game_class_combo.count()):
                if self.game_class_combo.itemData(i) == game_class_id:
                    self.game_class_combo.setCurrentIndex(i)
                    break
        
        for s in self.STAT_FIELDS:
            self.stat_edits[s].setText(str(data.get(s, 0)))
            self.growth_edits[s].setText(str(data.get(f"{s}_growth", 0)))

    # ------------------------------------------------------------------ private
    def _on_save(self):
        game_class_id = self.game_class_combo.currentData()
        
        if game_class_id is None:
            return
        
        data: dict = {
            "name": self.name_edit.text().strip(),
            "level": int(self.level_edit.text() or "1"),
            "game_class_id": game_class_id,
        }
        for s in self.STAT_FIELDS:
            data[s] = int(self.stat_edits[s].text() or "0")
            data[f"{s}_growth"] = int(self.growth_edits[s].text() or "0")

        if not data["name"]:
            return

        self.character_saved.emit(data)
