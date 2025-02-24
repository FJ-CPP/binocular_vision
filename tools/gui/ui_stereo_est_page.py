# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'page_stereo_est.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StereoEstPage(object):
  def setupUi(self, StereoEstPage):
    StereoEstPage.setObjectName("StereoEstPage")
    StereoEstPage.setEnabled(True)
    StereoEstPage.resize(1304, 998)
    font = QtGui.QFont()
    font.setPointSize(14)
    StereoEstPage.setFont(font)
    self.gridLayout = QtWidgets.QGridLayout(StereoEstPage)
    self.gridLayout.setObjectName("gridLayout")
    self.label_right_image = QtWidgets.QLabel(StereoEstPage)
    self.label_right_image.setMinimumSize(QtCore.QSize(640, 480))
    self.label_right_image.setMaximumSize(QtCore.QSize(640, 480))
    self.label_right_image.setStyleSheet(
      "#label_left_image, #label_right_image,#label_est_res {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}")
    self.label_right_image.setText("")
    self.label_right_image.setObjectName("label_right_image")
    self.gridLayout.addWidget(self.label_right_image, 0, 1, 1, 1)
    self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
    self.horizontalLayout_2.setObjectName("horizontalLayout_2")
    self.verticalLayout_2 = QtWidgets.QVBoxLayout()
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_2.addItem(spacerItem)
    self.formLayout_3 = QtWidgets.QFormLayout()
    self.formLayout_3.setObjectName("formLayout_3")
    self.label_3 = QtWidgets.QLabel(StereoEstPage)
    self.label_3.setObjectName("label_3")
    self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                self.label_3)
    self.spin_box_baseline = QtWidgets.QSpinBox(StereoEstPage)
    self.spin_box_baseline.setMaximum(9999)
    self.spin_box_baseline.setProperty("value", 6)
    self.spin_box_baseline.setObjectName("spin_box_baseline")
    self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                self.spin_box_baseline)
    self.label = QtWidgets.QLabel(StereoEstPage)
    self.label.setObjectName("label")
    self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
    self.label_4 = QtWidgets.QLabel(StereoEstPage)
    self.label_4.setObjectName("label_4")
    self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole,
                                self.label_4)
    self.label_5 = QtWidgets.QLabel(StereoEstPage)
    self.label_5.setObjectName("label_5")
    self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole,
                                self.label_5)
    self.line_coordinate = QtWidgets.QLineEdit(StereoEstPage)
    self.line_coordinate.setReadOnly(False)
    self.line_coordinate.setObjectName("line_coordinate")
    self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole,
                                self.line_coordinate)
    self.line_disparity = QtWidgets.QLineEdit(StereoEstPage)
    self.line_disparity.setReadOnly(True)
    self.line_disparity.setObjectName("line_disparity")
    self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole,
                                self.line_disparity)
    self.line_depth = QtWidgets.QLineEdit(StereoEstPage)
    self.line_depth.setMinimumSize(QtCore.QSize(120, 0))
    self.line_depth.setReadOnly(True)
    self.line_depth.setObjectName("line_depth")
    self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole,
                                self.line_depth)
    self.verticalLayout_2.addLayout(self.formLayout_3)
    spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_2.addItem(spacerItem1)
    self.horizontalLayout_2.addLayout(self.verticalLayout_2)
    spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Minimum)
    self.horizontalLayout_2.addItem(spacerItem2)
    self.verticalLayout_3 = QtWidgets.QVBoxLayout()
    self.verticalLayout_3.setObjectName("verticalLayout_3")
    spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_3.addItem(spacerItem3)
    self.verticalLayout = QtWidgets.QVBoxLayout()
    self.verticalLayout.setObjectName("verticalLayout")
    self.horizontalLayout = QtWidgets.QHBoxLayout()
    self.horizontalLayout.setObjectName("horizontalLayout")
    self.button_prev_image = QtWidgets.QPushButton(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_prev_image.setFont(font)
    self.button_prev_image.setObjectName("button_prev_image")
    self.horizontalLayout.addWidget(self.button_prev_image)
    self.button_next_image = QtWidgets.QPushButton(StereoEstPage)
    self.button_next_image.setObjectName("button_next_image")
    self.horizontalLayout.addWidget(self.button_next_image)
    self.verticalLayout.addLayout(self.horizontalLayout)
    self.button_load_images = QtWidgets.QPushButton(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_load_images.setFont(font)
    self.button_load_images.setObjectName("button_load_images")
    self.verticalLayout.addWidget(self.button_load_images)
    self.button_load_camera_params = QtWidgets.QPushButton(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_load_camera_params.setFont(font)
    self.button_load_camera_params.setObjectName("button_load_camera_params")
    self.verticalLayout.addWidget(self.button_load_camera_params)
    self.formLayout_2 = QtWidgets.QFormLayout()
    self.formLayout_2.setObjectName("formLayout_2")
    self.combo_stereo_algs = QtWidgets.QComboBox(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.combo_stereo_algs.setFont(font)
    self.combo_stereo_algs.setObjectName("combo_stereo_algs")
    self.combo_stereo_algs.addItem("")
    self.combo_stereo_algs.addItem("")
    self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                self.combo_stereo_algs)
    self.label_stereo_algs = QtWidgets.QLabel(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.label_stereo_algs.setFont(font)
    self.label_stereo_algs.setObjectName("label_stereo_algs")
    self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                self.label_stereo_algs)
    self.verticalLayout.addLayout(self.formLayout_2)
    self.button_compute = QtWidgets.QPushButton(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_compute.setFont(font)
    self.button_compute.setObjectName("button_compute")
    self.verticalLayout.addWidget(self.button_compute)
    self.button_save_results = QtWidgets.QPushButton(StereoEstPage)
    font = QtGui.QFont()
    font.setPointSize(14)
    self.button_save_results.setFont(font)
    self.button_save_results.setObjectName("button_save_results")
    self.verticalLayout.addWidget(self.button_save_results)
    self.verticalLayout_3.addLayout(self.verticalLayout)
    spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Expanding)
    self.verticalLayout_3.addItem(spacerItem4)
    self.horizontalLayout_2.addLayout(self.verticalLayout_3)
    self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
    self.label_est_res = QtWidgets.QLabel(StereoEstPage)
    self.label_est_res.setMinimumSize(QtCore.QSize(640, 480))
    self.label_est_res.setMaximumSize(QtCore.QSize(640, 480))
    self.label_est_res.setStyleSheet(
      "#label_left_image, #label_right_image,#label_est_res {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}")
    self.label_est_res.setText("")
    self.label_est_res.setObjectName("label_est_res")
    self.gridLayout.addWidget(self.label_est_res, 1, 0, 2, 1)
    self.label_left_image = QtWidgets.QLabel(StereoEstPage)
    self.label_left_image.setMinimumSize(QtCore.QSize(640, 480))
    self.label_left_image.setMaximumSize(QtCore.QSize(640, 480))
    self.label_left_image.setStyleSheet(
      "#label_left_image, #label_right_image,#label_est_res {\n"
      "    background-color: rgb(255, 255, 255);\n"
      "}")
    self.label_left_image.setText("")
    self.label_left_image.setObjectName("label_left_image")
    self.gridLayout.addWidget(self.label_left_image, 0, 0, 1, 1)

    self.retranslateUi(StereoEstPage)
    QtCore.QMetaObject.connectSlotsByName(StereoEstPage)

  def retranslateUi(self, StereoEstPage):
    _translate = QtCore.QCoreApplication.translate
    StereoEstPage.setWindowTitle(
      _translate("StereoEstPage", "Stereo Estimation Mode"))
    self.label_3.setText(_translate("StereoEstPage", "Baseline(cm)"))
    self.label.setText(_translate("StereoEstPage", "Coordinate"))
    self.label_4.setText(_translate("StereoEstPage", "Disparity"))
    self.label_5.setText(_translate("StereoEstPage", "Depth(cm)"))
    self.button_prev_image.setText(_translate("StereoEstPage", "Prev Image"))
    self.button_next_image.setText(_translate("StereoEstPage", "Next Image"))
    self.button_load_images.setText(_translate("StereoEstPage", "Load Images"))
    self.button_load_camera_params.setText(
      _translate("StereoEstPage", "Load Camera Params"))
    self.combo_stereo_algs.setItemText(0, _translate("StereoEstPage", "SGBM"))
    self.combo_stereo_algs.setItemText(
      1, _translate("StereoEstPage", "RAFT-Stereo"))
    self.label_stereo_algs.setText(
      _translate("StereoEstPage", "Stereo Algorithm"))
    self.button_compute.setText(_translate("StereoEstPage", "Compute"))
    self.button_save_results.setText(
      _translate("StereoEstPage", "Save Results"))


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  StereoEstPage = QtWidgets.QWidget()
  ui = Ui_StereoEstPage()
  ui.setupUi(StereoEstPage)
  StereoEstPage.show()
  sys.exit(app.exec_())
