#!/usr/bin/env python3
import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(str(proj_root))

import logging
import cv2
import os
import numpy as np
import torch
import time
import matplotlib.pyplot as plt

import bv
from common import ensure_path, MiddleBury_data_loader

sys.path.append(str(proj_root) + '/3rdparties/RAFT-Stereo/core')
sys.path.append(str(proj_root) + '/3rdparties/RAFT-Stereo/')
from raft_stereo import RAFTStereo
from utils.utils import InputPadder


def cal_error(disp_gt, disp, extra_mask=None):
  mask = disp_gt != 0
  if extra_mask is not None:
    mask = mask & extra_mask

  abs_rel = np.mean(np.abs(disp_gt[mask] - disp[mask]) / disp_gt[mask])
  sq_rel = np.mean(np.square(disp_gt[mask] - disp[mask]) / disp_gt[mask])
  rmse = np.sqrt(np.mean(np.square(disp_gt[mask] - disp[mask])))

  return abs_rel, sq_rel, rmse


class RAFTArgs:
  def __init__(self):
    # self.restore_ckpt = os.path.join(proj_root, 'tools/gui/raft-models/raftstereo-middlebury.pth')
    self.restore_ckpt = os.path.join(
      proj_root, 'tools/gui/raft-models/raftstereo-eth3d.pth')
    self.save_numpy = False
    self.mixed_precision = False
    self.valid_iters = 32
    self.hidden_dims = [128] * 3
    self.corr_implementation = "alt"
    self.shared_backbone = False
    self.corr_levels = 4
    self.corr_radius = 4
    self.n_downsample = 2
    self.context_norm = "batch"
    self.slow_fast_gru = False
    self.n_gru_layers = 3


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

  data_sets = os.listdir(f'{proj_root}/data/MiddleBury_2021')
  logging.info(f'data_sets: {data_sets}')

  abs_rel_list = []
  sq_rel_list = []
  rmse_list = []
  time_list = []

  args = RAFTArgs()
  model = torch.nn.DataParallel(RAFTStereo(args), device_ids=[0])
  model.load_state_dict(torch.load(args.restore_ckpt))
  model = model.module
  model.to('cuda')
  model.eval()
  with torch.no_grad():
    for data_set in data_sets:
      logging.info(f'handling {data_set} ...')

      limage, rimage, disp_gt_left, intrin1, intrin2, doffs, baseline, ndisp, vmin, vmax = MiddleBury_data_loader(
        os.path.join(f'{proj_root}/data/MiddleBury_2021', data_set))

      logging.info('computing disparity map ...')
      start_time = time.time()
      image1 = torch.from_numpy(limage).permute(2, 0,
                                                1).float()[None].to('cuda')
      image2 = torch.from_numpy(rimage).permute(2, 0,
                                                1).float()[None].to('cuda')

      padder = InputPadder(image1.shape, divis_by=32)
      image1, image2 = padder.pad(image1, image2)

      _, flow_up = model(image1,
                         image2,
                         iters=args.valid_iters,
                         test_mode=True)
      flow_up = padder.unpad(flow_up).squeeze()

      end_time = time.time()
      logging.info(f'Elapsed time: {end_time - start_time} seconds')
      time_list.append(end_time - start_time)

      disp = bv.DisparityMap(data=-flow_up.cpu().numpy().squeeze())

      plt.imsave(f'{output_dir}/{data_set}_gt_color.png',
                 disp_gt_left.raw(),
                 cmap='jet',
                 vmin=vmin,
                 vmax=vmax)
      plt.imsave(f'{output_dir}/{data_set}_disp_color.png',
                 disp.raw(),
                 cmap='jet',
                 vmin=vmin,
                 vmax=vmax)

      disp_gt = disp_gt_left.raw()
      disp = disp.raw()

      abs_rel, sq_rel, rmse = cal_error(disp_gt, disp)
      logging.info(f'abs_rel: {abs_rel}')
      logging.info(f'sq_rel: {sq_rel}')
      logging.info(f'rmse: {rmse}')

      abs_rel_list.append(abs_rel)
      sq_rel_list.append(sq_rel)
      rmse_list.append(rmse)

  logging.info(f'Final abs_rel: {np.mean(abs_rel_list)}')
  logging.info(f'Final sq_rel: {np.mean(sq_rel_list)}')
  logging.info(f'Final rmse: {np.mean(rmse_list)}')
  logging.info(f'Final time: {np.mean(time_list)}')
