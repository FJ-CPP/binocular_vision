#!/usr/bin/env python3
import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(str(proj_root))

import logging
import cv2
import numpy as np
import os

import bv
from common import ensure_path, MiddleBury_data_loader

if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logging.info('running stereo matching ...')

  output_dir = __file__.replace('.py', '_output')
  ensure_path(output_dir)
  """
  load stereo image pair and calibration data
  """
  logging.info('loading stereo image pair and calibration data ...')
  limage, rimage, intrin1, intrin2, doffs, baseline, ndisp, vmin, vmax = MiddleBury_data_loader(
    f'{proj_root}/data/stereo_match/MiddleBury_2021/artroom1')
  """
  compute disparity map
  """
  logging.info('computing disparity map ...')
  matcher = bv.StereoMatcher(min_disparity=0,
                             num_disparities=ndisp,
                             block_size=3,
                             p1=8 * 3 * 3**2,
                             p2=32 * 3 * 3**2,
                             disp12_max_diff=1,
                             pre_filter_cap=63,
                             uniqueness_ratio=10,
                             speckle_window_size=100,
                             speckle_range=32,
                             mode=cv2.STEREO_SGBM_MODE_SGBM)

  disp_map = matcher.compute_disparity_map(limage, rimage)
  """
  save disparity map as png file
  """
  logging.info('saving disparity map as png file ...')
  cv2.imwrite(f'{output_dir}/disp_map.png', disp_map.norm2int8())
  """
  save disparity map as pfm file
  """
  logging.info('saving disparity map as pfm file ...')
  disp_map.save_as_pfm(f'{output_dir}/disp_map.pfm')
