from data.functions import *
import cv2, imutils, os


class MainWindow(Functions):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.removeTitleBar()
        self.appName.mouseMoveEvent = self.moveWindow

        self.maxBtn.clicked.connect(self.on_maxBtn_clicked)
        self.optionBtn.clicked.connect(self.on_optionBtn_clicked)
        self.saveBtn.clicked.connect(self.saveFile)

        self.openBtn.clicked.connect(self.openImage)

        self.blurSlide.valueChanged['int'].connect(self.blurChanged)
        self.brightSlide.valueChanged['int'].connect(self.brightChanged)

        self.clrMapCombo.currentIndexChanged.connect(self.clrMapChanged)

        self.widthHeightBtn.clicked.connect(self.setPicSize)

        self.filename = None
        self.tmp = None
        self.image = None

        self.blur_val = 0
        self.bright_val = 0
        self.clr_val = 0

        self.timerCount = 0

    def getPath(self):
        return os.path.abspath(self.filename)

    # ------------ Groesse des akutellen Bildes ------------ #
    def picProperties(self, x):
        lst = [n for n in self.image.shape]
        return lst[x]

    # ------------ Groesse des Bildes veraendern ------------ #
    def setPicSize(self):
        if (self.breite.text() and self.hoehe.text()) != "":
            self.imageLbl.setMaximumSize(QtCore.QSize(int(self.breite.text()), int(self.hoehe.text())))

    # ------------ Bilddatei oeffnen ------------ #
    def openImage(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.image = cv2.imread(self.filename)
        self.setImage(self.image)

    # ------------ Bild setzen ------------ #
    def setImage(self, image):
        self.tmp = image
        image = imutils.resize(image, height=self.picProperties(0), width=self.picProperties(1))
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
        self.imageLbl.setPixmap(QtGui.QPixmap.fromImage(image))
        self.setTimer()

    # ------------ Blur Slider ------------ #
    def blurChanged(self, value):
        if self.filename is not None:
            self.blur_val = value
            self.blurValLbl.setText(str(value))
            self.update()

    # ------------ Blur-Werte aendern ------------ #
    def blur(self, img, value):
        size = (value + 1, value + 1)
        return cv2.blur(img, size)

    # ------------ Helligkeit Slider------------ #
    def brightChanged(self, value):
        if self.filename is not None:
            self.bright_val = value
            self.brightValLbl.setText(str(value))
            self.update()

    # ------------ Helligkeit-Werte aendern ------------ #
    def brightness(self, img, value):
        return cv2.convertScaleAbs(img, beta=value)

    # ------------ Colormap ComboBox------------ #
    def clrMapChanged(self, value):
        if self.filename is not None:
            self.clr_val = value
            self.update()

    # ------------ Colormap aendern ------------ #
    def clrMap(self, image, value):
        if self.clr_val == 0:
            return cv2.cvtColor(image, cv2.IMREAD_COLOR)
        else:
            return cv2.applyColorMap(image, eval("cv2.COLORMAP_{CLR}".replace("{CLR}", self.clrMapCombo.itemText(value).upper())))

    # ------------ Update, wenn die Slider benutzt werden ------------ #
    def update(self):
        img = self.brightness(self.image, self.bright_val)
        img = self.blur(img, self.blur_val)
        img = self.clrMap(img, self.clr_val)
        self.setImage(img)

    def saveFile(self):
        if self.filename is not None:
            cv2.imwrite(self.filename, self.tmp)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()