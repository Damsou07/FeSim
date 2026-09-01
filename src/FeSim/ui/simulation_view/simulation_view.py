from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
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

        layout = QVBoxLayout(self)

        title = QLabel("Simulation")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        scenario_layout = QHBoxLayout()

        scenario_label = QLabel("Nombre de scénarios :")

        self.scenario_count = QSpinBox()
        self.scenario_count.setMinimum(1)
        self.scenario_count.setMaximum(100000)
        self.scenario_count.setValue(1000)

        scenario_layout.addWidget(scenario_label)
        scenario_layout.addWidget(self.scenario_count)
        scenario_layout.addStretch()

        layout.addLayout(scenario_layout)

        self.run_btn = QPushButton("Lancer la simulation")
        self.run_btn.setObjectName("simulationBtn")

        self.run_btn.clicked.connect(self._on_run_clicked)

        layout.addWidget(self.run_btn)

        # ── Results area ────────────────────────────────────────────
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setContentsMargins(0, 10, 0, 0)

        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel")
        self.results_layout.addWidget(self.info_label)

        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(
            ["Stat", "Base", "Moy.", "Min", "Max"]
        )
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.verticalHeader().setVisible(False)
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for col in range(2, 5):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        self.results_layout.addWidget(self.results_table)

        self.results_widget.setVisible(False)
        layout.addWidget(self.results_widget)

        layout.addStretch()

    def _on_run_clicked(self):
        self.run_simulation.emit(self.scenario_count.value())

    def display_results(self, result: dict):
        self.info_label.setText(
            f"<b>{result['character_name']}</b>  ·  "
            f"Nv.{result['start_level']} → Nv.{result['target_level']}  ·  "
            f"{result['scenario_count']} scénarios"
        )

        avg = result["avg_stats"]
        base = result["base_stats"]
        mn = result.get("min_stats", avg)
        mx = result.get("max_stats", avg)

        self.results_table.setRowCount(len(STAT_KEYS))
        for row, key in enumerate(STAT_KEYS):
            label_item = QTableWidgetItem(STAT_LABELS[row])
            label_item.setTextAlignment(0x0080)  # AlignRight
            self.results_table.setItem(row, 0, label_item)

            base_val = QTableWidgetItem(str(base[key]))
            base_val.setTextAlignment(0x0080)
            self.results_table.setItem(row, 1, base_val)

            avg_val = QTableWidgetItem(str(avg[key]))
            avg_val.setTextAlignment(0x0080)
            self.results_table.setItem(row, 2, avg_val)

            min_val = QTableWidgetItem(str(mn[key]))
            min_val.setTextAlignment(0x0080)
            self.results_table.setItem(row, 3, min_val)

            max_val = QTableWidgetItem(str(mx[key]))
            max_val.setTextAlignment(0x0080)
            self.results_table.setItem(row, 4, max_val)

        self.results_widget.setVisible(True)
