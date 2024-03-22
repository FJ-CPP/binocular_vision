import re
import sys
import numpy as np
"""for processing pfm(portable float map)
"""


def load_pfm(path):
  """ load pfm file

  Args:
      path (str): path to the pfm file

  Returns:
      np.array: float map
      float: scale
  """
  with open(path, 'rb') as file:
    header = file.readline().decode('utf-8').rstrip()
    dims = file.readline().decode('utf-8')
    width, height = map(int, re.findall(r'\d+', dims))
    scale = float(file.readline().decode('utf-8').rstrip())
    if scale < 0:  # little-endian
      endian = '<'
      scale = -scale
    else:  # big-endian
      endian = '>'

    data = np.fromfile(file, endian + 'f')
    shape = (height, width, 3) if header == 'PF' else (height, width)
    return np.reshape(data, shape), scale


def save_pfm(path, fm: np.array, scale=1):
  """save pfm file

  Args:
      path (str): path to the pfm file
      fm (np.array): float map
      scale (int, optional): scale. Defaults to 1.
  """
  with open(path, 'wb') as file:
    color = None
    if fm.ndim == 2:  # grayscale
      color = 'Pf'
    elif fm.ndim == 3:  # color
      color = 'PF'

    file.write(f"{color}\n".encode('utf-8'))
    file.write(f"{fm.shape[1]} {fm.shape[0]}\n".encode('utf-8'))
    endian = fm.dtype.byteorder

    if endian == '<' or endian == '=' and sys.byteorder == 'little':
      scale = -scale

    file.write(f"{scale}\n".encode('utf-8'))
    fm.tofile(file)


if __name__ == '__main__':
  pfm_path = '../../data/artroom1/disp0.pfm'

  # read value
  read_value, scale = load_pfm(pfm_path)
  print('Loaded PFM:', read_value.shape)
  print(f'Scale: {scale}')

  # real value
  real_value = read_value * abs(scale)
  real_value[np.isinf(real_value)] = 0
  import cv2
  real_value = cv2.normalize(real_value,
                             None,
                             alpha=0,
                             beta=255,
                             norm_type=cv2.NORM_MINMAX,
                             dtype=cv2.CV_8U)

  cv2.imwrite('disparity_visualized.png', np.flipud(real_value))

  print('Real value:\n', real_value)
  save_pfm('resaved.pfm', read_value, scale)
  print('Saved PFM.')

  # check md5
  import os
  import hashlib
  assert hashlib.md5(open(pfm_path, 'rb').read()).hexdigest() == hashlib.md5(
    open('resaved.pfm', 'rb').read()).hexdigest()
  os.remove('resaved.pfm')
