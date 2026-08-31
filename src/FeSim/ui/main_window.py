from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from FeSim.ui.character_form import CharacterForm
from FeSim.ui.confirm_dialog import confirm_delete


class MainWindow(QMainWindow):
    """Main window containing the spreadsheet and the character form."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeSim – Fire Emblem Simulator")
        self.resize(1100, 600)

        self._columns = [
            "ID",
            "Nom",
            "Nv.",
            "Jeu",
            "Classe",
            "HP",
            "STR",
            "MAG",
            "SKL",
            "SPD",
            "LCK",
            "DEF",
            "RES",
            "HP%",
            "STR%",
            "MAG%",
            "SKL%",
            "SPD%",
            "LCK%",
            "DEF%",
            "RES%",
        ]

        self._build_ui()

    # ------------------------------------------------------------------ ui
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        root_layout.addWidget(splitter)

        # --- Left panel: character form (hidden by default) ---
        self.form_panel = CharacterForm()
        self.form_panel.setVisible(False)
        splitter.addWidget(self.form_panel)

        # --- Right panel: table + buttons ---
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(4, 4, 4, 4)

        # Top buttons
        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("+ Ajouter")
        self.add_btn.setFixedWidth(120)
        btn_row.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setFixedWidth(120)
        self.edit_btn.setEnabled(False)
        btn_row.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.setFixedWidth(120)
        self.delete_btn.setEnabled(False)
        btn_row.addWidget(self.delete_btn)

        btn_row.addStretch()
        right_layout.addLayout(btn_row)

        # Table
        self.table = QTableWidget(0, len(self._columns))
        self.table.setHorizontalHeaderLabels(self._columns)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for col in range(2, len(self._columns)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self.table.selectionModel().selectionChanged.connect(
            self._on_selection_changed
        )
        right_layout.addWidget(self.table, 1)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

    # ------------------------------------------------------------------ public api
    def load_characters(self, rows: list[dict]):
        self.table.setRowCount(0)
        for row_data in rows:
            self._add_row(row_data)

    def add_character_row(self, row_data: dict):
        self._add_row(row_data)

    def update_character_row(self, row_data: dict):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        row = rows[0].row()
        self._fill_row(row, row_data)

    def get_selected_id(self) -> int | None:
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return None
        return int(self.table.item(rows[0].row(), 0).text())

    def show_form(self, editing: bool = False):
        self.form_panel.setVisible(True)
        if not editing:
            self.form_panel.reset()

    def hide_form(self):
        self.form_panel.setVisible(False)

    # ------------------------------------------------------------------ private
    def _add_row(self, data: dict):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._fill_row(row, data)

    def _fill_row(self, row: int, data: dict):
        keys = [
            "id",
            "name",
            "level",
            "game",
            "class_name",
            "hp",
            "str",
            "mag",
            "skl",
            "spd",
            "lck",
            "defense",
            "res",
            "hp_growth",
            "str_growth",
            "mag_growth",
            "skl_growth",
            "spd_growth",
            "lck_growth",
            "defense_growth",
            "res_growth",
        ]
        for col, key in enumerate(keys):
            val = data.get(key, "")
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, col, item)

    def _on_selection_changed(self):
        has = len(self.table.selectionModel().selectedRows()) > 0
        self.edit_btn.setEnabled(has)
        self.delete_btn.setEnabled(has)
