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
TABLE_HEADERS = ["Stat", "Base", "Min", "Max", "Moy.", "Variance"]


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

        # Promotion chooser (visible only for pre-promotion classes)
        self.promo_label = QLabel("Promotion :")
        controls_layout.addWidget(self.promo_label)
        self.promo_combo = QComboBox()
        self.promo_combo.setMinimumWidth(200)
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
        self.results_layout.setSpacing(20)

        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel")
        self.results_layout.addWidget(self.info_label)

        # Table 1: Level 20
        self.table_level20 = self._create_table("Niveau 20")
        self.results_layout.addWidget(self.table_level20)

        # Table 2: Level 1 after promotion
        self.table_post_promo = self._create_table("Niveau 1 après promotion")
        self.results_layout.addWidget(self.table_post_promo)

        # Table 3: Variance
        self.table_variance = self._create_table("Variance")
        self.results_layout.addWidget(self.table_variance)

        self.results_layout.addStretch()

        scroll.setWidget(self.results_container)
        root_layout.addWidget(scroll, 1)

        self.results_container.setVisible(False)

    def _create_table(self, title_text: str) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel(title_text)
        label.setObjectName("tableTitle")
        layout.addWidget(label)

        table = QTableWidget(0, 6)
        table.setHorizontalHeaderLabels(TABLE_HEADERS)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.verticalHeader().setVisible(False)
        table.setMaximumHeight(220)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

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
        self.table_post_promo.setVisible(not is_post_promo)

    def display_results(self, result: dict, post_promo_result: dict | None = None):
        self.info_label.setText(
            f"<b>{result['character_name']}</b>  ·  "
            f"Nv.{result['start_level']} → Nv.{result['target_level']}  ·  "
            f"{result['scenario_count']} scénarios"
        )

        # Fill level 20 table
        self._fill_table(self.table_level20._table, result)

        # Fill post-promotion table if available
        if post_promo_result:
            self._fill_table(self.table_post_promo._table, post_promo_result)
            self.table_post_promo.setVisible(True)
        else:
            self.table_post_promo.setVisible(False)

        # Fill variance table
        variance = result.get("variance_stats", {})
        base = result.get("base_stats", {})
        avg = result.get("avg_stats", {})
        mn = result.get("min_stats", {})
        mx = result.get("max_stats", {})
        self._fill_full_table(self.table_variance._table, base, mn, mx, avg, variance)

        self.results_container.setVisible(True)

    def _fill_table(self, table: QTableWidget, data: dict):
        base = data.get("base_stats", {})
        mn = data.get("min_stats", {})
        mx = data.get("max_stats", {})
        avg = data.get("avg_stats", {})
        var = data.get("variance_stats", {})

        self._fill_full_table(table, base, mn, mx, avg, var)

    def _fill_full_table(
        self, table: QTableWidget,
        base: dict, mn: dict, mx: dict, avg: dict, var: dict,
    ):
        table.setRowCount(len(STAT_KEYS))
        for row, key in enumerate(STAT_KEYS):
            stat_item = QTableWidgetItem(STAT_LABELS[row])
            stat_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            table.setItem(row, 0, stat_item)

            base_val = QTableWidgetItem(str(base.get(key, 0)))
            base_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 1, base_val)

            min_val = QTableWidgetItem(str(mn.get(key, 0)))
            min_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 2, min_val)

            max_val = QTableWidgetItem(str(mx.get(key, 0)))
            max_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 3, max_val)

            avg_val = QTableWidgetItem(str(avg.get(key, 0)))
            avg_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 4, avg_val)

            var_val = QTableWidgetItem(str(var.get(key, 0.0)))
            var_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row, 5, var_val)
