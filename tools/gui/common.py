from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QHBoxLayout


class UIBasePage(QtWidgets.QWidget):
  close_signal = QtCore.pyqtSignal()

  def __init__(self):
    super().__init__()

  def move_to_center(self):
    self.move((QtWidgets.QApplication.desktop().width() - self.width()) // 2,
              (QtWidgets.QApplication.desktop().height() - self.height()) // 2)

  def clean_focus(self):
    self.setFocus()

  def show_msg_box(self, title, text):
    class CustomDialog(QDialog):
      def __init__(self, title, text, parent=None):
        super(CustomDialog, self).__init__(parent)

        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        label = QLabel(text)
        label.setMargin(10)
        label.setFont(QFont("Sans Serif", 12))
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        button_layout.addStretch(1)

        button = QPushButton("OK")
        button.setFont(QFont("Sans Serif", 12))
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button_layout.addWidget(button)

        button.clicked.connect(self.accept)

        self.setLayout(layout)

    dialog = CustomDialog(title, text, self)
    dialog.exec_()

  def cvimage2qpixmap_gray(self, cv_img):
    h, w = cv_img.shape
    bytes_per_line = w
    q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
    return QPixmap(q_img)

  def cvimage2qpixmap_rgb(self, cv_img):
    h, w, c = cv_img.shape
    bytes_per_line = w * c
    q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap(q_img)
