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
        self.results_layout.setSpacing(10)

        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel")
        self.results_layout.addWidget(self.info_label)

        # Matrix table
        self.matrix_table = QTableWidget()
        self.matrix_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.matrix_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.matrix_table.verticalHeader().setVisible(False)
        self.results_layout.addWidget(self.matrix_table, 1)

        scroll.setWidget(self.results_container)
        root_layout.addWidget(scroll, 1)

        self.results_container.setVisible(False)

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

    def display_matrix(self, result: dict):
        columns = result["columns"]
        matrix = result["matrix"]
        is_pre_promo = result["is_pre_promo"]

        self.info_label.setText(
            f"<b>{result['character_name']}</b>  ·  "
            f"Nv.{result['start_level']} → Nv.{result['target_level']}  ·  "
            f"{result['scenario_count']} scénarios"
        )

        # Setup table: rows = stats, cols = level columns + stat label column
        num_cols = len(columns) + 1  # +1 for stat name column
        self.matrix_table.setRowCount(len(STAT_KEYS))
        self.matrix_table.setColumnCount(num_cols)

        # Headers
        headers = ["Stat"] + columns
        self.matrix_table.setHorizontalHeaderLabels(headers)

        # Fill data
        for row, key in enumerate(STAT_KEYS):
            # Stat name
            stat_item = QTableWidgetItem(STAT_LABELS[row])
            stat_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            font = stat_item.font()
            font.setBold(True)
            stat_item.setFont(font)
            self.matrix_table.setItem(row, 0, stat_item)

            # Values
            values = matrix[key]
            for col_idx, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Highlight promotion column
                if is_pre_promo and col_idx == len(columns) // 2:
                    item.setBackground(Qt.GlobalColor.darkYellow)
                    item.setForeground(Qt.GlobalColor.white)

                self.matrix_table.setItem(row, col_idx + 1, item)

        # Resize
        header = self.matrix_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, num_cols):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self.results_container.setVisible(True)
