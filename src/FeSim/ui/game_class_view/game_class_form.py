from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
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
        self.setFixedWidth(280)
        self._editing_id: int | None = None
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)

        title = QLabel("Ajouter une classe")
        title.setObjectName("titleLabel")
        self._title_label = title
        root.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.game_edit = QLineEdit()
        form.addRow("Jeu :", self.game_edit)

        self.class_edit = QLineEdit()
        form.addRow("Classe :", self.class_edit)

        # Promotion stats
        for s in self.STAT_FIELDS:
            setattr(self, f"promo_{s}_edit", QLineEdit("0"))
            form.addRow(f"Promo {s.upper()} +(x) :", getattr(self, f"promo_{s}_edit"))

        root.addLayout(form)

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

        root.addStretch()

    def reset(self):
        self._editing_id = None
        self._title_label.setText("Ajouter une classe")
        self.game_edit.clear()
        self.class_edit.clear()
        for s in self.STAT_FIELDS:
            getattr(self, f"promo_{s}_edit").setText("0")

    def load(self, data: dict):
        self._editing_id = data.get("id")
        self._title_label.setText(f"Modifier : {data.get('class_name', '')}")
        self.game_edit.setText(data.get("game", ""))
        self.class_edit.setText(data.get("class_name", ""))
        for s in self.STAT_FIELDS:
            getattr(self, f"promo_{s}_edit").setText(str(data.get(f"promotion_{s}", 0)))

    def _on_save(self):
        data: dict = {
            "id": self._editing_id,
            "game": self.game_edit.text().strip(),
            "class_name": self.class_edit.text().strip(),
        }
        for s in self.STAT_FIELDS:
            data[f"promotion_{s}"] = int(
                getattr(self, f"promo_{s}_edit").text() or "0"
            )
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
        }
        for s in self.STAT_FIELDS:
            data[f"promotion_{s}"] = int(
                getattr(self, f"promo_{s}_edit").text() or "0"
            )
        return data
