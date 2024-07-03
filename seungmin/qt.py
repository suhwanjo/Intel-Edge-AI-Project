from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpServer, QHostAddress
import json
import sys
import random


class _DashBoardMain(QWidget):
    """WARNING: This is a private class. do not import this."""
    def __init__(self, parent, size: tuple | list = (1280, 720), hide_creator_button: bool = False,
                 skip_start_screen: bool = False, skip_loading_screen: bool = False, do_not_move: bool = False):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(True)
        self.setFixedSize(*size)
        self.oldPos = QCursor().pos()
        self.hide_creator_button = hide_creator_button
        self.skip_start_screen = skip_start_screen
        self.skip_loading_screen = skip_loading_screen
        self.do_not_move = do_not_move
        self.initUI()

    def initUI(self):
        self.stacked_widget()
        self.loding_screen()
        self.dash_board_design()
        self.skip_start_screen = True
        self.skip_loading_screen = True
        if self.skip_start_screen:
            self.swidget.setCurrentIndex(1)
            if self.skip_loading_screen:
                self.swidget.setCurrentIndex(2)
                self.dash_board_design_widget.start_up_animation()
            else:
                self.progress_bar_animation.start()

    def stacked_widget(self):
        self.swidget = QStackedWidget(self)
        self.swidget.setContentsMargins(0, 0, 0, 0)
        grad = "qlineargradient(spread:pad, x1:0.6, y1:0.4, x2:0.1, y2:0.8, stop:0 {color1}, stop:{value} {color2}, stop:1.0 {color1});".format(
            color1=QColor(0, 0, 0, 100).name(), color2=QColor(13, 13, 13).name(), value=0.5)
        self.setStyleSheet("background-color: %s;" % grad)
        self.swidget.setFixedSize(self.width(), self.height())
        self.swidget.setCurrentIndex(0)

    def loding_screen(self):
        loading_screen_widget = QWidget()
        loading_screen_widget.setContentsMargins(0, 0, 0, 0)
        loading_screen_widget.setFixedSize(self.width(), self.height())
        self.swidget.addWidget(loading_screen_widget)

        get_ready_label = QLabel(loading_screen_widget)
        get_ready_label.setFixedSize(*map(round, (self.width() * 0.6, self.height() * 0.2)))
        get_ready_label.move(self.rect().center() - get_ready_label.rect().center() - QPoint(0, get_ready_label.height()))
        get_ready_label.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: rgb(207, 184, 29)")
        get_ready_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        saftey_rule_font = QFont("Consolas", 0, 0, True)
        saftey_rule_font.setBold(True)
        saftey_rule_font.setPixelSize(round(self.width() * 0.035))
        get_ready_label.setFont(saftey_rule_font)
        get_ready_label.setText("Get ready for the ride...")

        loding_progress_bar = QProgressBar(loading_screen_widget)
        loding_progress_bar.setContentsMargins(0, 0, 0, 0)
        loding_progress_bar.setFixedSize(*map(round, (loading_screen_widget.width() * 0.7, loading_screen_widget.height() * 0.1)))
        loding_progress_bar.move(self.rect().center() - loding_progress_bar.rect().center())
        loding_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loding_progress_bar_font = QFont("Consolas", 0, 0, True)
        loding_progress_bar_font.setBold(True)
        loding_progress_bar_font.setPixelSize(round(self.width() * 0.04))
        loding_progress_bar.setFont(loding_progress_bar_font)
        grad = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color3});".format(
            color1=QColor(240, 0, 0).name(), color2=QColor(255, 80, 0).name(), color3=QColor(255, 255, 0).name(), value=0.3)
        loding_progress_bar.setStyleSheet("QProgressBar {background-color: rgba(0, 0, 0, 0); color: white; border-radius: %spx;}" % str(
            loding_progress_bar.height() // 2) + "QProgressBar::chunk {background-color: %s; border-radius: %spx;}" % (
                                          grad, str(loding_progress_bar.height() // 2)))
        self.progress_bar_animation = QPropertyAnimation(loding_progress_bar, b"value")
        self.progress_bar_animation.setStartValue(loding_progress_bar.height() * 0.2)
        self.progress_bar_animation.valueChanged.connect(self.driving_rule_info)
        self.progress_bar_animation.setEndValue(100)
        self.progress_bar_animation.setDuration(3000)
        self.saftey_rules = ("Do not drink and drive.", "Always wear a helmet!", "Drive within the speed limits.",
                             "Don't use mobile phones while driving.", "Buckle up before you drive.", "Keep a safe distance from vehicles!")
        self.saftey_rule_label = QLabel(loading_screen_widget)
        self.saftey_rule_label.setFixedSize(*map(round, (self.width() * 0.6, self.height() * 0.2)))
        self.saftey_rule_label.move(self.rect().center() - self.saftey_rule_label.rect().center() + QPoint(0, self.saftey_rule_label.height()))
        self.saftey_rule_label.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: yellow")
        self.saftey_rule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        saftey_rule_font = QFont("Consolas", 0, 0, True)
        saftey_rule_font.setBold(True)
        saftey_rule_font.setPixelSize(round(self.width() * 0.025))
        self.saftey_rule_label.setFont(saftey_rule_font)
        self.saftey_rule_label.setText(random.sample(self.saftey_rules, 1)[0])

    def driving_rule_info(self, val):
        if val % 33 == 0 and val != 99:
            self.saftey_rule_label.setText(random.sample(self.saftey_rules, 1)[0])
        if val == 100:
            self.swidget.setCurrentIndex(2)
            self.dash_board_design_widget.start_up_animation()

    def dash_board_design(self):
        self.dash_board_design_widget = _DashBoardContolsDesign(self.swidget)
        self.swidget.addWidget(self.dash_board_design_widget)

    def mousePressEvent(self, event):
        if not self.do_not_move: self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.do_not_move:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QCoreApplication.instance().quit()


class _DashBoardContolsDesign(QWidget):
    """WARNING: This is a private class. do not import this."""
    def __init__(self, parent=None):
        super(_DashBoardContolsDesign, self).__init__(parent)
        self.parent_ = parent
        self.resize(self.parent_.size())
        self.setContentsMargins(0, 0, 0, 0)
        self.header_properties()
        self.indicators_properties()
        self.horn_properties()
        self.break_properties()
        self.accelerator_properties()
        self.speedometer_properties()
        self.left_sign_detected = False
        self.unprotected_left_image = QPixmap("./unprotected_left.png")
        self.traffic_light_state = 3  # 초기 상태, 예: 3은 꺼진 상태

    def set_left_sign_detected(self, detected):
        self.left_sign_detected = detected
        self.update()  # 화면 갱신을 위해 update 호출

    def header_properties(self):
        self.header_border_color_lst = (QColorConstants.Svg.orchid, QColorConstants.Svg.red)
        self.header_border_color = 0
        self.traffic_light_state = 3
        header_trans = QTransform()
        header_trans.scale(self.width() * 0.012, self.height() * 0.008)
        header_boarder = QPolygonF((QPointF(10, 10), QPointF(15, 10), QPointF(25, 25),
                                   QPointF(55, 25), QPointF(65, 10), QPointF(70, 10),
                                   QPointF(60, 30), QPointF(20, 30)))
        self.scaled_header_border = header_trans.map(header_boarder)
        scaled_header_border_bounding_rect = QRect(self.scaled_header_border.boundingRect().toRect())
        self.scaled_header_border.translate(self.rect().center() - scaled_header_border_bounding_rect.center())
        self.scaled_header_border.translate(0, -self.rect().height() * 0.5 + scaled_header_border_bounding_rect.height() * 0.5)
        header_inner = QPolygonF((QPointF(15, 10), QPointF(25, 25),
                                  QPointF(55, 25), QPointF(65, 10)))
        self.scaled_header_inner = header_trans.map(header_inner)
        scaled_header_inner_bounding_rect = QRect(self.scaled_header_inner.boundingRect().toRect())
        self.scaled_header_inner.translate(self.rect().center() - scaled_header_inner_bounding_rect.center())
        self.scaled_header_inner.translate(0, -self.rect().height() * 0.5 + scaled_header_inner_bounding_rect.height() * 0.5)

    def set_traffic_light_state(self, state):
        self.traffic_light_state = state
        self.update()

    def header_painting(self, painter: QPainter):
        painter.setPen(QPen(QGradient(QGradient.Preset.Blessing), round(self.width() * 0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.setBrush(QBrush(self.header_border_color_lst[self.header_border_color], Qt.BrushStyle.Dense4Pattern))
        painter.drawPolygon(self.scaled_header_border)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(76, 97, 78, 100)))
        painter.drawPolygon(self.scaled_header_inner)
        painter.setPen(QPen(QGradient(QGradient.Preset.Blessing), round(self.width() * 0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.drawPolygon(self.scaled_header_border)
        light_diameter = round(self.height() * 0.1)
        light_spacing = round(self.width() * 0.02)
        light_radius = light_diameter // 2
        scaled_header_inner_bounding_rect = self.scaled_header_inner.boundingRect().toRect()
        center_y = scaled_header_inner_bounding_rect.center().y()
        left_x = scaled_header_inner_bounding_rect.right() // 2
        colors = [QColorConstants.Svg.red, QColorConstants.Svg.yellow, QColorConstants.Svg.green]
        for i, color in enumerate(colors):
            if i == self.traffic_light_state:
                painter.setBrush(QBrush(color))
            else:
                painter.setBrush(QBrush(QColor(50, 50, 50)))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            x = left_x + i * (light_diameter + light_spacing)
            painter.drawEllipse(QPointF(x + light_radius, center_y), light_radius, light_radius)

    def indicators_properties(self):
        self.indicator_timer = QTimer()
        self.indicator_timer.timeout.connect(self.indicator_blink_animation)
        self.indicator_color_list = (QColorConstants.DarkGreen, QColorConstants.Green)
        self.right_indicator_color = self.indicator_color_list[0]
        self.left_indicator_color = self.indicator_color_list[0]
        self.right_indicator_state = 0
        self.left_indicator_state = 0
        self.right_indicator_blink = 0
        self.left_indicator_blink = 0
        indicator_trans = QTransform()
        indicator_trans.scale(self.width() * 0.001, self.height() * 0.0015)
        left_idicator = QPolygonF((QPointF(40, 80), QPointF(90, 120), QPointF(90, 100), QPointF(150, 100),
                                   QPointF(150, 60), QPointF(90, 60), QPointF(90, 40)))
        self.scaled_left_idicator = indicator_trans.map(left_idicator)
        self.scaled_left_idicator.translate(-self.scaled_left_idicator.boundingRect().x(), -self.scaled_left_idicator.boundingRect().y())
        self.scaled_left_idicator.translate(self.width() * 0.03, self.height() * 0.06)
        rotate_t = QTransform()
        rotate_t.rotate(180, Qt.Axis.YAxis)
        self.scaled_right_idicator = self.scaled_left_idicator
        self.scaled_right_idicator = rotate_t.map(self.scaled_right_idicator)
        self.scaled_right_idicator.translate(-self.scaled_right_idicator.boundingRect().x(), -self.scaled_right_idicator.boundingRect().y())
        self.scaled_right_idicator.translate(self.width() - self.scaled_right_idicator.boundingRect().width() - self.scaled_left_idicator.boundingRect().x(), self.height() * 0.06)

    def set_traffic_light_state(self, state):
        self.traffic_light_state = state
        self.repaint()

    def indicators_painting(self, painter: QPainter):
        painter.setPen(QPen(self.left_indicator_color, round(self.width() * 0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.setBrush(QBrush(self.left_indicator_color, Qt.BrushStyle.Dense3Pattern))
        painter.drawPolygon(self.scaled_left_idicator)
        painter.setPen(QPen(self.right_indicator_color, round(self.width() * 0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.setBrush(QBrush(self.right_indicator_color, Qt.BrushStyle.Dense3Pattern))
        painter.drawPolygon(self.scaled_right_idicator)

    def indicator_triger(self, indecator):
        if indecator == 0:  # left indicator
            self.left_indicator_state = not self.left_indicator_state
        if indecator == 1:  # right indicator
            self.right_indicator_state = not self.right_indicator_state
        if self.right_indicator_state or self.left_indicator_state:
            self.indicator_timer.start(300)  # blink indicator interval of 600ms
        else:
            self.indicator_blink_animation()
            self.indicator_timer.stop()

    def indicator_blink_animation(self):
        if self.right_indicator_state:
            self.right_indicator_color = self.indicator_color_list[self.right_indicator_blink]
            self.right_indicator_blink = not self.right_indicator_blink
        else:
            self.right_indicator_color = self.indicator_color_list[0]
        if self.left_indicator_state:
            self.left_indicator_color = self.indicator_color_list[self.left_indicator_blink]
            self.left_indicator_blink = not self.left_indicator_blink
        else:
            self.left_indicator_color = self.indicator_color_list[0]
        self.repaint()

    def horn_properties(self):
        self.horn_sound_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.BlackSea))
        self.horn_sound_color_idx = 0
        self.horn_state = 0  # 0 -> off 1 -> on

    def horn_painting(self, painter: QPainter):
        painter.setPen(QPen(QColorConstants.Black, round(self.width() * 0.0012)))
        painter.setBrush(QBrush(QGradient(QGradient.Preset.RichMetal)))
        horn_trans = QTransform()
        horn_trans.scale(self.width() * 0.0012, self.height() * 0.002)
        horn = QPolygonF((QPointF(40, 50), QPointF(60, 50), QPointF(90, 30), QPointF(100, 30),
                          QPointF(100, 100), QPointF(90, 100), QPointF(60, 80), QPointF(40, 80)))
        scaled_horn = horn_trans.map(horn)
        scaled_horn.translate(-scaled_horn.boundingRect().x(), -scaled_horn.boundingRect().y())
        scaled_horn.translate(self.width() * 0.03, self.height() * 0.7)
        painter.drawPolygon(scaled_horn)
        horn_rect = scaled_horn.boundingRect().toRect()
        painter.setPen(QPen(QColorConstants.Gray, round(self.width() * 0.0012)))
        painter.drawLine(horn_rect.topRight(), horn_rect.bottomRight())
        painter.setPen(QPen(self.horn_sound_color_lst[self.horn_sound_color_idx], round(self.width() * 0.0025), cap=Qt.PenCapStyle.RoundCap))
        sound_rect1 = QRect(0, 0, round(horn_rect.width() * 1.5), round(horn_rect.height() * 1.5))
        sound_rect1.moveCenter(horn_rect.center())
        sound_rect1.moveRight(round(horn_rect.width() * 1.7))
        painter.drawArc(sound_rect1.x(), sound_rect1.y(), sound_rect1.width(), sound_rect1.height(), 35 * 16, -70 * 16)
        sound_rect2 = QRect(0, 0, round(horn_rect.width() * 1.3), round(horn_rect.height() * 1.3))
        sound_rect2.moveCenter(horn_rect.center())
        sound_rect2.moveRight(round(horn_rect.width() * 1.6))
        painter.drawArc(sound_rect2.x(), sound_rect2.y(), sound_rect2.width(), sound_rect2.height(), 27 * 16, -55 * 16)
        sound_rect3 = QRect(0, 0, round(horn_rect.width() * 1.2), round(horn_rect.height() * 1.2))
        sound_rect3.moveCenter(horn_rect.center())
        sound_rect3.moveRight(round(horn_rect.width() * 1.5))
        painter.drawArc(sound_rect3.x(), sound_rect3.y(), sound_rect3.width(), sound_rect3.height(), 17 * 16, -35 * 16)

    def set_horn_state(self, val):
        self.horn_sound_color_idx = val
        if self.horn_sound_color_idx != self.horn_state:
            self.repaint()
        self.horn_state = val

    def break_properties(self):
        self.break_state = 0
        self.break_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.ColorfulPeach))

    def set_break_state(self, val):
        self.break_state = val
        self.header_border_color = val
        self.repaint()

    def break_painting(self, painter: QPainter):
        break_font = QFont("Consolas", 0, 0, True)
        break_font.setPixelSize(round(self.width() * 0.045))
        break_fm = QFontMetrics(break_font)
        break_rect = break_fm.boundingRect("BREAK")
        painter.setFont(break_font)
        break_rect.moveTo(self.rect().center() + QPointF(self.rect().width() * 0.345, self.rect().height() * 0.1).toPoint())
        painter.setPen(QPen(self.break_color_lst[self.break_state], round(self.width() * 0.0025)))
        painter.drawText(break_rect, Qt.AlignmentFlag.AlignCenter, "BREAK")

    def accelerator_properties(self):
        self.speed_angle_factor = 200 / 300  # 200 default top speed and 300 available angle of speedometer
        self.speed = 0
        self.accelerator_state = 0
        self.accelerator_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.FruitBlend))

    def set_speed(self, val):
        self.speed = round(val / self.speed_angle_factor) if round(val / self.speed_angle_factor) <= 300 else 300
        self.repaint()

    def get_speed(self):
        return round(self.speed * self.speed_angle_factor)

    def set_accelerator_state(self, val):
        self.accelerator_state = val
        if self.speed <= 300 and not self.break_state:
            self.speed += self.speed_angle_factor
            self.repaint()

    def accelerator_painting(self, painter: QPainter):
        accelerator_font = QFont("Consolas", 0, 0, True)
        accelerator_font.setPixelSize(round(self.width() * 0.031))
        accelerator_fm = QFontMetrics(accelerator_font)
        painter.setFont(accelerator_font)
        painter.setPen(QPen(self.accelerator_color_lst[self.accelerator_state], round(self.width() * 0.0025)))

    def speedometer_properties(self):
        self.speedometer_bounding_rect = QRectF(self.width() * 0.173, self.height() * 1.01, self.width() * 0.4, self.width() * 0.4)
        self.enable_speedometer_resetter = True
        self.speedometer_resetter_timer = QTimer()
        self.speedometer_resetter_timer.timeout.connect(self.speedometer_resetter)
        self.speedometer_resetter_timer.start(5)
        self.speed_range = 200
        self.for_loop_count = self.speed_range // 20 + 2
        self.angle_to_rotate = 300 / (self.speed_range / 20)
        self.compromise_angle = 30 - self.angle_to_rotate
        self.compromise_angle_half = self.compromise_angle + self.angle_to_rotate / 2
        self.enable_sub_number = True

    def set_speedometer_range(self, top_speed):
        if 40 <= top_speed <= 400:
            self.speed_range = int(top_speed - top_speed % -20 if top_speed % 20 >= 10 else top_speed - top_speed % 20)
        elif top_speed < 40:
            self.speed_range = 40
        elif top_speed > 400:
            self.speed_range = 400
        self.speed_angle_factor = self.speed_range / 300
        self.for_loop_count = self.speed_range // 20 + 2
        self.angle_to_rotate = 300 / (self.speed_range / 20)
        self.compromise_angle = 30 - self.angle_to_rotate
        self.compromise_angle_half = self.compromise_angle + self.angle_to_rotate / 2
        self.enable_sub_number = True if self.speed_range <= 260 else False
        self.repaint()

    def set_speedometer_resetter_state(self, val):
        self.enable_speedometer_resetter = val

    def speedometer_resetter(self):
        if self.speed > 0 and self.enable_speedometer_resetter:
            if not self.accelerator_state:  # accelerator released
                if self.break_state:  # break presssed
                    self.speed -= 3 * self.speed_angle_factor
                else:
                    self.speed -= self.speed_angle_factor
            if self.break_state:  # break presssed
                self.speed -= 2 * self.speed_angle_factor
            if self.speed < 0:
                self.speed = 0
            self.repaint()

    def speedometer_painting(self, painter: QPainter):
        conicalGradient = QConicalGradient(QPointF(self.speedometer_bounding_rect.width() / 2, self.speedometer_bounding_rect.width() / 2), -59 * 16)
        conicalGradient.setColorAt(0.2, QColorConstants.Green)
        conicalGradient.setColorAt(0.7, QColorConstants.Yellow)
        conicalGradient.setColorAt(0.5, QColorConstants.Red)
        inner_dial = self.speedometer_bounding_rect.toRect()
        inner_dial.setSize(QSizeF(self.speedometer_bounding_rect.width() * 0.975, self.speedometer_bounding_rect.width() * 0.975).toSize())
        inner_dial.moveCenter(self.speedometer_bounding_rect.center().toPoint())
        painter.setPen(QPen(conicalGradient, self.width() * 0.01))
        painter.drawArc(inner_dial, -59 * 16, 298 * 16)
        number_font = QFont("Consolas", 0, 0, True)
        number_font.setPixelSize(round(self.width() * 0.02))
        number_fm = QFontMetrics(number_font)
        number_rect = number_fm.boundingRect("000")
        painter.setFont(number_font)
        painter.setPen(QPen(QGradient(QGradient.Preset.FebruaryInk), self.width() * 0.005))
        center = self.speedometer_bounding_rect.center()
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(self.compromise_angle)
        painter.translate(-center.x(), -center.y())
        for a in range(1, self.for_loop_count):
            painter.translate(center.x(), center.y())
            painter.rotate(self.angle_to_rotate)
            painter.translate(-center.x(), -center.y())
            spike_p1 = center + QPointF(0, self.speedometer_bounding_rect.height() // 2)
            spike_p2 = center + QPointF(0, self.speedometer_bounding_rect.height() * 0.45)
            painter.drawLine(spike_p1, spike_p2)
            number_point = spike_p2.toPoint() - QPoint(0, round(self.width() * 0.02))
            painter.save()
            painter.translate(number_point.x(), number_point.y())
            painter.rotate(a * -self.angle_to_rotate - self.compromise_angle)
            painter.translate(-number_point.x(), -number_point.y())
            number_rect.moveCenter(number_point)
            painter.drawText(number_rect, Qt.AlignmentFlag.AlignCenter, str((a - 1) * 20))
            painter.restore()
        painter.restore()
        painter.setPen(QPen(QGradient(QGradient.Preset.FebruaryInk), self.width() * 0.003))
        number_font.setPixelSize(round(self.width() * 0.015))
        painter.setFont(number_font)
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(self.compromise_angle_half)
        painter.translate(-center.x(), -center.y())
        for a in range(1, self.for_loop_count - 1):
            painter.translate(center.x(), center.y())
            painter.rotate(self.angle_to_rotate)
            painter.translate(-center.x(), -center.y())
            spike_p1 = center + QPointF(0, self.speedometer_bounding_rect.height() // 2)
            spike_p2 = center + QPointF(0, self.speedometer_bounding_rect.height() * 0.47)
            painter.drawLine(spike_p1, spike_p2)
            number_point = spike_p2.toPoint() - QPoint(0, round(self.width() * 0.02))
            if self.enable_sub_number:
                painter.save()
                painter.translate(number_point.x(), number_point.y())
                painter.rotate(a * -self.angle_to_rotate - self.compromise_angle_half)
                painter.translate(-number_point.x(), -number_point.y())
                number_rect.moveCenter(number_point)
                painter.drawText(number_rect, Qt.AlignmentFlag.AlignCenter, str((2 * a - 1) * 10))
                painter.restore()
        painter.restore()
        painter.setPen(QPen(QGradient(QGradient.Preset.Blessing), round(self.width() * 0.003), cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(QBrush(QGradient(QGradient.Preset.Blessing)))
        hand_polygon = (center + QPoint(0, round(self.height() * 0.0055)), center + QPoint(0, -round(self.height() * 0.0055)), center + QPoint(round(self.height() * 0.28), 0))
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(120 + self.speed)
        painter.translate(-center.x(), -center.y())
        painter.drawPolygon(hand_polygon)
        painter.restore()
        painter.setPen(QPen(QGradient(QGradient.Preset.CrystalRiver), round(self.width() * 0.03), cap=Qt.PenCapStyle.RoundCap))
        painter.drawPoint(center)
        painter.setPen(QPen(QGradient(QGradient.Preset.CrystalRiver), self.width() * 0.005))
        painter.drawArc(self.speedometer_bounding_rect.toRect(), -60 * 16, 300 * 16)
        painter.setPen(QPen(QGradient(QGradient.Preset.Crystalline), self.width() * 0.005))
        speed_font = QFont("Consolas", 0, 0, True)
        speed_font.setPixelSize(round(self.width() * 0.035))
        speed_fm = QFontMetrics(speed_font)
        speed_kmph_rect = speed_fm.boundingRect("000-km/h")
        painter.setFont(speed_font)
        speed_kmph_rect.moveCenter(center.toPoint())
        speed_kmph_rect.moveBottom(round(self.speedometer_bounding_rect.bottom()))
        painter.drawText(speed_kmph_rect, Qt.AlignmentFlag.AlignCenter, f'{self.get_speed()} km/h')
        speed_word_rect = speed_fm.boundingRect("SPEED")
        painter.setFont(speed_font)
        speed_word_rect.moveCenter(center.toPoint())
        speed_word_rect.moveBottom(round(self.speedometer_bounding_rect.bottom() - speed_kmph_rect.height()))
        painter.drawText(speed_word_rect, Qt.AlignmentFlag.AlignCenter, "SPEED")

    def start_up_animation(self):
        self.other_visible = False
        indicator_animation = QVariantAnimation(self)
        indicator_animation.setStartValue(self.width())
        indicator_animation.setEndValue(round(self.width() * 0.03))
        indicator_animation.valueChanged.connect(self.indicator_animation)
        indicator_animation.setDuration(500)
        header_animation = QVariantAnimation(self)
        header_animation.setStartValue(0)
        header_animation.setEndValue(round(self.scaled_header_border.boundingRect().height()))
        header_animation.valueChanged.connect(self.header_animation)
        header_animation.setDuration(300)
        speedometer_popup_animation = QVariantAnimation(self)
        speedometer_popup_animation.setStartValue(round(self.height() * 1.01))
        speedometer_popup_animation.setEndValue(round(self.height() * 0.2))
        speedometer_popup_animation.valueChanged.connect(self.speedometer_popup_animation)
        speedometer_popup_animation.finished.connect(self.other_popup_animation)
        speedometer_popup_animation.setDuration(500)
        speedometer_animation1 = QVariantAnimation(self)
        speedometer_animation1.setStartValue(0)
        speedometer_animation1.setEndValue(300)
        speedometer_animation1.valueChanged.connect(self.speedometer_animation)
        speedometer_animation1.setDuration(1000)
        speedometer_animation2 = QVariantAnimation(self)
        speedometer_animation2.setStartValue(300)
        speedometer_animation2.setEndValue(0)
        speedometer_animation2.valueChanged.connect(self.speedometer_animation)
        speedometer_animation2.setDuration(1000)
        check_all_state_animation = QVariantAnimation(self)
        check_all_state_animation.currentLoopChanged.connect(self.check_all_state_animation)
        check_all_state_animation.setDuration(200)
        check_all_state_animation.setLoopCount(10)
        sa_speeddial_group = QSequentialAnimationGroup(self)
        sa_speeddial_group.addAnimation(speedometer_animation1)
        sa_speeddial_group.insertPause(1, 50)
        sa_speeddial_group.addAnimation(speedometer_animation2)
        pa_group = QParallelAnimationGroup(self)
        pa_group.addAnimation(check_all_state_animation)
        pa_group.addAnimation(sa_speeddial_group)
        sa_group = QSequentialAnimationGroup(self)
        sa_group.addAnimation(indicator_animation)
        sa_group.addAnimation(header_animation)
        sa_group.addAnimation(speedometer_popup_animation)
        sa_group.addAnimation(pa_group)
        sa_group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def indicator_animation(self, pos):
        self.scaled_header_border.translate(0, -self.scaled_header_border.boundingRect().y() - self.scaled_header_border.boundingRect().height())
        self.scaled_header_inner.translate(0, -self.scaled_header_inner.boundingRect().y() - self.scaled_header_border.boundingRect().height())
        self.scaled_left_idicator.translate(-self.scaled_left_idicator.boundingRect().x(), -self.scaled_left_idicator.boundingRect().y())
        self.scaled_left_idicator.translate(pos, self.height() * 0.06)
        self.scaled_right_idicator.translate(-self.scaled_right_idicator.boundingRect().x(), -self.scaled_right_idicator.boundingRect().y())
        self.scaled_right_idicator.translate(self.width() - self.scaled_right_idicator.boundingRect().width() - self.scaled_left_idicator.boundingRect().x(), self.height() * 0.06)
        self.repaint()

    def header_animation(self, pos):
        self.scaled_header_border.translate(0, -self.scaled_header_border.boundingRect().y() - self.scaled_header_border.boundingRect().height())
        self.scaled_header_inner.translate(0, -self.scaled_header_inner.boundingRect().y() - self.scaled_header_border.boundingRect().height())
        self.scaled_header_border.translate(0, pos)
        self.scaled_header_inner.translate(0, pos)
        self.repaint()

    def speedometer_popup_animation(self, pos):
        self.speedometer_bounding_rect.moveTop(pos)
        self.repaint()

    def other_popup_animation(self):
        self.other_visible = True
        self.repaint()

    def speedometer_animation(self, val):
        self.speed = val
        self.repaint()

    def check_all_state_animation(self, loop_count):
        if loop_count == 1:
            self.show_time = 1
        elif loop_count == 2:
            self.left_indicator_color = self.indicator_color_list[1]
        elif loop_count == 3:
            self.left_indicator_color = self.indicator_color_list[0]
            self.header_border_color = 1
        elif loop_count == 4:
            self.header_border_color = 0
            self.right_indicator_color = self.indicator_color_list[1]
        elif loop_count == 5:
            self.right_indicator_color = self.indicator_color_list[0]
            self.set_horn_state(1)
            self.break_state = 1
        elif loop_count == 8:
            self.break_state = 0
            self.accelerator_state = 1
        elif loop_count == 9:
            self.accelerator_state = 0
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.LosslessImageRendering |
                               QPainter.RenderHint.Qt4CompatiblePainting | QPainter.RenderHint.NonCosmeticDefaultPen |
                               QPainter.RenderHint.TextAntialiasing, True)
        linearGradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        linearGradient.setColorAt(0.2, QColor(0, 0, 0))
        linearGradient.setColorAt(0.7, QColor(16, 0, 0))
        linearGradient.setColorAt(0.5, QColor(56, 0, 0))
        painter.setBrush(linearGradient)
        painter.drawRect(self.rect())
        self.header_painting(painter)
        self.indicators_painting(painter)
        if self.other_visible:
            self.horn_painting(painter)
            self.break_painting(painter)
            self.accelerator_painting(painter)
        self.speedometer_painting(painter)
        if self.left_sign_detected:
            painter.drawPixmap(480, 150, self.unprotected_left_image)


class DashBoard(QWidget):
    """This is a pyqt widget class to embed this dashboard to other pyqt widgets"""

    def __init__(self, parent=None):
        super(DashBoard, self).__init__(parent)
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

    def show_dashboard(self, hide_creator_button: bool = False, skip_start_screen: bool = False,
                       skip_loading_screen: bool = False):
        """This method is to show the dashboard in your window"""
        global _dash_board
        self.dash_board_widget = _DashBoardMain(self, (self.width(), self.height()), hide_creator_button, skip_start_screen, skip_loading_screen, True)
        self.dash_board_widget.move(0, 0)
        self.vlayout.addWidget(self.dash_board_widget)
        _dash_board = self.dash_board_widget


class ServerDashBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Dashboard")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.dash_board = DashBoard()
        layout.addWidget(self.dash_board)
        self.dash_board.show_dashboard(skip_start_screen=True, skip_loading_screen=True)
        self.dash_board.setFocus()
        self.tcpServer = QTcpServer(self)
        self.tcpServer.newConnection.connect(self.new_connection)
        port = 5001
        if not self.tcpServer.listen(QHostAddress.Any, port):
            print(f"Failed to start server on port {port}")
        else:
            print(f"Server started on port {port}")

    def new_connection(self):
        client_connection = self.tcpServer.nextPendingConnection()
        client_connection.readyRead.connect(self.receive_data)

    def receive_data(self):
        client_connection = self.sender()
        if client_connection:
            data = client_connection.readAll().data().decode()
            if data:
                try:
                    received_data = json.loads(data)
                    self.handle_data(received_data)
                except json.JSONDecodeError as e:
                    self.statusBar().showMessage(f"JSON decode error: {e}")
            else:
                self.statusBar().showMessage("No data received")

    def handle_data(self, received_data):
        left_sign_detected = received_data.get("left_sign_detected", False)
        current_green_light = received_data.get("current_green_light", False)
        depth_value = received_data.get("depth_value", -1)
        if current_green_light:
            self.dash_board.dash_board_widget.dash_board_design_widget.set_traffic_light_state(2)  # Green
        else:
            self.dash_board.dash_board_widget.dash_board_design_widget.set_traffic_light_state(0)  # Red
            self.dash_board.dash_board_widget.dash_board_design_widget.set_horn_state(1)  # 경적 활성화
        self.dash_board.dash_board_widget.dash_board_design_widget.set_left_sign_detected(left_sign_detected)
        if depth_value >= 100:
            self.dash_board.dash_board_widget.dash_board_design_widget.set_break_state(1)  # 브레이크 활성화
            self.dash_board.dash_board_widget.dash_board_design_widget.set_horn_state(1)  # 경적 활성화
        else:
            self.dash_board.dash_board_widget.dash_board_design_widget.set_break_state(0)  # 브레이크 비활성화
            self.dash_board.dash_board_widget.dash_board_design_widget.set_horn_state(0)  # 경적 비활성화

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.dash_board.dash_board_widget.dash_board_design_widget.indicator_triger(0)  # Left indicator
        elif event.key() == Qt.Key_Right:
            self.dash_board.dash_board_widget.dash_board_design_widget.indicator_triger(1)  # Right indicator


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerDashBoard()
    window.show()
    sys.exit(app.exec_())
