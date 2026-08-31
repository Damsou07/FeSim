DARK_THEME = """
QWidget {
    background-color: #1e1e1e;
    color: #e6e6e6;
    font-size: 13px;
}

QMainWindow {
    background-color: #1e1e1e;
}

QPushButton {
    background-color: #2d2d2d;
    color: #e6e6e6;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #3a3a3a;
}

QPushButton:pressed {
    background-color: #454545;
}

QPushButton:disabled {
    color: #777777;
    background-color: #252525;
}

QTableWidget {
    background-color: #252525;
    alternate-background-color: #2b2b2b;
    color: #e6e6e6;
    gridline-color: #444444;
    border: 1px solid #444444;
    selection-background-color: #3d5a80;
    selection-color: white;
}

QHeaderView::section {
    background-color: #303030;
    color: #e6e6e6;
    padding: 6px;
    border: 1px solid #444444;
}

QLineEdit,
QSpinBox,
QDoubleSpinBox,
QComboBox {
    background-color: #252525;
    color: #e6e6e6;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 5px;
}

QLineEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QComboBox:focus {
    border: 1px solid #6a9bd8;
}

QComboBox QAbstractItemView {
    background-color: #252525;
    color: #e6e6e6;
    selection-background-color: #3d5a80;
}

QLabel {
    color: #e6e6e6;
}

QSplitter::handle {
    background-color: #444444;
}

QScrollBar:vertical {
    background-color: #202020;
    width: 12px;
}

QScrollBar::handle:vertical {
    background-color: #444444;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #555555;
}
"""
