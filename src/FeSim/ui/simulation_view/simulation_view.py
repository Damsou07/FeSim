from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from FeSim.ui.matrix_cell_delegate import MatrixCellDelegate
from FeSim.ui.simulation_view.score_chart_view import ScoreChartView


STAT_LABELS = ["HP", "STR", "MAG", "SKL", "SPD", "LCK", "DEF", "RES"]
STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]

CAP_BG = QColor("#1e7a3a")
CAP_FG = QColor("#ffffff")
PROMO_BG = QColor("#D9602C")
PROMO_FG = QColor("#ffffff")
ROW_BG = QColor("#12141c")
ROW_ALT_BG = QColor("#161820")
STAT_COL_BG = QColor("#1a1e28")

_MATRIX_DELEGATE = MatrixCellDelegate()


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
            "Simulez l'évolution des statistiques jusqu'au plus au niveau possible "
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
        self.scenario_count.setMaximum(10000)
        self.scenario_count.setSingleStep(10)
        self.scenario_count.setValue(50)
        self.scenario_count.setFixedWidth(100)
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

        # ── Progress bar ─────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Calcul de la simulation... %p%")
        self.progress_bar.setVisible(False)
        root_layout.addWidget(self.progress_bar)

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

        self.score_chart = ScoreChartView()
        self.results_layout.addWidget(self.score_chart)

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

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(title_text)
        label.setObjectName("tableTitle")
        header_layout.addWidget(label)

        header_layout.addStretch()

        score_label = QLabel("Score : --")
        score_label.setObjectName("matrixScoreLabel")
        header_layout.addWidget(score_label)

        layout.addLayout(header_layout)

        matrix_row = QWidget()
        matrix_row_layout = QHBoxLayout(matrix_row)
        matrix_row_layout.setContentsMargins(0, 0, 0, 0)
        matrix_row_layout.setSpacing(0)

        stat_table = QTableWidget()
        stat_table.setObjectName("matrixStatTable")
        stat_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        stat_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        stat_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        stat_table.verticalHeader().setVisible(False)
        stat_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        stat_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        stat_table.setShowGrid(True)
        stat_table.setMouseTracking(False)
        stat_table.setItemDelegate(_MATRIX_DELEGATE)

        h_scroll = QScrollArea()
        h_scroll.setObjectName("matrixScroll")
        h_scroll.setWidgetResizable(False)
        h_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        h_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        h_scroll.setFrameShape(QFrame.Shape.NoFrame)

        data_table = QTableWidget()
        data_table.setObjectName("matrixTable")
        data_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        data_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        data_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        data_table.verticalHeader().setVisible(False)
        data_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        data_table.setShowGrid(True)
        data_table.setMouseTracking(False)
        data_table.setItemDelegate(_MATRIX_DELEGATE)

        h_scroll.setWidget(data_table)
        matrix_row_layout.addWidget(stat_table)
        matrix_row_layout.addWidget(h_scroll, 1)
        layout.addWidget(matrix_row)

        card._stat_table = stat_table
        card._table = data_table
        card._h_scroll = h_scroll
        card._score_label = score_label
        return card

    def _on_run_clicked(self):
        self.run_simulation.emit(self.scenario_count.value())

    def show_progress(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.run_btn.setEnabled(False)

    def set_progress(self, value: int):
        self.progress_bar.setValue(value)

    def hide_progress(self):
        self.progress_bar.setVisible(False)
        self.run_btn.setEnabled(True)

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
            f"{'Avec Promotion' if result['is_pre_promo'] else 'Sans promotion'}  ·  "
            f"{result['scenario_count']}&nbsp;scénarios"
        )

        self._fill_matrix_table(
            self.table_avg,
            self.table_avg._stat_table,
            self.table_avg._table,
            self.table_avg._h_scroll,
            columns,
            result["avg_matrix"],
            result["score_average"],
            is_pre_promo,
            column_caps,
        )
        self._fill_matrix_table(
            self.table_best,
            self.table_best._stat_table,
            self.table_best._table,
            self.table_best._h_scroll,
            columns,
            result["best_matrix"],
            result["score_best"],
            is_pre_promo,
            column_caps,
        )
        self._fill_matrix_table(
            self.table_worst,
            self.table_worst._stat_table,
            self.table_worst._table,
            self.table_worst._h_scroll,
            columns,
            result["worst_matrix"],
            result["score_worst"],
            is_pre_promo,
            column_caps,
        )

        self.score_chart.set_data(
            columns,
            result.get("score_avg_curve", []),
            result.get("score_best_curve", []),
            result.get("score_worst_curve", []),
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
        card: QWidget,
        stat_table: QTableWidget,
        data_table: QTableWidget,
        h_scroll: QScrollArea,
        columns: list[str],
        matrix: dict,
        score: float,
        is_pre_promo: bool,
        column_caps: list[dict],
    ):
        if hasattr(card, "_score_label"):
            card._score_label.setText(f"Score : {score:.1f}")
        stat_table.setRowCount(len(STAT_KEYS))
        stat_table.setColumnCount(1)
        stat_table.setHorizontalHeaderLabels(["Stat"])

        data_table.setRowCount(len(STAT_KEYS))
        data_table.setColumnCount(len(columns))
        data_table.setHorizontalHeaderLabels(columns)

        promo_col = columns.index("↑") if is_pre_promo else -1

        for row, key in enumerate(STAT_KEYS):
            stat_item = QTableWidgetItem(STAT_LABELS[row])
            stat_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            font = stat_item.font()
            font.setBold(True)
            stat_item.setFont(font)
            stat_item.setBackground(QBrush(STAT_COL_BG))
            stat_item.setForeground(QBrush(QColor("#c0c8dc")))
            stat_table.setItem(row, 0, stat_item)

            values = matrix[key]
            cap_for_stat_cols = [caps.get(key, 0) for caps in column_caps]
            row_bg = ROW_ALT_BG if row % 2 else ROW_BG

            for col_idx, val in enumerate(values):
                display_val = int(val)
                item = QTableWidgetItem(str(display_val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if display_val == cap_for_stat_cols[col_idx]:
                    item.setBackground(QBrush(CAP_BG))
                    item.setForeground(QBrush(CAP_FG))
                elif is_pre_promo and col_idx == promo_col:
                    item.setBackground(QBrush(PROMO_BG))
                    item.setForeground(QBrush(PROMO_FG))
                else:
                    item.setBackground(QBrush(row_bg))
                    item.setForeground(QBrush(QColor("#d0d0da")))

                data_table.setItem(row, col_idx, item)

        stat_header = stat_table.horizontalHeader()
        stat_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        data_header = data_table.horizontalHeader()
        for col in range(len(columns)):
            data_header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self._size_matrix_tables(stat_table, data_table, h_scroll)

    def _size_matrix_tables(
        self, stat_table: QTableWidget, data_table: QTableWidget, h_scroll: QScrollArea
    ):
        """Size tables to show all rows; stat column fixed, data columns scroll horizontally."""
        stat_table.resizeColumnsToContents()
        data_table.resizeColumnsToContents()
        stat_table.resizeRowsToContents()
        data_table.resizeRowsToContents()

        header_height = max(
            stat_table.horizontalHeader().height(),
            data_table.horizontalHeader().height(),
        )
        stat_table.horizontalHeader().setFixedHeight(header_height)
        data_table.horizontalHeader().setFixedHeight(header_height)

        for row in range(stat_table.rowCount()):
            row_height = max(stat_table.rowHeight(row), data_table.rowHeight(row))
            stat_table.setRowHeight(row, row_height)
            data_table.setRowHeight(row, row_height)

        rows_height = sum(stat_table.rowHeight(row) for row in range(stat_table.rowCount()))
        table_height = header_height + rows_height + stat_table.frameWidth() * 2

        stat_width = stat_table.frameWidth() * 2 + stat_table.columnWidth(0)
        stat_table.setFixedSize(stat_width, table_height)

        data_width = data_table.frameWidth() * 2
        for col in range(data_table.columnCount()):
            data_width += data_table.columnWidth(col)
        data_table.setFixedSize(data_width, table_height)

        h_scroll.setMinimumHeight(table_height)
        h_scroll.setMaximumHeight(table_height)
