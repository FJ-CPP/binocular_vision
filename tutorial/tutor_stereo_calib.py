#!/usr/bin/env python3
import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(str(proj_root))

import logging
import cv2
import numpy as np
import glob

import bv
from common import ensure_path

if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logging.info('running stereo calibration ...')

  left_images = glob.glob(
    f'{proj_root}/data/calib/opencv_calib_data/left??.jpg')
  right_images = glob.glob(
    f'{proj_root}/data/calib/opencv_calib_data/right??.jpg')

  left_images.sort()
  right_images.sort()

  calibrator = bv.StereoCalibrator(border_size=(9, 6), square_size=1.0)
  # res = calibrator.stereo_calib(left_images, right_images, True)
  cam_params, calib_rms, epipolar_err, corners, valid_image_pairs = calibrator.stereo_calib(
    left_images, right_images, True)
  logging.info(f'calibration rms: {calib_rms}')
  logging.info(f'epipolar error: {epipolar_err}')

  output_dir = __file__.replace('.py', '_output')
  ensure_path(output_dir)

  # save calibration result to json file
  logging.info('saving calibration result to file ...')
  cam_params.save_as_json(f'{output_dir}/calib_params.json')

  # draw chessboard corners
  images = [[], []]
  for i in valid_image_pairs:
    images[0].append(cv2.imread(left_images[i], cv2.IMREAD_COLOR))
    images[1].append(cv2.imread(right_images[i], cv2.IMREAD_COLOR))

  logging.info('drawing chessboard corners ...')
  for i in valid_image_pairs:
    limage = images[0][i].copy()
    rimage = images[1][i].copy()
    limage_gray = cv2.cvtColor(limage, cv2.COLOR_BGR2GRAY)
    rimage_gray = cv2.cvtColor(rimage, cv2.COLOR_BGR2GRAY)
    cv2.drawChessboardCorners(limage, calibrator.border_size, corners[0][i],
                              True)
    cv2.drawChessboardCorners(rimage, calibrator.border_size, corners[1][i],
                              True)
    cv2.imwrite(f'{output_dir}/corners_{i}_l.png', limage)
    cv2.imwrite(f'{output_dir}/corners_{i}_r.png', rimage)

  # saving unrectified images
  logging.info('saving unrectified images ...')
  for i in range(len(left_images)):
    limage = images[0][i].copy()
    rimage = images[1][i].copy()
    concat = np.hstack((limage, rimage))
    for j in range(0, concat.shape[0], 30):
      cv2.line(concat, (0, j), (concat.shape[1], j), (0, 255, 0), 1, 8)
    cv2.imwrite(f'{output_dir}/unrectified_{i}.png', concat)

  # rectify images and save to file
  logging.info('rectifying images ...')
  rectifier = bv.BinoImageRectifier(images[0][0].shape[1],
                                    images[0][0].shape[0], cam_params)
  rect_maps = rectifier.compute_rect_maps()
  for i in range(len(left_images)):
    limage = images[0][i].copy()
    rimage = images[1][i].copy()

    limage_rect = cv2.remap(limage, rect_maps[0][0], rect_maps[0][1],
                            cv2.INTER_LINEAR)
    rimage_rect = cv2.remap(rimage, rect_maps[1][0], rect_maps[1][1],
                            cv2.INTER_LINEAR)
    concat = np.hstack((limage_rect, rimage_rect))

    for j in range(0, concat.shape[0], 30):
      cv2.line(concat, (0, j), (concat.shape[1], j), (0, 255, 0), 1, 8)
    cv2.imwrite(f'{output_dir}/rectified_{i}.png', concat)
