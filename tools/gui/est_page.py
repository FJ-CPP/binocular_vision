from PyQt5.QtWidgets import QFileDialog
from ui_stereo_est_page import Ui_StereoEstPage
import logging
import glob
import os
import cv2

from common import UIBasePage
import bv

import sys
from pathlib import Path
import matplotlib.pyplot as plt

proj_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(str(proj_root) + '/3rdparties/RAFT-Stereo/core')
sys.path.append(str(proj_root) + '/3rdparties/RAFT-Stereo/')
from raft_stereo import RAFTStereo
from utils.utils import InputPadder
import torch
import argparse


class StereoEstPage(UIBasePage, Ui_StereoEstPage):
  def __init__(self):
    self.init_ui()
    self.init_slots()

    self.load_img_msg_box_shown = False
    self.left_images = []  # image paths
    self.right_images = []  # image paths
    self.cur_img_idx = 0
    self.camera_params = None
    self.rect_maps = None
    self.sgbm_matcher = None
    self.cur_disp_map = None
    self.cur_whole_disp_map = None
    self.min_disp = 0

  def init_ui(self):
    super().__init__()
    self.setupUi(self)
    self.setFixedSize(self.width(), self.height())
    self.move_to_center()

  def init_slots(self):
    self.button_load_images.clicked.connect(self.on_load_images_clicked)
    self.button_load_camera_params.clicked.connect(
      self.on_load_camera_params_clicked)
    self.button_prev_image.clicked.connect(self.on_prev_image_clicked)
    self.button_next_image.clicked.connect(self.on_next_image_clicked)
    self.button_compute.clicked.connect(self.on_compute_disparity_clicked)
    self.label_est_res.mouseMoveEvent = self.label_est_res_mouse_move_event
    self.button_save_results.clicked.connect(self.on_save_results_clicked)

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
    self.label_left_image.setPixmap(l2show)
    self.label_right_image.setPixmap(r2show)

  def on_prev_image_clicked(self):
    if self.cur_img_idx > 0:
      self.cur_img_idx -= 1
      self.update_image_label()

  def on_next_image_clicked(self):
    if self.cur_img_idx < len(self.left_images) - 1:
      self.cur_img_idx += 1
      self.update_image_label()

  def on_load_images_clicked(self):
    if not self.load_img_msg_box_shown:
      self.load_img_msg_box_shown = True
      self.show_msg_box(
        "Select Directory",
        "Please select a directory containing 'left' and 'right' folders to store"
        " images from the left and right cameras.\nThe images should be named as"
        " 'left_*.jpg' and 'right_*.jpg' respectively, id from 0 to xxx.\n"
        ".png images are also supported.")

    dir = QFileDialog.getExistingDirectory(self, "Select Directory",
                                           f"{proj_root}/data")

    if dir:
      logging.debug(f"[on_load_images_clicked] Selected directory: {dir}")
      is_valid_dir = self.check_image_dir(dir)
      if is_valid_dir:
        self.cur_img_idx = 0
        self.rect_maps = None
        self.sgbm_matcher = None
        self.update_image_label()
      else:
        self.show_msg_box(
          "Error",
          "The selected directory does not contain the correct-format images.")
        logging.error(
          f"[on_load_images_clicked] The selected directory does not contain the correct images."
        )

  def on_load_camera_params_clicked(self):
    cam_file = QFileDialog.getOpenFileName(self,
                                           "Select Camera Parameters File",
                                           f"{proj_root}/data")

    try:
      if cam_file:
        cam_file = cam_file[0]
        logging.debug(
          f"[on_load_camera_params_clicked] Selected camera file: {cam_file}")
        self.camera_params = bv.StereoCalibParams()
        self.camera_params.load_from_json(cam_file)
        self.rect_maps = None
      else:
        self.show_msg_box("Error", "No valid camera parameters file selected.")
    except Exception as e:
      self.show_msg_box("Error", f"Error loading camera parameters file: {e}")
      logging.error(
        f"[on_load_camera_params_clicked] Error loading camera parameters file: {e}"
      )

  def compute_disparity_sgbm(self):
    if self.rect_maps is None:
      img = cv2.imread(self.left_images[0], cv2.IMREAD_GRAYSCALE)
      rectifier = bv.BinoImageRectifier(img.shape[1], img.shape[0],
                                        self.camera_params)
      self.rect_maps = rectifier.compute_rect_maps()
      logging.info(f"[compute_disparity_sgbm] Rectification maps computed.")

    limage = cv2.imread(self.left_images[self.cur_img_idx],
                        cv2.IMREAD_GRAYSCALE)
    rimage = cv2.imread(self.right_images[self.cur_img_idx],
                        cv2.IMREAD_GRAYSCALE)
    limage_rect = cv2.remap(limage, self.rect_maps[0][0], self.rect_maps[0][1],
                            cv2.INTER_LINEAR)
    rimage_rect = cv2.remap(rimage, self.rect_maps[1][0], self.rect_maps[1][1],
                            cv2.INTER_LINEAR)
    if self.sgbm_matcher is None:
      block_size = 3
      self.sgbm_matcher = bv.StereoMatcher(min_disparity=self.min_disp,
                                           num_disparities=192 - self.min_disp,
                                           block_size=block_size,
                                           p1=8 * 3 * block_size**2,
                                           p2=32 * 3 * block_size**2,
                                           disp12_max_diff=1,
                                           pre_filter_cap=63,
                                           uniqueness_ratio=10,
                                           speckle_window_size=100,
                                           speckle_range=100,
                                           mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
      logging.info(f"[compute_disparity_sgbm] SGBM matcher initialized.")

    disp_map = self.sgbm_matcher.compute_disparity_map(limage_rect,
                                                       rimage_rect)
    disp_map_wls = self.sgbm_matcher.filter_with_wls(disp_map, limage_rect,
                                                     rimage_rect, 8000, 1.5)
    self.cur_whole_disp_map = disp_map_wls
    resized_disp_map_wls = bv.DisparityMap(
      cv2.resize(disp_map_wls.raw(),
                 (self.label_est_res.width(), self.label_est_res.height())))
    self.cur_disp_map = resized_disp_map_wls
    logging.info(f"[compute_disparity_sgbm] Disparity map computed.")
    disp_map_qpixmap = self.cvimage2qpixmap_rgb(
      self.cur_disp_map.trans2color())
    self.label_est_res.setPixmap(disp_map_qpixmap)

  def compute_disparity_raft_stereo(self):
    class RAFTArgs:
      def __init__(self):
        self.restore_ckpt = 'raft-models/raftstereo-realtime.pth'
        self.save_numpy = False
        self.mixed_precision = True
        self.valid_iters = 7
        self.hidden_dims = [128] * 3
        self.corr_implementation = "reg_cuda"
        self.shared_backbone = True
        self.corr_levels = 4
        self.corr_radius = 4
        self.n_downsample = 3
        self.context_norm = "batch"
        self.slow_fast_gru = True
        self.n_gru_layers = 2

    args = RAFTArgs()
    model = torch.nn.DataParallel(RAFTStereo(args), device_ids=[0])
    model.load_state_dict(torch.load(args.restore_ckpt))
    model = model.module
    model.to('cuda')
    model.eval()
    with torch.no_grad():
      if self.rect_maps is None:
        img = cv2.imread(self.left_images[0], cv2.IMREAD_GRAYSCALE)
        rectifier = bv.BinoImageRectifier(img.shape[1], img.shape[0],
                                          self.camera_params)
        self.rect_maps = rectifier.compute_rect_maps()
        logging.info(
          f"[compute_disparity_raft_stereo] Rectification maps computed.")

      limage = cv2.imread(self.left_images[self.cur_img_idx],
                          cv2.IMREAD_GRAYSCALE)
      rimage = cv2.imread(self.right_images[self.cur_img_idx],
                          cv2.IMREAD_GRAYSCALE)
      limage_rect = cv2.remap(limage, self.rect_maps[0][0],
                              self.rect_maps[0][1], cv2.INTER_LINEAR)
      rimage_rect = cv2.remap(rimage, self.rect_maps[1][0],
                              self.rect_maps[1][1], cv2.INTER_LINEAR)

      limage_rect = cv2.cvtColor(limage_rect, cv2.COLOR_GRAY2RGB)
      rimage_rect = cv2.cvtColor(rimage_rect, cv2.COLOR_GRAY2RGB)

      image1 = torch.from_numpy(limage_rect).permute(
        2, 0, 1).float()[None].to('cuda')
      image2 = torch.from_numpy(rimage_rect).permute(
        2, 0, 1).float()[None].to('cuda')

      padder = InputPadder(image1.shape, divis_by=32)
      image1, image2 = padder.pad(image1, image2)

      _, flow_up = model(image1,
                         image2,
                         iters=args.valid_iters,
                         test_mode=True)
      flow_up = padder.unpad(flow_up).squeeze()
      self.cur_whole_disp_map = bv.DisparityMap(
        -flow_up.cpu().numpy().squeeze())
      self.cur_disp_map = bv.DisparityMap(
        cv2.resize(-flow_up.cpu().numpy().squeeze(),
                   (self.label_est_res.width(), self.label_est_res.height())))
      disp_map_qpixmap = self.cvimage2qpixmap_rgb(
        self.cur_disp_map.trans2color())
      self.label_est_res.setPixmap(disp_map_qpixmap)

  def on_compute_disparity_clicked(self):
    if not self.camera_params:
      self.show_msg_box("Error", "No camera parameters loaded.")
      logging.error(
        "[on_compute_disparity_clicked] No camera parameters loaded.")
      return

    if not self.left_images or not self.right_images:
      self.show_msg_box("Error", "No images loaded.")
      logging.error("[on_compute_disparity_clicked] No images loaded.")
      return

    alg = self.combo_stereo_algs.currentText()
    logging.info(
      f"[on_compute_disparity_clicked] Selected disparity algorithm: {alg}")

    if alg == "SGBM":
      self.compute_disparity_sgbm()
    elif alg == "RAFT-Stereo":
      self.compute_disparity_raft_stereo()
    else:
      self.show_msg_box("Error", "Unsupported disparity algorithm.")
      logging.error(
        "[on_compute_disparity_clicked] Unsupported disparity algorithm.")

  def label_est_res_mouse_move_event(self, event):
    if not self.label_est_res.pixmap():
      return
    x = event.x()
    y = event.y()

    if x < 0 or x >= self.label_est_res.pixmap().width(
    ) or y < 0 or y >= self.label_est_res.pixmap().height():
      return

    img = self.cur_disp_map.trans2color()
    cv2.circle(img, (x, y), 4, (255, 255, 255), 1)
    disp_map_qpixmap = self.cvimage2qpixmap_rgb(img)
    self.label_est_res.setPixmap(disp_map_qpixmap)

    self.line_coordinate.setText(f"({y}, {x})")

    disp = self.cur_disp_map.raw()[y, x]
    if disp == (self.min_disp - 1) * 16:
      self.line_disparity.setText("N/A")
      self.line_depth.setText("N/A")
      return

    b = self.spin_box_baseline.value()
    fx = self.camera_params.intrins1[0, 0]
    depth = round(b * fx / disp, 3)
    logging.debug(
      f"[label_est_res_mouse_move_event] fx: {fx}, baseline: {b}, disparity: {disp}, depth: {depth}"
    )

    self.line_disparity.setText(str(disp))
    self.line_depth.setText(str(depth))

  def on_save_results_clicked(self):
    if not self.cur_disp_map:
      self.show_msg_box("Error", "No disparity map computed.")
      logging.error("[on_save_results_clicked] No disparity map computed.")
      return

    output_dir = QFileDialog.getExistingDirectory(self, "Select Directory",
                                                  ".")
    if not output_dir:
      return

    try:
      cv2.imwrite(
        os.path.join(output_dir, "disp_map.png"),
        cv2.cvtColor(self.cur_whole_disp_map.trans2color(), cv2.COLOR_RGB2BGR))
      self.cur_whole_disp_map.save_as_pfm(
        os.path.join(output_dir, "disp_map.pfm"))
      logging.info(
        f"[on_save_results_clicked] Disparity map saved to {output_dir}.")
    except Exception as e:
      self.show_msg_box("Error", f"Error saving disparity map: {e}")
      logging.error(
        f"[on_save_results_clicked] Error saving disparity map: {e}")
