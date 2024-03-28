#!/usr/bin/env python3
import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(str(proj_root))

import logging
import cv2

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
  block_size = 3
  matcher = bv.StereoMatcher(min_disparity=16,
                             num_disparities=192 - 16,
                             block_size=block_size,
                             p1=8 * 3 * block_size**2,
                             p2=32 * 3 * block_size**2,
                             disp12_max_diff=1,
                             pre_filter_cap=63,
                             uniqueness_ratio=10,
                             speckle_window_size=100,
                             speckle_range=100,
                             mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)

  disp_map = matcher.compute_disparity_map(limage, rimage)
  """
  save disparity map as png file
  """
  logging.info('saving disparity map as png file ...')
  cv2.imwrite(f'{output_dir}/disp_map.png', disp_map.norm2int8())
  logging.info('saving disparity map as pfm file ...')
  disp_map.save_as_pfm(f'{output_dir}/disp_map.pfm')
  """
  filter disparity map with WLS filter
  """
  logging.info('filtering disparity map with WLS filter ...')
  disp_map_filtered = matcher.filter_with_wls(disp_map, limage, rimage, 8000,
                                              1.5)
  cv2.imwrite(f'{output_dir}/disp_map_wls_filtered.png',
              disp_map_filtered.raw())
  logging.info('saving filtered disparity map as pfm file ...')
  disp_map_filtered.save_as_pfm(f'{output_dir}/disp_map_wls_filtered.pfm')
  """
  filter disparity map with Median filter
  """
  logging.info('filtering disparity map with Median filter ...')
  disp_map_filtered = matcher.filter_with_median(disp_map, 7)
  cv2.imwrite(f'{output_dir}/disp_map_median_filtered.png',
              disp_map_filtered.raw())
  logging.info('saving filtered disparity map as pfm file ...')
  disp_map_filtered.save_as_pfm(f'{output_dir}/disp_map_median_filtered.pfm')
