# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'page_calib.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StereoCalibPage(object):
  def setupUi(self, StereoCalibPage):
    StereoCalibPage.setObjectName("StereoCalibPage")
    StereoCalibPage.setEnabled(True)
    StereoCalibPage.resize(1326, 879)
    self.verticalLayout_3 = QtWidgets.QVBoxLayout(StereoCalibPage)
    self.verticalLayout_3.setObjectName("verticalLayout_3")
    spacerItem = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_3.addItem(spacerItem)
    self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_5.setObjectName("horizontalLayout_5")
    spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_5.addItem(spacerItem1)
    self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_4.setObjectName("horizontalLayout_4")
    self.label_left_image = QtWidgets.QLabel(StereoCalibPage)
    self.label_left_image.setMinimumSize(QtCore.QSize(640, 480))
    self.label_left_image.setMaximumSize(QtCore.QSize(640, 480))
    self.label_left_image.setStyleSheet(
      "#label_left_image, #label_right_image {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}")
    self.label_left_image.setText("")
    self.label_left_image.setObjectName("label_left_image")
    self.horizontalLayout_4.addWidget(self.label_left_image)
    spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_4.addItem(spacerItem2)
    self.label_right_image = QtWidgets.QLabel(StereoCalibPage)
    self.label_right_image.setMinimumSize(QtCore.QSize(640, 480))
    self.label_right_image.setMaximumSize(QtCore.QSize(640, 480))
    self.label_right_image.setStyleSheet(
      "#label_left_image, #label_right_image {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}")
    self.label_right_image.setText("")
    self.label_right_image.setObjectName("label_right_image")
    self.horizontalLayout_4.addWidget(self.label_right_image)
    self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
    spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_5.addItem(spacerItem3)
    self.verticalLayout_3.addLayout(self.horizontalLayout_5)
    spacerItem4 = QtWidgets.QSpacerItem(17, 21, QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_3.addItem(spacerItem4)
    self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_3.setObjectName("horizontalLayout_3")
    spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem5)
    self.horizontalLayout = QtWidgets.QHBoxLayout()
    self.horizontalLayout.setObjectName("horizontalLayout")
    self.formLayout = QtWidgets.QFormLayout()
    self.formLayout.setObjectName("formLayout")
    self.label_chessboard_w = QtWidgets.QLabel(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_chessboard_w.setFont(font)
    self.label_chessboard_w.setObjectName("label_chessboard_w")
    self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                              self.label_chessboard_w)
    self.spinbox_chessboard_w = QtWidgets.QSpinBox(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.spinbox_chessboard_w.setFont(font)
    self.spinbox_chessboard_w.setProperty("value", 9)
    self.spinbox_chessboard_w.setObjectName("spinbox_chessboard_w")
    self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                              self.spinbox_chessboard_w)
    self.label_chessboard_h = QtWidgets.QLabel(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_chessboard_h.setFont(font)
    self.label_chessboard_h.setObjectName("label_chessboard_h")
    self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole,
                              self.label_chessboard_h)
    self.spinbox_chessboard_h = QtWidgets.QSpinBox(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.spinbox_chessboard_h.setFont(font)
    self.spinbox_chessboard_h.setProperty("value", 6)
    self.spinbox_chessboard_h.setObjectName("spinbox_chessboard_h")
    self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole,
                              self.spinbox_chessboard_h)
    self.label_grid_size = QtWidgets.QLabel(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_grid_size.setFont(font)
    self.label_grid_size.setObjectName("label_grid_size")
    self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole,
                              self.label_grid_size)
    self.double_spinbox_grid_size = QtWidgets.QDoubleSpinBox(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.double_spinbox_grid_size.setFont(font)
    self.double_spinbox_grid_size.setDecimals(2)
    self.double_spinbox_grid_size.setProperty("value", 1.0)
    self.double_spinbox_grid_size.setObjectName("double_spinbox_grid_size")
    self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole,
                              self.double_spinbox_grid_size)
    self.horizontalLayout.addLayout(self.formLayout)
    spacerItem6 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout.addItem(spacerItem6)
    self.formLayout_2 = QtWidgets.QFormLayout()
    self.formLayout_2.setObjectName("formLayout_2")
    self.label_epipolar_error = QtWidgets.QLabel(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_epipolar_error.setFont(font)
    self.label_epipolar_error.setObjectName("label_epipolar_error")
    self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole,
                                self.label_epipolar_error)
    self.output_epi_err = QtWidgets.QLineEdit(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.output_epi_err.setFont(font)
    self.output_epi_err.setReadOnly(True)
    self.output_epi_err.setObjectName("output_epi_err")
    self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole,
                                self.output_epi_err)
    self.output_calib_rms = QtWidgets.QLineEdit(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.output_calib_rms.setFont(font)
    self.output_calib_rms.setReadOnly(True)
    self.output_calib_rms.setObjectName("output_calib_rms")
    self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                self.output_calib_rms)
    self.label_calib_rms = QtWidgets.QLabel(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_calib_rms.setFont(font)
    self.label_calib_rms.setObjectName("label_calib_rms")
    self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                self.label_calib_rms)
    self.label_calib_results = QtWidgets.QLabel(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_calib_results.setFont(font)
    self.label_calib_results.setObjectName("label_calib_results")
    self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole,
                                self.label_calib_results)
    self.text_calib_results = QtWidgets.QTextBrowser(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(9)
    self.text_calib_results.setFont(font)
    self.text_calib_results.setObjectName("text_calib_results")
    self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole,
                                self.text_calib_results)
    self.horizontalLayout.addLayout(self.formLayout_2)
    self.horizontalLayout_3.addLayout(self.horizontalLayout)
    spacerItem7 = QtWidgets.QSpacerItem(25, 275,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem7)
    self.verticalLayout_2 = QtWidgets.QVBoxLayout()
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_2.setObjectName("horizontalLayout_2")
    self.button_prev_image = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_prev_image.setFont(font)
    self.button_prev_image.setObjectName("button_prev_image")
    self.horizontalLayout_2.addWidget(self.button_prev_image)
    self.button_next_image = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_next_image.setFont(font)
    self.button_next_image.setObjectName("button_next_image")
    self.horizontalLayout_2.addWidget(self.button_next_image)
    self.verticalLayout_2.addLayout(self.horizontalLayout_2)
    self.verticalLayout = QtWidgets.QVBoxLayout()
    self.verticalLayout.setObjectName("verticalLayout")
    self.button_load_images = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_load_images.setFont(font)
    self.button_load_images.setObjectName("button_load_images")
    self.verticalLayout.addWidget(self.button_load_images)
    self.button_display_calib_images = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_display_calib_images.setFont(font)
    self.button_display_calib_images.setObjectName(
      "button_display_calib_images")
    self.verticalLayout.addWidget(self.button_display_calib_images)
    self.button_display_raw_images = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_display_raw_images.setFont(font)
    self.button_display_raw_images.setObjectName("button_display_raw_images")
    self.verticalLayout.addWidget(self.button_display_raw_images)
    self.button_calibrate = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_calibrate.setFont(font)
    self.button_calibrate.setObjectName("button_calibrate")
    self.verticalLayout.addWidget(self.button_calibrate)
    self.button_save_results = QtWidgets.QPushButton(StereoCalibPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_save_results.setFont(font)
    self.button_save_results.setObjectName("button_save_results")
    self.verticalLayout.addWidget(self.button_save_results)
    spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout.addItem(spacerItem8)
    self.verticalLayout_2.addLayout(self.verticalLayout)
    self.horizontalLayout_3.addLayout(self.verticalLayout_2)
    spacerItem9 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem9)
    spacerItem10 = QtWidgets.QSpacerItem(40, 20,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem10)
    spacerItem11 = QtWidgets.QSpacerItem(40, 20,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem11)
    spacerItem12 = QtWidgets.QSpacerItem(40, 20,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem12)
    spacerItem13 = QtWidgets.QSpacerItem(40, 20,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem13)
    spacerItem14 = QtWidgets.QSpacerItem(40, 20,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem14)
    spacerItem15 = QtWidgets.QSpacerItem(40, 20,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem15)
    spacerItem16 = QtWidgets.QSpacerItem(24, 275,
                                         QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_3.addItem(spacerItem16)
    self.verticalLayout_3.addLayout(self.horizontalLayout_3)
    spacerItem17 = QtWidgets.QSpacerItem(20, 35, QtWidgets.QSizePolicy.Minimum,
                                         QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_3.addItem(spacerItem17)

    self.retranslateUi(StereoCalibPage)
    QtCore.QMetaObject.connectSlotsByName(StereoCalibPage)

  def retranslateUi(self, StereoCalibPage):
    _translate = QtCore.QCoreApplication.translate
    StereoCalibPage.setWindowTitle(
      _translate("StereoCalibPage", "Stereo Calibration Mode"))
    self.label_chessboard_w.setText(
      _translate("StereoCalibPage", "Chessboard Width"))
    self.label_chessboard_h.setText(
      _translate("StereoCalibPage", "Chessboard Height"))
    self.label_grid_size.setText(_translate("StereoCalibPage",
                                            "Grid Size(cm)"))
    self.label_epipolar_error.setText(
      _translate("StereoCalibPage", "Epipolar Error"))
    self.label_calib_rms.setText(_translate("StereoCalibPage", "Calib RMS"))
    self.label_calib_results.setText(
      _translate("StereoCalibPage", "Calib Results:"))
    self.text_calib_results.setHtml(
      _translate(
        "StereoCalibPage",
        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"
      ))
    self.button_prev_image.setText(
      _translate("StereoCalibPage", " Prev Image "))
    self.button_next_image.setText(
      _translate("StereoCalibPage", " Next Image "))
    self.button_load_images.setText(
      _translate("StereoCalibPage", "Load Images"))
    self.button_display_calib_images.setText(
      _translate("StereoCalibPage", "Display Calib Image"))
    self.button_display_raw_images.setText(
      _translate("StereoCalibPage", "Display Raw Image "))
    self.button_calibrate.setText(_translate("StereoCalibPage", "Calibrate"))
    self.button_save_results.setText(
      _translate("StereoCalibPage", "Save Results"))


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  StereoCalibPage = QtWidgets.QWidget()
  ui = Ui_StereoCalibPage()
  ui.setupUi(StereoCalibPage)
  StereoCalibPage.show()
  sys.exit(app.exec_())
