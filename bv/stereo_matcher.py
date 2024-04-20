import cv2
import numpy as np
from scipy.ndimage import median_filter
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
    """ normalize disparity map

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
  def load_from_pfm(self, pfm_file: str, need_flipud=False) -> None:
    """ load disparity map from pfm file

    Inf values in this pfm file will be set to 0.

    Args:
        pfm_file (str): pfm file path
    """
    disp, scale = load_pfm(pfm_file)
    real_disp = disp
    real_disp[np.isinf(real_disp)] = 0
    self._data = real_disp
    if need_flipud:
      self._data = np.flipud(self._data)

  @timecost
  def save_as_pfm(self, pfm_file: str, scale=1) -> None:
    """save disparity map as pfm file

    Args:
        pfm_file (str): pfm file path
        scale (float, optional): scale. Defaults to 1/16.0.
    """
    save_pfm(pfm_file, self._data, scale)


class StereoMatcher:
  def __init__(self,
               min_disparity=0,
               num_disparities=16,
               block_size=3,
               p1=0,
               p2=0,
               disp12_max_diff=0,
               pre_filter_cap=0,
               uniqueness_ratio=0,
               speckle_window_size=0,
               speckle_range=0,
               mode=cv2.STEREO_SGBM_MODE_SGBM):
    """ init method for StereoMatcher class

    Args:
        min_disparity (int, optional): minimum disparity. Defaults to 0.
        num_disparities (int, optional): number of disparities. Defaults to 16.
        block_size (int, optional): block size. Defaults to 3.
        p1 (int, optional): p1. Defaults to 0.
        p2 (int, optional): p2. Defaults to 0.
        disp12_max_diff (int, optional): disp12_max_diff. Defaults to 0.
        pre_filter_cap (int, optional): pre_filter_cap. Defaults to 0.
        uniqueness_ratio (int, optional): uniqueness_ratio. Defaults to 0.
        speckle_window_size (int, optional): speckle_window_size. Defaults to 0.
        speckle_range (int, optional): speckle_range. Defaults to 0.
        mode (int, optional): mode. Defaults to cv2.STEREO_SGBM_MODE_SGBM.
    """
    self._min_disparity = min_disparity
    self._num_disparities = num_disparities
    self._block_size = block_size
    self._p1 = p1
    self._p2 = p2
    self._disp12_max_diff = disp12_max_diff
    self._pre_filter_cap = pre_filter_cap
    self._uniqueness_ratio = uniqueness_ratio
    self._speckle_window_size = speckle_window_size
    self._speckle_range = speckle_range
    self._mode = mode

    if self._mode == cv2.STEREO_SGBM_MODE_SGBM or      \
       self._mode == cv2.STEREO_SGBM_MODE_HH or        \
       self._mode == cv2.STEREO_SGBM_MODE_SGBM_3WAY or \
       self._mode == cv2.STEREO_SGBM_MODE_HH4:
      self.stereo_matcher = cv2.StereoSGBM_create(
        minDisparity=self._min_disparity,
        numDisparities=self._num_disparities,
        blockSize=self._block_size,
        P1=self._p1,
        P2=self._p2,
        disp12MaxDiff=self._disp12_max_diff,
        preFilterCap=self._pre_filter_cap,
        uniquenessRatio=self._uniqueness_ratio,
        speckleWindowSize=self._speckle_window_size,
        speckleRange=self._speckle_range,
        mode=self._mode)
    else:
      raise NotImplementedError(f'stereo matcher mode not implemented!')

  @property
  def min_disparity(self):
    return self._min_disparity

  @min_disparity.setter
  def min_disparity(self, v):
    self._min_disparity = v
    self.stereo_matcher.setMinDisparity(self._min_disparity)

  @property
  def num_disparity(self):
    return self._num_disparities

  @num_disparity.setter
  def num_disparity(self, v):
    if v % 16 != 0:
      raise ValueError('num_disparities must be a multiple of 16!')
    self._num_disparities = v
    self.stereo_matcher.setNumDisparities(self._num_disparities)

  @property
  def block_size(self):
    return self._block_size

  @block_size.setter
  def block_size(self, v):
    self._block_size = v
    self.stereo_matcher.setBlockSize(self._block_size)

  @property
  def p1(self):
    return self._p1

  @p1.setter
  def p1(self, v):
    self._p1 = v
    self.stereo_matcher.setP1(self._p1)

  @property
  def p2(self):
    return self._p2

  @p2.setter
  def p2(self, v):
    self._p2 = v
    self.stereo_matcher.setP2(self._p2)

  @property
  def disp12_max_diff(self):
    return self._disp12_max_diff

  @disp12_max_diff.setter
  def disp12_max_diff(self, v):
    self._disp12_max_diff = v
    self.stereo_matcher.setDisp12MaxDiff(self._disp12_max_diff)

  @property
  def pre_filter_cap(self):
    return self._pre_filter_cap

  @pre_filter_cap.setter
  def pre_filter_cap(self, v):
    self._pre_filter_cap = v
    self.stereo_matcher.setPreFilterCap(self._pre_filter_cap)

  @property
  def uniqueness_ratio(self):
    return self._uniqueness_ratio

  @uniqueness_ratio.setter
  def uniqueness_ratio(self, v):
    self._uniqueness_ratio = v
    self.stereo_matcher.setUniquenessRatio(self._uniqueness_ratio)

  @property
  def speckle_window_size(self):
    return self._speckle_window_size

  @speckle_window_size.setter
  def speckle_window_size(self, v):
    self._speckle_window_size = v
    self.stereo_matcher.setSpeckleWindowSize(self._speckle_window_size)

  @property
  def speckle_range(self):
    return self._speckle_range

  @speckle_range.setter
  def speckle_range(self, v):
    self._speckle_range = v
    self.stereo_matcher.setSpeckleRange(self._speckle_range)

  @property
  def mode(self):
    return self._mode

  @mode.setter
  def mode(self, v):
    self._mode = v
    self.stereo_matcher.setMode(self._mode)

  @timecost
  def compute_disparity_map(self, img_left, img_right) -> DisparityMap:
    """ compute disparity map from stereo images

    Args:
        img_left (Any): left image
        img_right (Any): right image

    Returns:
        DisparityMap : disparity map
    """

    # divide by 16 to get the raw disparity map
    disparity = self.stereo_matcher.compute(img_left, img_right).astype(
      np.float32) / 16.0
    return DisparityMap(data=disparity)

  @timecost
  def filter_with_wls(self,
                      left_disparity_map: DisparityMap,
                      img_left,
                      img_right,
                      wls_lambda=8000,
                      wls_sigma=1.5) -> DisparityMap:
    """ filter disparity map with wls

    Args:
        left_disparity_map (DisparityMap): left disparity map
        img_left (Any): left image
        img_right (Any): right image
        wls_lambda (int, optional): lambda param for wls. Defaults to 8000.
        wls_sigma (float, optional): sigma param for wls. Defaults to 1.5.

    Returns:
        DisparityMap: filtered disparity map
    """
    right_matcher = cv2.ximgproc.createRightMatcher(self.stereo_matcher)

    # divide by 16 to get the raw disparity map
    right_disparity_map = (
      right_matcher.compute(img_right, img_left).astype(np.float32) / 16.0)

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(
      matcher_left=self.stereo_matcher)
    wls_filter.setLambda(wls_lambda)
    wls_filter.setSigmaColor(wls_sigma)

    filtered_left_disparity_map = wls_filter.filter(left_disparity_map.raw(),
                                                    img_left, None,
                                                    right_disparity_map)
    return DisparityMap(data=filtered_left_disparity_map)

  @timecost
  def filter_with_median(self,
                         disparity_map: DisparityMap,
                         ksize=3) -> DisparityMap:
    """ filter disparity map with median filter

    Args:
        disparity_map (DisparityMap): disparity map
        ksize (int, optional): kernel size. Defaults to 3.

    Returns:
        DisparityMap: filtered disparity map
    """
    return DisparityMap(data=median_filter(disparity_map.raw(), ksize))
