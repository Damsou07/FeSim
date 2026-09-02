from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


STAT_LABELS = ["HP", "STR", "MAG", "SKL", "SPD", "LCK", "DEF", "RES"]
STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]

CAP_BG = QColor("#1a5c32")
CAP_FG = QColor("#c8f5d4")
PROMO_BG = QColor("#7a6520")
PROMO_FG = QColor("#fff8dc")


class SimulationView(QWidget):

    run_simulation = Signal(int)

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        title = QLabel("Simulation")
        title.setObjectName("pageTitle")
        root_layout.addWidget(title)

        subtitle = QLabel(
            "Simulez l'évolution des statistiques jusqu'au niveau 20 "
            "sur plusieurs scénarios aléatoires."
        )
        subtitle.setObjectName("pageSubtitle")
        root_layout.addWidget(subtitle)

        # ── Controls panel ──────────────────────────────────────────
        controls_panel = QFrame()
        controls_panel.setObjectName("simulationControls")
        controls_layout = QHBoxLayout(controls_panel)
        controls_layout.setContentsMargins(16, 12, 16, 12)
        controls_layout.setSpacing(16)

        scenario_label = QLabel("Scénarios")
        scenario_label.setObjectName("controlLabel")
        controls_layout.addWidget(scenario_label)

        self.scenario_count = QSpinBox()
        self.scenario_count.setMinimum(1)
        self.scenario_count.setMaximum(1000)
        self.scenario_count.setValue(50)
        self.scenario_count.setFixedWidth(90)
        controls_layout.addWidget(self.scenario_count)

        self.promo_label = QLabel("Promotion")
        self.promo_label.setObjectName("controlLabel")
        controls_layout.addWidget(self.promo_label)
        self.promo_combo = QComboBox()
        self.promo_combo.setMinimumWidth(280)
        controls_layout.addWidget(self.promo_combo)

        controls_layout.addStretch()

        self.run_btn = QPushButton("Lancer la simulation")
        self.run_btn.setObjectName("simulationBtn")
        self.run_btn.clicked.connect(self._on_run_clicked)
        controls_layout.addWidget(self.run_btn)

        root_layout.addWidget(controls_panel)

        # ── Scrollable results area (vertical scroll on page) ───────
        scroll = QScrollArea()
        scroll.setObjectName("simulationScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(0, 4, 0, 8)
        self.results_layout.setSpacing(20)

        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel")
        self.info_label.setWordWrap(True)
        self.results_layout.addWidget(self.info_label)

        self.table_avg = self._create_matrix_table("Moyenne")
        self.results_layout.addWidget(self.table_avg)

        self.table_best = self._create_matrix_table("Meilleur scénario")
        self.results_layout.addWidget(self.table_best)

        self.table_worst = self._create_matrix_table("Pire scénario")
        self.results_layout.addWidget(self.table_worst)

        self.results_layout.addStretch()

        scroll.setWidget(self.results_container)
        root_layout.addWidget(scroll, 1)

        self.results_container.setVisible(False)

    def _create_matrix_table(self, title_text: str) -> QWidget:
        card = QFrame()
        card.setObjectName("matrixCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        label = QLabel(title_text)
        label.setObjectName("tableTitle")
        layout.addWidget(label)

        h_scroll = QScrollArea()
        h_scroll.setObjectName("matrixScroll")
        h_scroll.setWidgetResizable(False)
        h_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        h_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        h_scroll.setFrameShape(QFrame.Shape.NoFrame)

        table = QTableWidget()
        table.setObjectName("matrixTable")
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setShowGrid(True)

        h_scroll.setWidget(table)
        layout.addWidget(h_scroll)

        card._table = table
        card._h_scroll = h_scroll
        return card

    def _on_run_clicked(self):
        self.run_simulation.emit(self.scenario_count.value())

    def get_selected_promo_id(self) -> int | None:
        return self.promo_combo.currentData()

    def set_promotion_choices(self, promotions: list[dict]):
        self.promo_combo.clear()
        for promo in promotions:
            display = f"{promo['game']} – {promo['class_name']}"
            self.promo_combo.addItem(display, promo["id"])
        has_promos = len(promotions) > 0
        self.promo_label.setVisible(has_promos)
        self.promo_combo.setVisible(has_promos)

    def set_post_promo_mode(self, is_post_promo: bool):
        self.promo_label.setVisible(not is_post_promo)
        self.promo_combo.setVisible(not is_post_promo)

    def display_matrices(self, result: dict):
        columns = result["columns"]
        is_pre_promo = result["is_pre_promo"]
        caps_phase1 = result.get("caps_phase1", {})
        caps_phase2 = result.get("caps_phase2", caps_phase1)
        column_caps = self._build_column_caps(columns, is_pre_promo, caps_phase1, caps_phase2)

        self.info_label.setText(
            f"<b>{result['character_name']}</b>  ·  "
            f"Nv.&nbsp;{result['start_level']} → Nv.&nbsp;{result['target_level']}  ·  "
            f"{result['scenario_count']}&nbsp;scénarios"
        )

        self._fill_matrix_table(
            self.table_avg._table,
            self.table_avg._h_scroll,
            columns,
            result["avg_matrix"],
            is_pre_promo,
            column_caps,
        )
        self._fill_matrix_table(
            self.table_best._table,
            self.table_best._h_scroll,
            columns,
            result["best_matrix"],
            is_pre_promo,
            column_caps,
        )
        self._fill_matrix_table(
            self.table_worst._table,
            self.table_worst._h_scroll,
            columns,
            result["worst_matrix"],
            is_pre_promo,
            column_caps,
        )

        self.results_container.setVisible(True)

    def _build_column_caps(
        self,
        columns: list[str],
        is_pre_promo: bool,
        caps_phase1: dict,
        caps_phase2: dict,
    ) -> list[dict]:
        promo_idx = columns.index("↑") if is_pre_promo and "↑" in columns else -1
        column_caps = []
        for col_idx in range(len(columns)):
            if is_pre_promo and promo_idx >= 0 and col_idx >= promo_idx:
                column_caps.append(caps_phase2)
            else:
                column_caps.append(caps_phase1)
        return column_caps

    def _fill_matrix_table(
        self,
        table: QTableWidget,
        h_scroll: QScrollArea,
        columns: list[str],
        matrix: dict,
        is_pre_promo: bool,
        column_caps: list[dict],
    ):
        num_cols = len(columns) + 1
        table.setRowCount(len(STAT_KEYS))
        table.setColumnCount(num_cols)
        table.setHorizontalHeaderLabels(["Stat"] + columns)

        promo_col = columns.index("↑") if is_pre_promo else -1

        for row, key in enumerate(STAT_KEYS):
            stat_item = QTableWidgetItem(STAT_LABELS[row])
            stat_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            font = stat_item.font()
            font.setBold(True)
            stat_item.setFont(font)
            table.setItem(row, 0, stat_item)

            values = matrix[key]
            cap_for_stat_cols = [caps.get(key, 0) for caps in column_caps]

            for col_idx, val in enumerate(values):
                display_val = int(val)
                item = QTableWidgetItem(str(display_val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if is_pre_promo and col_idx == promo_col:
                    item.setBackground(QBrush(PROMO_BG))
                    item.setForeground(QBrush(PROMO_FG))
                elif display_val == cap_for_stat_cols[col_idx]:
                    item.setBackground(QBrush(CAP_BG))
                    item.setForeground(QBrush(CAP_FG))

                table.setItem(row, col_idx + 1, item)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, num_cols):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self._size_table_to_content(table, h_scroll)

    def _size_table_to_content(self, table: QTableWidget, h_scroll: QScrollArea):
        """Size table to show all rows (no vertical scroll); horizontal scroll if needed."""
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        frame = table.frameWidth() * 2
        header_height = table.horizontalHeader().height()
        rows_height = sum(table.rowHeight(row) for row in range(table.rowCount()))
        table_height = header_height + rows_height + frame

        table_width = frame
        for col in range(table.columnCount()):
            table_width += table.columnWidth(col)

        table.setFixedSize(table_width, table_height)
        h_scroll.setMinimumHeight(table_height)
        h_scroll.setMaximumHeight(table_height)
