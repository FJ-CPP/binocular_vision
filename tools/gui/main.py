#!/usr/bin/env python3

import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(str(proj_root))

import sys
from PyQt5 import QtWidgets, QtCore

from ui_home_page import Ui_HomePage
from common import UIBasePage
from calib_page import StereoCalibPage
from est_page import StereoEstPage

import logging


class BVAppRunningMode:
  NONE = -1
  CALIBRATE = 0
  STEREO_VISION = 1


class BVApp(UIBasePage, Ui_HomePage):
  def __init__(self):
    self.init_ui()
    self.init_slots()

    self.running_mode = BVAppRunningMode.NONE
    self.running_page = None

  def init_ui(self):
    super().__init__()
    self.setupUi(self)
    self.setFixedSize(self.width(), self.height())
    self.move_to_center()

  def init_slots(self):
    self.button_sel_stereo_calib_mode.toggled.connect(self.on_mode_changed)
    self.button_sel_stereo_est_mode.toggled.connect(self.on_mode_changed)
    self.button_start_mode.clicked.connect(self.on_start_clicked)

  def on_mode_changed(self, checked: bool):
    if checked:
      if self.button_sel_stereo_calib_mode.isChecked():
        logging.debug("[on_mode_changed] Calibrate Mode selected")
      elif self.button_sel_stereo_est_mode.isChecked():
        logging.debug("[on_mode_changed] StereoVision Mode selected")
      else:
        logging.error("[on_mode_changed] Unknown mode selected")

  def on_start_clicked(self):
    if self.button_sel_stereo_calib_mode.isChecked():
      self.running_mode = BVAppRunningMode.CALIBRATE
      logging.debug("[on_start_clicked] Start operations for Calibrate Mode")
    elif self.button_sel_stereo_est_mode.isChecked():
      self.running_mode = BVAppRunningMode.STEREO_VISION
      logging.debug(
        "[on_start_clicked] Start operations for StereoVision Mode")
    else:
      self.running_mode = BVAppRunningMode.NONE
      logging.error("[on_start_clicked] Unknown mode selected")

    self.update_ui()

  def update_ui(self):
    if self.running_mode == BVAppRunningMode.CALIBRATE:
      self.running_page = StereoCalibPage()
      logging.debug("[update_ui] Updated UI for Calibrate Mode")
    elif self.running_mode == BVAppRunningMode.STEREO_VISION:
      self.running_page = StereoEstPage()
      logging.debug("[update_ui] Updated UI for StereoVision Mode")
    else:
      logging.error("[update_ui] Unknown running mode")

    if self.running_page:
      self.running_page.show()
      self.running_page.close_signal.connect(self.show)
      self.hide()


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  app = QtWidgets.QApplication(sys.argv)
  ex = BVApp()
  ex.show()
  sys.exit(app.exec_())
