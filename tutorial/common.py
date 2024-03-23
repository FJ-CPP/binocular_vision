import os
import cv2


def ensure_path(path):
  """ ensure path exists
  
  Args:
      path (str): path to ensure
  """
  if not os.path.exists(path):
    os.makedirs(path)


def MiddleBury_data_loader(data_path):
  """ load MiddleBury stereo image pair and calibration data

  Args:
      data_path (str): MiddleBury stereo data path
  """
  limage = cv2.imread(f'{data_path}/im0.png', cv2.IMREAD_COLOR)
  rimages = cv2.imread(f'{data_path}/im1.png', cv2.IMREAD_COLOR)
  calib_file = f'{data_path}/calib.txt'

  with open(calib_file, 'r') as f:
    lines = f.readlines()
    intrin1 = lines[0].split('=')[1]
    intrin2 = lines[1].split('=')[1]
    doffs = float(lines[2].split('=')[1])
    baseline = float(lines[3].split('=')[1])
    ndisp = int(lines[6].split('=')[1])
    vmin = int(lines[7].split('=')[1])
    vmax = int(lines[8].split('=')[1])

  return limage, rimages, intrin1, intrin2, doffs, baseline, ndisp, vmin, vmax