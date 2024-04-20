#!/usr/bin/env python3
import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(str(proj_root))

import logging
import cv2
import os
import numpy as np
import time
import matplotlib.pyplot as plt

import bv
from common import ensure_path, MiddleBury_data_loader


def cal_error(disp_gt, disp, extra_mask=None):
  mask = disp_gt != 0
  if extra_mask is not None:
    mask = mask & extra_mask
  disp = np.nan_to_num(disp)
  disp[np.isinf(np.square(disp))] = 0

  abs_rel = np.mean(np.abs(disp_gt[mask] - disp[mask]) / disp_gt[mask])
  sq_rel = np.mean(np.square(disp_gt[mask] - disp[mask]) / disp_gt[mask])
  rmse = np.sqrt(np.mean(np.square(disp_gt[mask] - disp[mask])))

  return abs_rel, sq_rel, rmse


if __name__ == '__main__':
  cv2.setNumThreads(4)
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

  data_sets = os.listdir(f'{proj_root}/data/MiddleBury_2021')
  logging.info(f'data_sets: {data_sets}')

  abs_rel_list = []
  sq_rel_list = []
  rmse_list = []

  abs_rel_list_filtered = []
  sq_rel_list_filtered = []
  rmse_list_filtered = []

  time_list = []
  time_list_filter = []

  block_size = 3
  min_disparity = 16
  matcher = bv.StereoMatcher(min_disparity=min_disparity,
                             num_disparities=192 - min_disparity,
                             block_size=block_size,
                             p1=8 * 3 * block_size**2,
                             p2=32 * 3 * block_size**2,
                             disp12_max_diff=1,
                             pre_filter_cap=63,
                             uniqueness_ratio=10,
                             speckle_window_size=100,
                             speckle_range=100,
                             mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)

  for data_set in data_sets:
    logging.info(f'handling {data_set} ...')

    limage, rimage, disp_gt_left, intrin1, intrin2, doffs, baseline, ndisp, vmin, vmax = MiddleBury_data_loader(
      os.path.join(f'{proj_root}/data/MiddleBury_2021', data_set))

    limage = cv2.cvtColor(limage, cv2.COLOR_BGR2GRAY)
    rimage = cv2.cvtColor(rimage, cv2.COLOR_BGR2GRAY)

    logging.info('computing disparity map ...')

    start_time = time.time()

    disp_map = matcher.compute_disparity_map(limage, rimage)

    end_time = time.time()
    logging.info(f'Elapsed time: {end_time - start_time} seconds')
    time_list.append(end_time - start_time)

    disp_map_filtered = matcher.filter_with_wls(disp_map, limage, rimage, 8000,
                                                1.5)

    end_time = time.time()
    logging.info(
      f'Elapsed time with WLS Filter: {end_time - start_time} seconds')
    time_list_filter.append(end_time - start_time)

    plt.imsave(f'{output_dir}/{data_set}_gt_color.png',
               disp_gt_left.raw(),
               cmap='jet',
               vmin=vmin,
               vmax=vmax)
    plt.imsave(f'{output_dir}/{data_set}_disp_color.png',
               disp_map.raw(),
               cmap='jet',
               vmin=vmin,
               vmax=vmax)
    plt.imsave(f'{output_dir}/{data_set}_disp_filtered_color.png',
               disp_map_filtered.raw(),
               cmap='jet',
               vmin=vmin,
               vmax=vmax)

    disp_gt = disp_gt_left.raw()
    disp = disp_map.raw()
    disp_filtered = disp_map_filtered.raw()

    abs_rel_filtered, sq_rel_filtered, rmse_filtered = cal_error(
      disp_gt, disp_filtered, disp_filtered != -16.0)
    abs_rel, sq_rel, rmse = cal_error(disp_gt, disp, disp != min_disparity - 1)
    logging.info(f'Filtered AbsRel: {abs_rel_filtered}')
    logging.info(f'Filtered SqRel: {sq_rel_filtered}')
    logging.info(f'Filtered RMSE: {rmse_filtered}')
    logging.info(f'AbsRel: {abs_rel}')
    logging.info(f'SqRel: {sq_rel}')
    logging.info(f'RMSE: {rmse}')
    abs_rel_list_filtered.append(abs_rel_filtered)
    sq_rel_list_filtered.append(sq_rel_filtered)
    rmse_list_filtered.append(rmse_filtered)
    abs_rel_list.append(abs_rel)
    sq_rel_list.append(sq_rel)
    rmse_list.append(rmse)

  logging.info(f'Final Filtered AbsRel: {np.mean(abs_rel_list_filtered)}')
  logging.info(f'Final Filtered SqRel: {np.mean(sq_rel_list_filtered)}')
  logging.info(f'Final Filtered RMSE: {np.mean(rmse_list_filtered)}')
  logging.info(f'Final AbsRel: {np.mean(abs_rel_list)}')
  logging.info(f'Final SqRel: {np.mean(sq_rel_list)}')
  logging.info(f'Final RMSE: {np.mean(rmse_list)}')
  logging.info(f'Final Time: {np.mean(time_list)} seconds')
  logging.info(f'Final Time with Filter: {np.mean(time_list_filter)} seconds')
