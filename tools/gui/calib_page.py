from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import logging
import glob
import os

import cv2

from common import UIBasePage
from ui_calib_page import Ui_StereoCalibPage
import bv
import json


class StereoCalibPage(UIBasePage, Ui_StereoCalibPage):
  def __init__(self):
    self.init_ui()
    self.init_slots()

    self.load_img_msg_box_shown = False
    self.left_images = []  # image paths
    self.right_images = []  # image paths
    self.cur_img_idx = 0
    self.prev_chessboard_size = None
    self.prev_grid_size = None
    self.prev_cam_params = None
    self.prev_corners = None
    self.prev_valid_image_pairs = None
    self.display_calib_res = False

  def init_ui(self):
    super().__init__()
    self.setupUi(self)
    self.setFixedSize(self.width(), self.height())
    self.move_to_center()
    self.clean_focus()

  def init_slots(self):
    self.button_load_images.clicked.connect(self.on_load_images_clicked)
    self.button_prev_image.clicked.connect(self.on_prev_image_clicked)
    self.button_next_image.clicked.connect(self.on_next_image_clicked)
    self.button_calibrate.clicked.connect(self.on_calibrate_clicked)
    self.button_save_results.clicked.connect(self.on_save_results_clicked)
    self.button_display_calib_images.clicked.connect(
      self.on_display_calib_images_clicked)
    self.button_display_raw_images.clicked.connect(
      self.on_display_raw_images_clicked)

  def closeEvent(self, event):
    self.close_signal.emit()
    super().closeEvent(event)

  def check_image_dir(self, dir):
    left_imgs = glob.glob(os.path.join(dir, "left", "left_*.png")) + glob.glob(
      os.path.join(dir, "left", "left_*.jpg"))
    right_imgs = glob.glob(os.path.join(
      dir, "right", "right_*.png")) + glob.glob(
        os.path.join(dir, "right", "right_*.jpg"))

    if not left_imgs or not right_imgs:
      logging.info(
        f"[check_image_dir] No images found in the directory: {dir}")
      return False

    left_imgs.sort()
    right_imgs.sort()

    if len(left_imgs) != len(right_imgs):
      return False

    for left_img, right_img in zip(left_imgs, right_imgs):
      if os.path.basename(left_img).split("_")[1] != os.path.basename(
          right_img).split("_")[1]:
        logging.error(
          f"[check_image_dir] Image names do not match: {left_img}, {right_img}"
        )
        return False

      if cv2.imread(left_img).shape != cv2.imread(right_img).shape:
        logging.error(
          f"[check_image_dir] Image shapes do not match: {left_img}, {right_img}"
        )
        return False

    self.left_images = left_imgs
    self.right_images = right_imgs
    return True

  def update_image_label(self):
    left_img = cv2.imread(self.left_images[self.cur_img_idx],
                          cv2.IMREAD_GRAYSCALE)
    right_img = cv2.imread(self.right_images[self.cur_img_idx],
                           cv2.IMREAD_GRAYSCALE)
    # resize images to fit the label
    left_img = cv2.resize(
      left_img,
      (self.label_left_image.width(), self.label_left_image.height()))
    right_img = cv2.resize(
      right_img,
      (self.label_right_image.width(), self.label_right_image.height()))
    l2show = self.cvimage2qpixmap_gray(left_img)
    r2show = self.cvimage2qpixmap_gray(right_img)

    if self.display_calib_res and self.prev_corners:
      if self.cur_img_idx in self.prev_valid_image_pairs:
        logging.debug(
          f'left image corners: {self.prev_corners[0][self.cur_img_idx]}')
        logging.debug(
          f'right image corners: {self.prev_corners[1][self.cur_img_idx]}')
        left_img = cv2.cvtColor(left_img, cv2.COLOR_GRAY2BGR)
        right_img = cv2.cvtColor(right_img, cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(left_img, self.prev_chessboard_size,
                                  self.prev_corners[0][self.cur_img_idx], True)
        cv2.drawChessboardCorners(right_img, self.prev_chessboard_size,
                                  self.prev_corners[1][self.cur_img_idx], True)
        l2show = self.cv2image2qpixmap_rgb(left_img)
        r2show = self.cv2image2qpixmap_rgb(right_img)
      else:
        # display raw images if no corners found
        self.show_msg_box(
          "Warning",
          f"No corners found for image {self.left_images[self.cur_img_idx]}")

    self.label_left_image.setPixmap(l2show)
    self.label_right_image.setPixmap(r2show)

  def on_load_images_clicked(self):
    if not self.load_img_msg_box_shown:
      self.load_img_msg_box_shown = True
      self.show_msg_box(
        "Select Directory",
        "Please select a directory containing 'left' and 'right' folders to store"
        " images from the left and right cameras.\nThe images should be named as"
        " 'left_*.jpg' and 'right_*.jpg' respectively, id from 0 to xxx.\n"
        ".png images are also supported.")

    dir = QFileDialog.getExistingDirectory(self, "Select Directory", ".")

    if dir:
      logging.debug(f"[on_load_images_clicked] Selected directory: {dir}")
      is_valid_dir = self.check_image_dir(dir)
      if is_valid_dir:
        self.cur_img_idx = 0
        self.prev_cam_params = None
        self.prev_corners = None
        self.prev_valid_image_pairs = None
        self.update_image_label()
      else:
        self.show_msg_box(
          "Error",
          "The selected directory does not contain the correct-format images.")
        logging.error(
          f"[on_load_images_clicked] The selected directory does not contain the correct images."
        )

  def on_prev_image_clicked(self):
    if self.cur_img_idx > 0:
      self.cur_img_idx -= 1
      self.update_image_label()

  def on_next_image_clicked(self):
    if self.cur_img_idx < len(self.left_images) - 1:
      self.cur_img_idx += 1
      self.update_image_label()

  def on_calibrate_clicked(self):
    if not self.left_images or not self.right_images:
      self.show_msg_box("Error", "Please load images first.")
      return

    chessboard_w = self.spinbox_chessboard_w.value()
    chessboard_h = self.spinbox_chessboard_h.value()
    grid_size = self.double_spinbox_grid_size.value()

    if chessboard_w <= 0 or chessboard_h <= 0 or grid_size <= 0:
      self.show_msg_box("Error", "Invalid chessboard size or grid size.")
      return

    logging.debug(
      f"[on_calibrate_clicked] Chessboard size: {chessboard_w}x{chessboard_h},"
      f" Grid size: {grid_size}")

    try:
      calibrator = bv.StereoCalibrator(border_size=(chessboard_w,
                                                    chessboard_h),
                                       square_size=grid_size)
      cam_params, calib_rms, epipolar_err, corners, valid_image_pairs = calibrator.stereo_calib(
        self.left_images,
        self.right_images,
        True,
        image_resize=(self.label_left_image.width(),
                      self.label_left_image.height()))
    except Exception as e:
      self.show_msg_box("Error", f"Error occurred during calibration: {e}")
      logging.error(
        f"[on_calibrate_clicked] Error occurred during calibration: {e}")
      return

    logging.info(f'calibration rms: {calib_rms}')
    logging.info(f'epipolar error: {epipolar_err}')
    logging.info(f'valid image pairs: {valid_image_pairs}')

    self.output_calib_rms.setText(str(calib_rms))
    self.output_epi_err.setText(str(epipolar_err))
    self.text_calib_results.setPlainText(cam_params.save_as_str())
    self.prev_chessboard_size = (chessboard_w, chessboard_h)
    self.prev_grid_size = grid_size
    self.prev_cam_params = cam_params
    self.prev_corners = corners
    self.prev_valid_image_pairs = valid_image_pairs

  def on_save_results_clicked(self):
    if not self.prev_cam_params:
      self.show_msg_box("Error", "Please calibrate first.")
      return

    output_dir = QFileDialog.getExistingDirectory(self, "Select Directory",
                                                  ".")
    if output_dir:
      self.prev_cam_params.save_as_json(
        os.path.join(output_dir, "calib_params.json"))

  def on_display_calib_images_clicked(self):
    if not self.prev_cam_params:
      self.show_msg_box("Error", "Please calibrate first.")
      return

    self.display_calib_res = True
    self.update_image_label()

  def on_display_raw_images_clicked(self):
    self.display_calib_res = False
    self.update_image_label()
