from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from FeSim.ui.glow_delegate import GlowingRowDelegate


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
            form.addRow(f"Promo {s.upper()} :", getattr(self, f"promo_{s}_edit"))

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


class GameClassView(QWidget):
    """Full-screen view for managing games and their classes."""

    back_requested = Signal()

    CLASS_TABLE_COLS = [
        "ID", "Classe",
        "Promo HP", "Promo STR", "Promo MAG", "Promo SKL",
        "Promo SPD", "Promo LCK", "Promo DEF", "Promo RES",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_classes: list[dict] = []
        self._build_ui()

    # ------------------------------------------------------------------ ui
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Buttons row ─────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(8, 6, 8, 6)

        self.add_game_btn = QPushButton("+ Ajouter un jeu")
        self.add_game_btn.setObjectName("addBtn")
        self.add_game_btn.setFixedWidth(160)
        btn_row.addWidget(self.add_game_btn)

        self.add_class_btn = QPushButton("+ Ajouter une classe")
        self.add_class_btn.setObjectName("addBtn")
        self.add_class_btn.setFixedWidth(180)
        self.add_class_btn.setEnabled(False)
        btn_row.addWidget(self.add_class_btn)

        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setFixedWidth(100)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setFixedWidth(100)
        self.delete_btn.setEnabled(False)
        btn_row.addWidget(self.delete_btn)

        btn_row.addStretch()
        root.addLayout(btn_row)

        # ── Splitter: game list | classes table + form ──────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)
        root.addWidget(splitter, 1)

        # Left: game list
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(4, 0, 4, 4)
        lbl = QLabel("Jeux")
        lbl.setObjectName("sectionLabel")
        left_layout.addWidget(lbl)

        self.game_list = QListWidget()
        self.game_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.game_list.currentRowChanged.connect(self._on_game_selected)
        left_layout.addWidget(self.game_list, 1)
        splitter.addWidget(left)

        # Right: classes table + inline form
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(4, 0, 4, 4)

        self.class_table = QTableWidget(0, len(self.CLASS_TABLE_COLS))
        self.class_table.setHorizontalHeaderLabels(self.CLASS_TABLE_COLS)
        self.class_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.class_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.class_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.class_table.verticalHeader().setVisible(False)
        self.class_table.setItemDelegate(GlowingRowDelegate(self.class_table))

        hdr = self.class_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for c in range(2, len(self.CLASS_TABLE_COLS)):
            hdr.setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)

        self.class_table.selectionModel().selectionChanged.connect(
            self._on_class_selected
        )
        right_layout.addWidget(self.class_table, 1)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # ── Inline form (hidden by default) ─────────────────────────
        self.form = GameClassForm()
        self.form.setVisible(False)
        splitter.addWidget(self.form)

    # ------------------------------------------------------------------ public api
    def set_classes(self, classes: list[dict]):
        self._all_classes = classes
        self._refresh_game_list()

    def get_selected_game(self) -> str | None:
        items = self.game_list.selectedItems()
        return items[0].text() if items else None

    def get_selected_class_id(self) -> int | None:
        rows = self.class_table.selectionModel().selectedRows()
        if not rows:
            return None
        return int(self.class_table.item(rows[0].row(), 0).text())

    def show_form(self, editing: bool = False):
        self.form.setVisible(True)
        if not editing:
            self.form.reset()

    def hide_form(self):
        self.form.setVisible(False)

    # ------------------------------------------------------------------ private
    def _refresh_game_list(self):
        current = self.get_selected_game()
        games = sorted({c["game"] for c in self._all_classes if c.get("game")})
        self.game_list.clear()
        for g in games:
            self.game_list.addItem(g)
        # restore selection
        if current:
            matches = self.game_list.findItems(current, Qt.MatchFlag.MatchExactly)
            if matches:
                self.game_list.setCurrentItem(matches[0])

    def _refresh_class_table(self, game: str | None):
        self.class_table.setRowCount(0)
        if game is None:
            return
        for c in self._all_classes:
            if c["game"] != game:
                continue
            row = self.class_table.rowCount()
            self.class_table.insertRow(row)
            keys = [
                "id", "class_name",
                "promotion_hp", "promotion_str", "promotion_mag", "promotion_skl",
                "promotion_spd", "promotion_lck", "promotion_def", "promotion_res",
            ]
            for col, key in enumerate(keys):
                val = c.get(key, "")
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.class_table.setItem(row, col, item)

    def _on_game_selected(self):
        game = self.get_selected_game()
        self._refresh_class_table(game)
        self.add_class_btn.setEnabled(game is not None)
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

    def _on_class_selected(self):
        has = len(self.class_table.selectionModel().selectedRows()) > 0
        self.edit_btn.setEnabled(has)
        self.delete_btn.setEnabled(has)
