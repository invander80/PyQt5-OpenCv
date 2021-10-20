from ui.main.ui_main import *
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot, QEvent)

class Functions(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Functions, self).__init__()
        self.setupUi(self)

    # ------------ Titelbar entfernen und Schatten setzen ------------ #
    def removeTitleBar(self):
        #=> Title enfernen
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #=> Schatten
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(Qt.black)

        self.setGraphicsEffect(shadow)

    # ------------ EVENT: Fenster bewegen ------------ #
    def moveWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
           # self.imageLbl.update()

    # ------------ EVENT: Fenster beim druecken der linken Maustaste ------------ #
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    # ------------ Fenster vergroessern / auf Normal setzen ------------ #
    def on_maxBtn_clicked(self):
        if self.maxBtn.isChecked():
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()
        else:
            self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.showNormal()

    # ------------ Animation fuer die OptionBar (Eigenschaften) ------------ #
    @QtCore.pyqtSlot()
    def on_optionBtn_clicked(self, start=0, end=300):
        if self.optionBtn.isChecked():
            self._animate = QtCore.QPropertyAnimation(self.optionBar, b"minimumWidth")
            self._animate.setDuration(500)
            self._animate.setEndValue(end)
            self._animate.setEasingCurve(QtCore.QEasingCurve.OutSine)
            self._animate.start()
        else:
            self._animate = QtCore.QPropertyAnimation(self.optionBar, b"minimumWidth")
            self._animate.setDuration(500)
            self._animate.setEndValue(start)
            self._animate.setEasingCurve(QtCore.QEasingCurve.InSine)
            self._animate.start()

    # ------------ Timer fuer die aktualisierung fuer den Pfad ------------ #
    def setTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(100)
        if self.timerCount == 1:
            self.timerCount = 0

    def on_timer(self):
        if self.timerCount < 1:
            self.pathLbl.setText(self.getPath())
            self.imageLbl.update()
            self.timerCount += 1