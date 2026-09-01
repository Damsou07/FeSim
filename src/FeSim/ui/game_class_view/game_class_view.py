from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from FeSim.ui.glow_delegate import GlowingRowDelegate
from FeSim.ui.game_class_view.game_class_form import GameClassForm


class GameClassView(QWidget):
    """Full-screen view for managing game classes."""

    back_requested = Signal()

    CLASS_TABLE_COLS = [
        "ID", "Jeu", "Classe",
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
        btn_row.setSpacing(12)

        self.add_class_btn = QPushButton("+ Ajouter une classe")
        self.add_class_btn.setObjectName("addBtn")
        self.add_class_btn.setFixedWidth(180)
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

        # ── Splitter: form (left) | classes table (right) ──────────
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        root.addWidget(self.splitter, 1)

        # Left: inline form (hidden by default)
        self.form = GameClassForm()
        self.form.setVisible(False)
        self.splitter.addWidget(self.form)

        # Right: classes table
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
        self.class_table.viewport().installEventFilter(self)

        hdr = self.class_table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        for c in range(3, len(self.CLASS_TABLE_COLS)):
            hdr.setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)

        self.class_table.selectionModel().selectionChanged.connect(
            self._on_class_selected
        )
        right_layout.addWidget(self.class_table, 1)

        self.splitter.addWidget(right)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

    # ------------------------------------------------------------------ public api
    def set_classes(self, classes: list[dict]):
        self._all_classes = classes
        self._refresh_class_table()

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

    def clear_selection(self):
        self.class_table.clearSelection()
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

    # ------------------------------------------------------------------ private
    def _refresh_class_table(self):
        self.class_table.setRowCount(0)
        sorted_classes = sorted(
            self._all_classes,
            key=lambda c: (c.get("game", ""), c.get("class_name", "")),
        )
        for c in sorted_classes:
            row = self.class_table.rowCount()
            self.class_table.insertRow(row)
            keys = [
                "id", "game", "class_name",
                "promotion_hp", "promotion_str", "promotion_mag", "promotion_skl",
                "promotion_spd", "promotion_lck", "promotion_def", "promotion_res",
            ]
            for col, key in enumerate(keys):
                val = c.get(key, "")
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.class_table.setItem(row, col, item)

    def _on_class_selected(self):
        has = len(self.class_table.selectionModel().selectedRows()) > 0
        self.edit_btn.setEnabled(has)
        self.delete_btn.setEnabled(has)

    def eventFilter(self, obj, event):
        if obj is self.class_table.viewport() and event.type() == QEvent.Type.MouseButtonPress:
            if isinstance(event, QMouseEvent):
                index = self.class_table.indexAt(event.position().toPoint())
                if not index.isValid():
                    self.class_table.clearSelection()
                    self.edit_btn.setEnabled(False)
                    self.delete_btn.setEnabled(False)
        return super().eventFilter(obj, event)
