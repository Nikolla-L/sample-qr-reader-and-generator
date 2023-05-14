import sys

import cv2
import qrcode

from PyQt6.QtWidgets import *
from PyQt6 import uic, QtGui

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('./assets/gui/qrgui.ui', self)
        self.show()

        self.current_file = ''
        self.actionLaod.triggered.connect(self.load_image)
        self.actionSave.triggered.connect(self.save_image)

        self.pushButton.clicked.connect(self.generate_code)
        self.pushButton_2.clicked.connect(self.read_code)

        # self.actionQuit.triggered.connect(exit)
        self.actionQuit.triggered.connect(self.quit_program)

    def load_image(self):
        # options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, 'ფოტოს არჩევა', '', 'All Files (*)', '''options = options '''
        )

        if filename != '':
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(300, 300)
            self.label.setScaledContents(True)
            self.label.setPixmap(pixmap)

    def save_image(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'ფოტოს შენახვა', '', 'PNG (*.png)')

        if filename != '':
            img = self.label.pixmap()
            img.save(filename, 'PNG')

    def generate_code(self):
        qr = qrcode.QRCode(
            version = 1, error_correction = qrcode.constants.ERROR_CORRECT_L, box_size = 20, border = 2,
        )
        qr.add_data(self.textEdit.toPlainText())
        qr.make(fit=True)

        img = qr.make_image(fill_color='blue', back_color='white')
        img.save('./assets/images/current.png')
        pixmap = QtGui.QPixmap('./assets/images/current.png')
        pixmap = pixmap.scaled(300, 300)
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)

    def read_code(self):
        img =cv2.imread(self.current_file)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        print('Decoded text: ', data)
        self.textEdit.setText(data)

    def quit_program(self):
        sys.exit(0)

    
def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()

if __name__ == '__main__':
    main()