from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class MatrixCellDelegate(QStyledItemDelegate):
    """Paint matrix cells using BackgroundRole / ForegroundRole (works with global QSS)."""

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = option.rect
        bg = index.data(Qt.ItemDataRole.BackgroundRole)
        if isinstance(bg, QBrush):
            painter.fillRect(rect, bg)
        elif isinstance(bg, QColor):
            painter.fillRect(rect, bg)

        fg = index.data(Qt.ItemDataRole.ForegroundRole)
        if isinstance(fg, QBrush):
            painter.setPen(fg.color())
        elif isinstance(fg, QColor):
            painter.setPen(fg)
        else:
            painter.setPen(option.palette.text().color())

        font = index.data(Qt.ItemDataRole.FontRole)
        if font:
            painter.setFont(font)

        text = str(index.data(Qt.ItemDataRole.DisplayRole) or "")
        alignment = index.data(Qt.ItemDataRole.TextAlignmentRole)
        if alignment is None:
            alignment = int(Qt.AlignmentFlag.AlignCenter)
        text_rect = rect.adjusted(6, 0, -6, 0)
        painter.drawText(text_rect, int(alignment) | int(Qt.AlignmentFlag.AlignVCenter), text)

        painter.restore()
