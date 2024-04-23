# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'page_index.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HomePage(object):
  def setupUi(self, HomePage):
    HomePage.setObjectName("HomePage")
    HomePage.resize(296, 191)
    font = QtGui.QFont()
    font.setPointSize(9)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    HomePage.setFont(font)
    self.verticalLayout_2 = QtWidgets.QVBoxLayout(HomePage)
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    self.lable_app_title = QtWidgets.QLabel(HomePage)
    font = QtGui.QFont()
    font.setPointSize(13)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    self.lable_app_title.setFont(font)
    self.lable_app_title.setAlignment(QtCore.Qt.AlignCenter)
    self.lable_app_title.setObjectName("lable_app_title")
    self.verticalLayout_2.addWidget(self.lable_app_title)
    spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_2.addItem(spacerItem)
    self.horizontalLayout = QtWidgets.QHBoxLayout()
    self.horizontalLayout.setObjectName("horizontalLayout")
    spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem1)
    self.verticalLayout = QtWidgets.QVBoxLayout()
    self.verticalLayout.setObjectName("verticalLayout")
    self.button_sel_stereo_calib_mode = QtWidgets.QRadioButton(HomePage)
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    self.button_sel_stereo_calib_mode.setFont(font)
    self.button_sel_stereo_calib_mode.setObjectName(
      "button_sel_stereo_calib_mode")
    self.verticalLayout.addWidget(self.button_sel_stereo_calib_mode)
    self.button_sel_stereo_est_mode = QtWidgets.QRadioButton(HomePage)
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    self.button_sel_stereo_est_mode.setFont(font)
    self.button_sel_stereo_est_mode.setObjectName("button_sel_stereo_est_mode")
    self.verticalLayout.addWidget(self.button_sel_stereo_est_mode)
    spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout.addItem(spacerItem2)
    self.button_start_mode = QtWidgets.QPushButton(HomePage)
    font = QtGui.QFont()
    font.setPointSize(14)
    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
    self.button_start_mode.setFont(font)
    self.button_start_mode.setObjectName("button_start_mode")
    self.verticalLayout.addWidget(self.button_start_mode)
    self.horizontalLayout.addLayout(self.verticalLayout)
    spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem3)
    self.verticalLayout_2.addLayout(self.horizontalLayout)

    self.retranslateUi(HomePage)
    QtCore.QMetaObject.connectSlotsByName(HomePage)

  def retranslateUi(self, HomePage):
    _translate = QtCore.QCoreApplication.translate
    HomePage.setWindowTitle(_translate("HomePage", "BincularVisionApp"))
    self.lable_app_title.setText(
      _translate("HomePage", "Select your running modes"))
    self.button_sel_stereo_calib_mode.setText(
      _translate("HomePage", "Stereo Calibration"))
    self.button_sel_stereo_est_mode.setText(
      _translate("HomePage", "Stereo Estimation"))
    self.button_start_mode.setText(_translate("HomePage", "Start"))


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  HomePage = QtWidgets.QWidget()
  ui = Ui_HomePage()
  ui.setupUi(HomePage)
  HomePage.show()
  sys.exit(app.exec_())
