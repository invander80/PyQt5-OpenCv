from PyQt5 import QtCore, QtGui, QtWidgets

import random


#<<<<<<<<<<<<<<<<<<<<<< GradientButton >>>>>>>>>>>>>>>>>>>>>>>>#
class GradientButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, bg1=None, bg2=None, color=None):
        super(GradientButton, self).__init__(parent)

        # Minimum Goesse
        self.setMinimumSize(60, 60)

        # Auf Inhalt der Attribute ueberpruefen
        if (bg1 or bg2 or color) is not None:
            self.bg1, self.bg2, self.color = bg1, bg2, color
        else:
            self.bg1, self.bg2, self.color = "black", "lightgray", "white"

        # QVariantAnimation
        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    # StyleSheet aendern
    def _animate(self, value):
        # Base Style
        style = """
        """

        # Gradient hinzufuegen
        gradient = """
        QPushButton{
        color:{color};
        border: 1px solid black;
        border-radius:10px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, 
        stop:{value} {color2}, stop: 1.0 {color1});}
        
        QPushButton::pressed{
        background-color: qlineargradient(spread:pad, x1:0, y1:{value}, x2:{value}, y2:0, stop:0 {color2}, 
        stop:{value} {color1}, stop: 1.0 {color2});}
        """.replace("{color1}",self.bg1).replace("{color2}", self.bg2).\
            replace("{value}", str(value)).replace("{color}",self.color)
        style += gradient
        self.setStyleSheet(style)

    # Event wenn der Cursor über dem Widget ist:
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(a0)


#<<<<<<<<<<<<<<<<<<<<<< ExplodedButtton >>>>>>>>>>>>>>>>>>>>>>>>#
class ExplodedButtton(QtWidgets.QPushButton):
    def __init__(self, parent = None):
        super(ExplodedButtton, self).__init__(parent)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=40,
            endValue=60,
            duration=250
        )

        self._animationPress = QtCore.QVariantAnimation(
            self,
            valueChanged= self._animateLeftBtn,
            startValue = 60,
            endValue = 50,
            duration=250
        )

    def _animate(self, value):
        self.setIconSize(QtCore.QSize(value, value))
        self.setMinimumSize(QtCore.QSize(value, value))

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def _animateLeftBtn(self, value):
        self.setIconSize(QtCore.QSize(value, value))
        self.setMinimumSize(QtCore.QSize(value, value))

    def mousePressEvent(self, event):
        self._animationPress.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animationPress.start()
        super().enterEvent(event)

    def mouseReleaseEvent(self, event):
        self._animationPress.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animationPress.start()
        super().enterEvent(event)
