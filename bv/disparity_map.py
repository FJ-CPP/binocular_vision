import numpy as np
import cv2
from .utils import timecost, load_pfm, save_pfm


class DisparityMap:
  def __init__(self, data: np.array = None) -> None:
    """ init method for DisparityMap class

    Args:
        data (np.array): disparity map data in float32
    """
    self._data = data

  def raw(self) -> np.array:
    """return raw disparity map data

    Returns:
        np.array: disparity map data
    """
    return self._data

  @timecost
  def norm2int8(self) -> np.array:
    """normalize disparity map

    Returns:
        np.array: normalized disparity map data
    """
    return cv2.normalize(self._data,
                         None,
                         alpha=0,
                         beta=255,
                         norm_type=cv2.NORM_MINMAX,
                         dtype=cv2.CV_8U)

  @timecost
  def load_from_pfm(self, pfm_file: str) -> None:
    """load disparity map from pfm file

    Inf values in this pfm file will be set to 0.

    Args:
        pfm_file (str): pfm file path
    """
    disp, scale = load_pfm(pfm_file)
    real_disp = disp * abs(scale)
    real_disp[np.isinf(real_disp)] = 0
    self._data = real_disp

  @timecost
  def save_as_pfm(self, pfm_file: str, scale=1) -> None:
    """save disparity map as pfm file

    Args:
        pfm_file (str): pfm file path
        scale (float, optional): scale. Defaults to 1/16.0.
    """
    save_pfm(pfm_file, self._data, scale)
