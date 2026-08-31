from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QStyledItemDelegate, QStyle, QStyleOptionViewItem


class GlowingRowDelegate(QStyledItemDelegate):
    """Paints selected rows with a left-side glow accent."""

    GLOW_COLOR = QColor(70, 140, 230)
    GLOW_WIDTH = 3

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index,
    ):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_selected = option.state & QStyle.StateFlag.State_Selected

        if is_selected:
            rect = option.rect

            # ── Background gradient ─────────────────────────────────
            bg = QLinearGradient(QPointF(rect.left(), rect.top()), QPointF(rect.right(), rect.top()))
            bg.setColorAt(0.0, QColor(20, 50, 100, 220))
            bg.setColorAt(0.12, QColor(32, 68, 130, 230))
            bg.setColorAt(0.5, QColor(38, 78, 148, 235))
            bg.setColorAt(0.88, QColor(32, 68, 130, 230))
            bg.setColorAt(1.0, QColor(20, 50, 100, 220))
            painter.fillRect(rect, bg)

            # ── Left glow bar ───────────────────────────────────────
            glow_rect = QRectF(rect.left(), rect.top(), self.GLOW_WIDTH, rect.height())
            grad = QLinearGradient(QPointF(glow_rect.left(), glow_rect.top()), QPointF(glow_rect.left(), glow_rect.bottom()))
            grad.setColorAt(0.0, QColor(100, 170, 255, 0))
            grad.setColorAt(0.2, self.GLOW_COLOR)
            grad.setColorAt(0.8, self.GLOW_COLOR)
            grad.setColorAt(1.0, QColor(100, 170, 255, 0))
            painter.fillRect(glow_rect, grad)

            # ── Soft top/bottom edge lines ──────────────────────────
            edge_pen = QPen(QColor(80, 150, 240, 60), 1)
            painter.setPen(edge_pen)
            painter.drawLine(rect.topLeft(), rect.topRight())
            painter.drawLine(rect.bottomLeft(), rect.bottomRight())

            # ── Text ────────────────────────────────────────────────
            text_rect = rect.adjusted(self.GLOW_WIDTH + 6, 0, -4, 0)
            text = index.data(Qt.ItemDataRole.DisplayRole) or ""
            painter.setPen(QColor(255, 255, 255))
            font = painter.font()
            font.setWeight(font.Weight.DemiBold)
            painter.setFont(font)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | option.displayAlignment, text)

            painter.restore()
            return

        # ── Not selected: default painting ──────────────────────────
        painter.restore()
        super().paint(painter, option, index)
