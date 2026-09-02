from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class ScoreChartCanvas(QWidget):
    """Custom QPainter widget rendering neon curves for score evolution by level."""

    COLOR_AVG = QColor("#00ff87")      # Neon Green
    COLOR_BEST = QColor("#00d2ff")     # Neon Electric Blue
    COLOR_WORST = QColor("#ff3366")    # Neon Crimson Red
    COLOR_BG = QColor("#12141c")
    COLOR_GRID = QColor("#1f2438")
    COLOR_TEXT = QColor("#8090a8")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(320)
        self.setMouseTracking(True)

        self._columns: list[str] = []
        self._avg_curve: list[float] = []
        self._best_curve: list[float] = []
        self._worst_curve: list[float] = []

        self._hover_idx: int | None = None

    def set_data(
        self,
        columns: list[str],
        avg_curve: list[float],
        best_curve: list[float],
        worst_curve: list[float],
    ):
        self._columns = columns
        self._avg_curve = avg_curve
        self._best_curve = best_curve
        self._worst_curve = worst_curve
        self._hover_idx = None
        self.update()

    def mouseMoveEvent(self, event):
        if not self._columns or not self._avg_curve:
            return

        margin_left = 55.0
        margin_right = 25.0
        width = self.width() - margin_left - margin_right

        if width <= 0:
            return

        n_pts = len(self._columns)
        step_x = width / max(1, n_pts - 1) if n_pts > 1 else width

        rel_x = event.position().x() - margin_left
        idx = int(round(rel_x / step_x))
        idx = max(0, min(n_pts - 1, idx))

        if idx != self._hover_idx:
            self._hover_idx = idx
            self.update()

    def leaveEvent(self, event):
        self._hover_idx = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)

        rect = self.rect()
        painter.fillRect(rect, self.COLOR_BG)

        if not self._columns or not self._avg_curve:
            painter.setPen(self.COLOR_TEXT)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Aucune donnée de simulation")
            return

        margin_left = 55.0
        margin_right = 25.0
        margin_top = 25.0
        margin_bottom = 45.0

        graph_w = rect.width() - margin_left - margin_right
        graph_h = rect.height() - margin_top - margin_bottom

        if graph_w <= 0 or graph_h <= 0:
            return

        # Determine Y min & max with padding
        all_vals = self._avg_curve + self._best_curve + self._worst_curve
        min_val = min(all_vals) if all_vals else 0.0
        max_val = max(all_vals) if all_vals else 100.0

        y_range = max_val - min_val
        if y_range < 5.0:
            y_range = 5.0
            min_val -= 2.0
            max_val += 3.0
        else:
            min_val = max(0.0, min_val - y_range * 0.08)
            max_val = max_val + y_range * 0.08
            y_range = max_val - min_val

        # Draw Grid & Y-Axis Labels
        painter.setPen(QPen(self.COLOR_GRID, 1, Qt.PenStyle.DashLine))
        font_axis = QFont("Segoe UI", 9)
        painter.setFont(font_axis)

        n_y_grid = 5
        for i in range(n_y_grid + 1):
            val = min_val + (y_range * i / n_y_grid)
            y_pos = margin_top + graph_h - (i / n_y_grid) * graph_h

            # Horizontal gridline
            painter.drawLine(
                QPointF(margin_left, y_pos),
                QPointF(margin_left + graph_w, y_pos),
            )

            # Y label
            painter.setPen(self.COLOR_TEXT)
            painter.drawText(
                QRectF(0, y_pos - 10, margin_left - 8, 20),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{val:.1f}",
            )
            painter.setPen(QPen(self.COLOR_GRID, 1, Qt.PenStyle.DashLine))

        n_pts = len(self._columns)
        step_x = graph_w / max(1, n_pts - 1) if n_pts > 1 else graph_w

        # Draw X-Axis Labels (Subsampled if too many columns)
        skip_step = max(1, n_pts // 15)
        for i in range(0, n_pts, skip_step):
            x_pos = margin_left + i * step_x
            col_text = self._columns[i]

            painter.setPen(self.COLOR_TEXT)
            painter.drawText(
                QRectF(x_pos - 20, margin_top + graph_h + 8, 40, 25),
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
                col_text,
            )

        # Helper mapping values to screen coordinates
        def map_points(curve: list[float]) -> list[QPointF]:
            pts = []
            for idx, v in enumerate(curve):
                px = margin_left + idx * step_x
                py = margin_top + graph_h - ((v - min_val) / y_range) * graph_h
                pts.append(QPointF(px, py))
            return pts

        pts_avg = map_points(self._avg_curve)
        pts_best = map_points(self._best_curve)
        pts_worst = map_points(self._worst_curve)

        # Function to draw neon curve with glow effect and area fill
        def draw_neon_curve(pts: list[QPointF], color: QColor):
            if not pts:
                return

            path = QPainterPath()
            path.moveTo(pts[0])
            for pt in pts[1:]:
                path.lineTo(pt)

            # 1. Translucent Gradient Fill Under Curve
            fill_path = QPainterPath(path)
            fill_path.lineTo(pts[-1].x(), margin_top + graph_h)
            fill_path.lineTo(pts[0].x(), margin_top + graph_h)
            fill_path.closeSubpath()

            grad = QLinearGradient(0, margin_top, 0, margin_top + graph_h)
            c_top = QColor(color)
            c_top.setAlpha(45)
            c_bot = QColor(color)
            c_bot.setAlpha(0)
            grad.setColorAt(0.0, c_top)
            grad.setColorAt(1.0, c_bot)
            painter.fillPath(fill_path, QBrush(grad))

            # 2. Outer Glow Stroke
            glow_color = QColor(color)
            glow_color.setAlpha(70)
            painter.setPen(QPen(glow_color, 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(path)

            # 3. Inner Crisp Neon Line
            painter.setPen(QPen(color, 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(path)

        # Draw curves (Worst, Best, Avg on top for readability)
        draw_neon_curve(pts_worst, self.COLOR_WORST)
        draw_neon_curve(pts_best, self.COLOR_BEST)
        draw_neon_curve(pts_avg, self.COLOR_AVG)

        # Draw Hover Crosshair and Callout Tooltip
        if self._hover_idx is not None and 0 <= self._hover_idx < n_pts:
            h_idx = self._hover_idx
            hx = pts_avg[h_idx].x()

            # Vertical guide line
            guide_pen = QPen(QColor("#5a8dee"), 1, Qt.PenStyle.DashLine)
            painter.setPen(guide_pen)
            painter.drawLine(QPointF(hx, margin_top), QPointF(hx, margin_top + graph_h))

            # Dots on each curve at hover index
            def draw_dot(pt: QPointF, color: QColor):
                painter.setPen(Qt.PenStyle.NoPen)
                halo = QColor(color)
                halo.setAlpha(120)
                painter.setBrush(QBrush(halo))
                painter.drawEllipse(pt, 6, 6)
                painter.setBrush(QBrush(color))
                painter.drawEllipse(pt, 3.5, 3.5)

            draw_dot(pts_worst[h_idx], self.COLOR_WORST)
            draw_dot(pts_best[h_idx], self.COLOR_BEST)
            draw_dot(pts_avg[h_idx], self.COLOR_AVG)

            # Floating Tooltip Box
            col_name = self._columns[h_idx]
            v_avg = self._avg_curve[h_idx]
            v_best = self._best_curve[h_idx]
            v_worst = self._worst_curve[h_idx]

            t_box_w = 140.0
            t_box_h = 75.0
            t_x = hx + 12.0
            if t_x + t_box_w > rect.width() - margin_right:
                t_x = hx - t_box_w - 12.0

            t_y = margin_top + 10.0
            box_rect = QRectF(t_x, t_y, t_box_w, t_box_h)

            painter.setPen(QPen(QColor("#3a4e70"), 1))
            painter.setBrush(QBrush(QColor("#181c28")))
            painter.drawRoundedRect(box_rect, 6, 6)

            # Tooltip text
            font_tt_title = QFont("Segoe UI", 9, QFont.Weight.Bold)
            font_tt_val = QFont("Segoe UI", 8)

            painter.setFont(font_tt_title)
            painter.setPen(QColor("#e8e8f0"))
            painter.drawText(QRectF(t_x + 8, t_y + 4, t_box_w - 16, 16), Qt.AlignmentFlag.AlignLeft, f"Niveau: {col_name}")

            painter.setFont(font_tt_val)
            painter.setPen(self.COLOR_BEST)
            painter.drawText(QRectF(t_x + 8, t_y + 22, t_box_w - 16, 14), Qt.AlignmentFlag.AlignLeft, f"Meilleur: {v_best:.1f}")

            painter.setPen(self.COLOR_AVG)
            painter.drawText(QRectF(t_x + 8, t_y + 38, t_box_w - 16, 14), Qt.AlignmentFlag.AlignLeft, f"Moyenne: {v_avg:.1f}")

            painter.setPen(self.COLOR_WORST)
            painter.drawText(QRectF(t_x + 8, t_y + 54, t_box_w - 16, 14), Qt.AlignmentFlag.AlignLeft, f"Pire: {v_worst:.1f}")


class ScoreChartView(QFrame):
    """Container card view displaying the score evolution neon chart and legend."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("scoreChartCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # Header row with title & legend
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        title = QLabel("ÉVOLUTION DU SCORE PAR NIVEAU")
        title.setObjectName("scoreChartTitle")
        header.addWidget(title)

        header.addStretch()

        # Legend items
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(14)

        def create_legend_item(text: str, color_hex: str) -> QWidget:
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(5)

            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color_hex}; font-size: 13px;")
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #a0acdc; font-size: 11px; font-weight: 600;")

            l.addWidget(dot)
            l.addWidget(lbl)
            return w

        legend_layout.addWidget(create_legend_item("Moyenne", "#00ff87"))
        legend_layout.addWidget(create_legend_item("Meilleur", "#00d2ff"))
        legend_layout.addWidget(create_legend_item("Pire", "#ff3366"))

        header.addLayout(legend_layout)
        layout.addLayout(header)

        # Canvas
        self.canvas = ScoreChartCanvas()
        layout.addWidget(self.canvas)

    def set_data(
        self,
        columns: list[str],
        avg_curve: list[float],
        best_curve: list[float],
        worst_curve: list[float],
    ):
        self.canvas.set_data(columns, avg_curve, best_curve, worst_curve)
