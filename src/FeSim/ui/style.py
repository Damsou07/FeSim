DARK_THEME = """
/* ── Global ─────────────────────────────────────────────────────────── */
* {
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}

QWidget {
    background-color: #12131a;
    color: #d4d4dc;
}

QMainWindow {
    background-color: #12131a;
}

/* ── Buttons ────────────────────────────────────────────────────────── */
QPushButton {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #2a2d3a, stop:1 #22252f
    );
    color: #d4d4dc;
    border: 1px solid #3a3d4a;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #363a4a, stop:1 #2e313e
    );
    border-color: #5a8dee;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #1e2028;
    border-color: #5a8dee;
}

QPushButton:disabled {
    color: #4a4d5a;
    background-color: #1a1c24;
    border-color: #2a2d38;
}

/* ── Accent buttons (ajouter / enregistrer) ─────────────────────────── */
QPushButton#addBtn,
QPushButton#saveBtn {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #1b6b3a, stop:1 #1a8a4a
    );
    color: #e8f5e9;
    border: 1px solid #2a9d5a;
    font-weight: 600;
}

QPushButton#addBtn:hover,
QPushButton#saveBtn:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #228b44, stop:1 #22a856
    );
    border-color: #43c970;
    color: #ffffff;
}

QPushButton#addBtn:pressed,
QPushButton#saveBtn:pressed {
    background-color: #145a2a;
}

/* ── Danger button (supprimer) ──────────────────────────────────────── */
QPushButton#deleteBtn {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #7a2028, stop:1 #9b2d38
    );
    color: #fdecea;
    border: 1px solid #b83a48;
    font-weight: 600;
}

QPushButton#deleteBtn:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #9b2d38, stop:1 #c0392b
    );
    border-color: #e74c3c;
    color: #ffffff;
}

QPushButton#deleteBtn:pressed {
    background-color: #5a1820;
}

/* ── Cancel button ──────────────────────────────────────────────────── */
QPushButton#cancelBtn {
    background-color: transparent;
    border: 1px solid #4a4d5a;
    color: #8a8d9a;
}

QPushButton#cancelBtn:hover {
    background-color: #2a2d38;
    border-color: #6a6d7a;
    color: #d4d4dc;
}

/* ── Table ──────────────────────────────────────────────────────────── */
QTableWidget {
    background-color: #16171f;
    alternate-background-color: #1a1b24;
    color: #d0d0da;
    gridline-color: #2a2c38;
    border: 1px solid #2a2c38;
    border-radius: 6px;
    selection-background-color: transparent;
    selection-color: #ffffff;
    outline: none;
}

QTableWidget::item {
    padding: 4px 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a3a6a,
        stop:0.15 #264e8a,
        stop:0.5 #2e5a96,
        stop:0.85 #264e8a,
        stop:1 #1a3a6a
    );
    color: #ffffff;
}

QTableWidget::item:hover:!selected {
    background-color: #1e2030;
}

/* ── Table header ───────────────────────────────────────────────────── */
QHeaderView::section {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e2030, stop:1 #181a24
    );
    color: #9094a8;
    padding: 7px 8px;
    border: none;
    border-bottom: 2px solid #2a5a8a;
    border-right: 1px solid #2a2c38;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QHeaderView::section:first {
    border-top-left-radius: 6px;
}

QHeaderView::section:last {
    border-top-right-radius: 6px;
    border-right: none;
}

QHeaderView::section:hover {
    background-color: #222538;
    color: #b0b4c8;
}

/* ── Inputs ─────────────────────────────────────────────────────────── */
QLineEdit,
QSpinBox,
QDoubleSpinBox,
QComboBox {
    background-color: #1a1c26;
    color: #d4d4dc;
    border: 1px solid #2e3040;
    border-radius: 5px;
    padding: 6px 8px;
    selection-background-color: #3a5a8a;
}

QSpinBox,
QDoubleSpinBox {
    padding-right: 22px;
}

QSpinBox::up-button,
QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 18px;
    height: 12px;
    border-left: 1px solid #2e3040;
    border-bottom: 1px solid #2e3040;
    background-color: #1e2030;
    border-top-right-radius: 4px;
}

QSpinBox::up-button:hover,
QDoubleSpinBox::up-button:hover {
    background-color: #2e3448;
}

QSpinBox::up-button:pressed,
QDoubleSpinBox::up-button:pressed {
    background-color: #1a2438;
}

QSpinBox::down-button,
QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 18px;
    height: 12px;
    border-left: 1px solid #2e3040;
    background-color: #1e2030;
    border-bottom-right-radius: 4px;
}

QSpinBox::down-button:hover,
QDoubleSpinBox::down-button:hover {
    background-color: #2e3448;
}

QSpinBox::down-button:pressed,
QDoubleSpinBox::down-button:pressed {
    background-color: #1a2438;
}

QSpinBox::up-arrow {
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid #8090a8;
}

QSpinBox::down-arrow {
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #8090a8;
}

QSpinBox::up-arrow:hover {
    border-bottom-color: #5a8dee;
}

QSpinBox::down-arrow:hover {
    border-top-color: #5a8dee;
}

/* ── Progress Bar ───────────────────────────────────────────────────── */
QProgressBar {
    background-color: #1a1c26;
    border: 1px solid #2e3040;
    border-radius: 5px;
    text-align: center;
    color: #d4d4dc;
    font-weight: 600;
    font-size: 11px;
    height: 18px;
}

QProgressBar::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a4a8a, stop:1 #2a8ab0
    );
    border-radius: 4px;
}

QLineEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QComboBox:focus {
    border: 1px solid #5a8dee;
    background-color: #1c1e2a;
}

QComboBox {
    padding-right: 20px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #2e3040;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #1e2030;
}

QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}

QComboBox QAbstractItemView {
    background-color: #1a1c26;
    color: #d4d4dc;
    border: 1px solid #2e3040;
    selection-background-color: #264e8a;
    selection-color: #ffffff;
    border-radius: 4px;
    padding: 4px;
}

/* ── Labels ─────────────────────────────────────────────────────────── */
QLabel {
    color: #c8c8d4;
}

QLabel#titleLabel {
    color: #e8e8f0;
    font-size: 15px;
    font-weight: 700;
    padding: 4px 0;
}

QLabel#sectionLabel {
    color: #8090b0;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Group boxes (Stats / Growth Rates) ─────────────────────────────── */
QGroupBox {
    background-color: #16181f;
    border: 1px solid #2a2c38;
    border-radius: 6px;
    margin-top: 14px;
    padding: 14px 8px 8px 8px;
    font-weight: 600;
    color: #9094a8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #6a8abf;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Scroll area ────────────────────────────────────────────────────── */
QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollBar:vertical {
    background-color: #12131a;
    width: 10px;
    margin: 0;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #3a3d4a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5a5d6a;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background-color: #12131a;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #3a3d4a;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #5a5d6a;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ── Splitter ───────────────────────────────────────────────────────── */
QSplitter::handle {
    background-color: #2a2c38;
    width: 2px;
    margin: 0 2px;
}

QSplitter::handle:hover {
    background-color: #5a8dee;
}

/* ── Form layout labels ─────────────────────────────────────────────── */
QFormLayout QLabel {
    color: #8090a8;
    font-size: 12px;
}

/* ── Tooltips ───────────────────────────────────────────────────────── */
QToolTip {
    background-color: #1e2030;
    color: #d4d4dc;
    border: 1px solid #3a5a8a;
    border-radius: 4px;
    padding: 4px 8px;
}

/* ── Navigation bar ─────────────────────────────────────────────────── */
QWidget#navBar {
    background-color: #0e0f15;
    border-bottom: 1px solid #2a2c38;
}

QPushButton#navBtn {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e2030, stop:1 #161820
    );
    color: #7a8ab0;
    border: 1px solid #2a3a5a;
    border-radius: 4px;
    padding: 5px 10px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton#navBtn:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #263050, stop:1 #1e2844
    );
    border-color: #5a8dee;
    color: #b0c4f0;
}

QPushButton#navBtn:pressed {
    background-color: #12141e;
}

/* ── List widget (game list) ────────────────────────────────────────── */
QListWidget {
    background-color: #16171f;
    color: #d0d0da;
    border: 1px solid #2a2c38;
    border-radius: 6px;
    outline: none;
    padding: 4px;
}

QListWidget::item {
    padding: 8px 10px;
    border-radius: 4px;
    border: none;
}

QListWidget::item:selected {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a3a6a,
        stop:0.5 #2e5a96,
        stop:1 #1a3a6a
    );
    color: #ffffff;
}

QListWidget::item:hover:!selected {
    background-color: #1e2030;
}

/* ── Simulation view ────────────────────────────────────────────────── */
QLabel#pageTitle {
    color: #eef0f8;
    font-size: 22px;
    font-weight: 700;
    padding: 0;
}

QLabel#pageSubtitle {
    color: #707890;
    font-size: 13px;
    padding-bottom: 4px;
}

QFrame#simulationControls {
    background-color: #161820;
    border: 1px solid #2a2e3c;
    border-radius: 8px;
}

QLabel#controlLabel {
    color: #8090a8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

QPushButton#simulationBtn {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a4a8a, stop:1 #2a6ab0
    );
    color: #e8f0ff;
    border: 1px solid #3a7ac8;
    font-weight: 600;
    padding: 8px 20px;
    min-width: 180px;
}

QPushButton#simulationBtn:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #2258a0, stop:1 #3480c8
    );
    border-color: #5a9aee;
    color: #ffffff;
}

QPushButton#simulationBtn:pressed {
    background-color: #143060;
}

QLabel#infoLabel {
    background-color: #161820;
    border: 1px solid #2a3a5a;
    border-radius: 8px;
    color: #c0c8dc;
    font-size: 14px;
    padding: 12px 16px;
}

QFrame#matrixCard {
    background-color: #14161e;
    border: 1px solid #2a2e3c;
    border-radius: 8px;
}

QLabel#tableTitle {
    color: #8aa8d8;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

QTableWidget#matrixTable {
    background-color: #12141c;
    border: none;
    border-radius: 0;
    gridline-color: #252830;
}

QTableWidget#matrixStatTable {
    background-color: #12141c;
    border: none;
    border-right: 2px solid #3a5a8a;
    border-radius: 0;
    gridline-color: #252830;
}

QTableWidget#matrixTable::item,
QTableWidget#matrixStatTable::item {
    padding: 0;
    border: none;
    background: transparent;
}

QTableWidget#matrixTable::item:selected,
QTableWidget#matrixStatTable::item:selected,
QTableWidget#matrixTable::item:hover,
QTableWidget#matrixStatTable::item:hover {
    background: transparent;
}

QTableWidget#matrixTable QHeaderView::section,
QTableWidget#matrixStatTable QHeaderView::section {
    background-color: #1a1e28;
    color: #9098b0;
    border-bottom: 2px solid #3a5a8a;
    padding: 8px 10px;
}

QScrollArea#matrixScroll {
    background-color: transparent;
}
"""
