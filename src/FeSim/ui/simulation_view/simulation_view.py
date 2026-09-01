from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
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


class SimulationView(QWidget):

    run_simulation = Signal(int)

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(8, 8, 8, 8)

        title = QLabel("Simulation")
        title.setObjectName("pageTitle")
        root_layout.addWidget(title)

        # ── Controls ────────────────────────────────────────────────
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)

        scenario_label = QLabel("Nombre de scénarios :")
        controls_layout.addWidget(scenario_label)

        self.scenario_count = QSpinBox()
        self.scenario_count.setMinimum(1)
        self.scenario_count.setMaximum(10000)
        self.scenario_count.setValue(1000)
        controls_layout.addWidget(self.scenario_count)

        # Promotion chooser
        self.promo_label = QLabel("Promotion :")
        controls_layout.addWidget(self.promo_label)
        self.promo_combo = QComboBox()
        self.promo_combo.setMinimumWidth(250)
        controls_layout.addWidget(self.promo_combo)

        controls_layout.addStretch()

        self.run_btn = QPushButton("Lancer la simulation")
        self.run_btn.setObjectName("simulationBtn")
        self.run_btn.clicked.connect(self._on_run_clicked)
        controls_layout.addWidget(self.run_btn)

        root_layout.addLayout(controls_layout)

        # ── Scrollable results area ─────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(0, 10, 0, 0)
        self.results_layout.setSpacing(16)

        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel")
        self.results_layout.addWidget(self.info_label)

        # Table 1: Average
        self.table_avg = self._create_matrix_table("Moyenne")
        self.results_layout.addWidget(self.table_avg)

        # Table 2: Best scenario
        self.table_best = self._create_matrix_table("Meilleur scénario")
        self.results_layout.addWidget(self.table_best)

        # Table 3: Worst scenario
        self.table_worst = self._create_matrix_table("Pire scénario")
        self.results_layout.addWidget(self.table_worst)

        self.results_layout.addStretch()

        scroll.setWidget(self.results_container)
        root_layout.addWidget(scroll, 1)

        self.results_container.setVisible(False)

    def _create_matrix_table(self, title_text: str) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel(title_text)
        label.setObjectName("tableTitle")
        layout.addWidget(label)

        table = QTableWidget()
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.verticalHeader().setVisible(False)

        layout.addWidget(table)
        container._table = table
        return container

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

        self.info_label.setText(
            f"<b>{result['character_name']}</b>  ·  "
            f"Nv.{result['start_level']} → Nv.{result['target_level']}  ·  "
            f"{result['scenario_count']} scénarios"
        )

        self._fill_matrix_table(self.table_avg._table, columns, result["avg_matrix"], is_pre_promo)
        self._fill_matrix_table(self.table_best._table, columns, result["best_matrix"], is_pre_promo)
        self._fill_matrix_table(self.table_worst._table, columns, result["worst_matrix"], is_pre_promo)

        self.results_container.setVisible(True)

    def _fill_matrix_table(
        self, table: QTableWidget, columns: list[str], matrix: dict, is_pre_promo: bool
    ):
        num_cols = len(columns) + 1
        table.setRowCount(len(STAT_KEYS))
        table.setColumnCount(num_cols)
        table.setHorizontalHeaderLabels(["Stat"] + columns)

        promo_col = len(columns) // 2 if is_pre_promo else -1

        for row, key in enumerate(STAT_KEYS):
            stat_item = QTableWidgetItem(STAT_LABELS[row])
            stat_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            font = stat_item.font()
            font.setBold(True)
            stat_item.setFont(font)
            table.setItem(row, 0, stat_item)

            values = matrix[key]
            for col_idx, val in enumerate(values):
                item = QTableWidgetItem(str(int(val)))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if is_pre_promo and col_idx == promo_col:
                    item.setBackground(Qt.GlobalColor.darkYellow)
                    item.setForeground(Qt.GlobalColor.white)

                table.setItem(row, col_idx + 1, item)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, num_cols):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
