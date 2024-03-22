import cv2
import numpy as np
from .disparity_map import DisparityMap
from .utils import timecost


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
    """compute disparity map from stereo images

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
