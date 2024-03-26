import cv2
from .calibration import StereoCalibParams
from .utils import timecost


class BinoImageRectifier:
  def __init__(self, w: int, h: int, params: StereoCalibParams) -> None:
    """ init method for BinoImageRectifier class

    Args:
        w (int): image width.
        h (int): image height.
        params (StereoCalibParams): stereo calibration parameters.
    """
    if w < 0 or h < 0:
      raise ValueError('image width and height should be positive')
    self.w = w
    self.h = h

    if params is None:
      raise ValueError('invalid stereo calibration parameters!')
    if params.intrins1 is None or params.intrins2 is None:
      raise ValueError('invalid intrinsics!')
    if params.R1 is None or params.R2 is None:
      raise ValueError('invalid rectification matrices!')
    if params.P1 is None or params.P2 is None:
      raise ValueError('invalid projection matrices!')
    self.params = params

  @timecost
  def compute_rect_maps(self):
    """ get rectification maps
    
    Returns:
        list: rectification maps for left and right camera.
    """
    shape = (self.w, self.h)
    rect_maps = [[], []]
    rect_maps[0] = cv2.initUndistortRectifyMap(self.params.intrins1,
                                               self.params.dist_coeffs1,
                                               self.params.R1, self.params.P1,
                                               shape, cv2.CV_16SC2)
    rect_maps[1] = cv2.initUndistortRectifyMap(self.params.intrins2,
                                               self.params.dist_coeffs2,
                                               self.params.R2, self.params.P2,
                                               shape, cv2.CV_16SC2)

    return rect_maps
