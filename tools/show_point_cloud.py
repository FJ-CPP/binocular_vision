#!/usr/bin/env python3

import plotly.graph_objects as go
import numpy as np
from imageio.v3 import imread

import sys
from pathlib import Path

proj_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(str(proj_root))
import bv

if len(sys.argv) != 5:
  print(
    "Usage: python show_point_cloud.py disp_path image_path cam_params_path baseline"
  )
  sys.exit(1)

disp_path = sys.argv[1]
image_path = sys.argv[2]
cam_params_path = sys.argv[3]
baseline = float(sys.argv[4])

# disp = np.fromfile(disp_path, dtype=np.float32)
disp = bv.DisparityMap()
disp.load_from_pfm(disp_path)

image = imread(image_path)

cam_prams = bv.StereoCalibParams()
cam_prams.load_from_json(cam_params_path)

fx = cam_prams.intrins1[0, 0]
cx1 = cam_prams.intrins1[0, 2]
cx2 = cam_prams.intrins2[0, 2]
fy = cam_prams.intrins1[1, 1]
cy = cam_prams.intrins1[1, 2]
print(fx, fy, cx1, cx2, cy)

disp = disp.raw()
disp[disp == -16.0] = 0
disp[disp <= 0] = 0

depth = (fx * baseline) / (disp + (cx2 - cx1))
depth[depth <= 0] = 0
depth[depth >= 300] = 0
depth[depth <= 240] = 0

# 对depth做水平翻转
depth = np.fliplr(depth)

H, W = depth.shape
xx, yy = np.meshgrid(np.arange(W), np.arange(H))
points_grid = np.stack(
  ((xx - cx1) / fx, (yy - cy) / fy, np.ones_like(xx)), axis=0) * depth

tmp_mask = points_grid > 1000
print(tmp_mask.sum())

mask = np.ones((H, W), dtype=bool)

# Remove flying points
mask[1:][np.abs(depth[1:] - depth[:-1]) > 1] = False
mask[:, 1:][np.abs(depth[:, 1:] - depth[:, :-1]) > 1] = False

points = points_grid.transpose(1, 2, 0)[mask]
colors = image[mask].astype(np.float64) / 255

NUM_POINTS_TO_DRAW = 100000

subset = np.random.choice(points.shape[0],
                          size=(NUM_POINTS_TO_DRAW, ),
                          replace=False)
points_subset = points[subset]
colors_subset = colors[subset]

print("""
Controls:
---------
Zoom:      Scroll Wheel
Translate: Right-Click + Drag
Rotate:    Left-Click + Drag
""")

x, y, z = points_subset.T

fig = go.Figure(
  data=[
    go.Scatter3d(
      x=x,
      y=-z,
      z=-y,  # flipped to make visualization nicer
      mode='markers',
      marker=dict(size=1, color=colors_subset))
  ],
  layout=dict(scene=dict(
    xaxis=dict(visible=True),
    yaxis=dict(visible=True),
    zaxis=dict(visible=True),
  )))
fig.show()
