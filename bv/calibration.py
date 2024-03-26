import json
import numpy as np
import cv2
import logging
from .utils import timecost


class StereoCalibParams:
  def __init__(self,
               intrins1=None,
               dist_coeffs1=None,
               intrins2=None,
               dist_coeffs2=None,
               R=None,
               T=None,
               E=None,
               F=None,
               R1=None,
               R2=None,
               P1=None,
               P2=None,
               Q=None,
               roi1=None,
               roi2=None):
    """ init method for StereoCalibParams class

    Args:
        intrins1 (np.ndarray, optional): intrinsic matrix of left camera.
        dist_coeffs1 (np.ndarray, optional): distortion coefficients of left camera.
        intrins2 (np.ndarray, optional): intrinsic matrix of right camera.
        dist_coeffs2 (np.ndarray, optional): distortion coefficients of right camera.
        R (np.ndarray, optional): rotation matrix between left and right cameras.
        T (np.ndarray, optional): translation vector between left and right cameras.
        E (np.ndarray, optional): essential matrix.
        F (np.ndarray, optional): fundamental matrix.
        R1 (np.ndarray, optional): rectification matrix for left camera.
        R2 (np.ndarray, optional): rectification matrix for right camera.
        P1 (np.ndarray, optional): projection matrix for left camera.
        P2 (np.ndarray, optional): projection matrix for right camera.
        Q (np.ndarray, optional): disparity-to-depth mapping matrix.
        roi1 (tuple, optional): region of interest for left camera.
        roi2 (tuple, optional): region of interest for right camera.
    """
    self.intrins1 = intrins1
    self.dist_coeffs1 = dist_coeffs1
    self.intrins2 = intrins2
    self.dist_coeffs2 = dist_coeffs2
    self.R = R
    self.T = T
    self.E = E
    self.F = F
    self.R1 = R1
    self.R2 = R2
    self.P1 = P1
    self.P2 = P2
    self.Q = Q
    self.roi1 = roi1
    self.roi2 = roi2

  def save_as_json(self, fpath):
    """ save stereo calibration parameters to json file

    Args:
        fpath (str): json file path.
    """
    with open(fpath, 'w') as f:
      serializable_dict = {}
      for k, v in self.__dict__.items():
        if isinstance(v, np.ndarray):
          serializable_dict[k] = v.tolist()
        elif isinstance(v, tuple):
          serializable_dict[k] = v
        else:
          raise ValueError(
            'invalid stereo calibration parameters for serialization!')

      json.dump(serializable_dict, f, indent=4)

  def load_from_json(self, fpath):
    """ load stereo calibration parameters from json file

    Args:
        fpath (str): json file path.
    """
    with open(fpath, 'r') as f:
      serializable_dict = json.load(f)
      for key, value in serializable_dict.items():
        if isinstance(value, list):
          setattr(self, key, np.array(value))
        else:
          setattr(self, key, value)

      for k, v in self.__dict__.items():
        print(k, v)


class StereoCalibrator:
  def __init__(self, border_size=(9, 6), square_size=1.0):
    """ init method for StereoCalibrator class

    Args:
        border_size (tuple, optional): chessboard size. Defaults to (9, 6).
        square_size (float, optional): chessboard square size. Defaults to 1.0.
    """
    self.border_size = border_size
    self.square_size = square_size

  @timecost
  def stereo_calib(
      self,
      left_images,
      right_images,
      check_quality=False
  ) -> tuple[StereoCalibParams, float, float, list, list]:
    """ stereo calibration

    Args:
        left_images (list(str)): path list of left images.
        right_images (list(str)): path list of right images.
        check_quality (bool, optional): need check stereo calibration quality. Defaults to False.

    Returns:
        tuple[StereoCalibParams, float, float, list, list]: stereo calibration parameters, 
        calibration rms, epipolar error, chessboard corners, valid image pairs.
    """
    if len(left_images) != len(right_images):
      raise ValueError('invalid image list!')

    h, w = None, None
    corners = [[], []]
    valid_image_pairs = []
    intrins = [[], []]
    dist_coeffs = [[], []]
    calib_rms = None
    epipolar_err = None
    rect_maps = [[], []]
    R = None
    T = None
    E = None
    F = None
    Q = None
    roi1 = None
    roi2 = None
    """
    Find chessboard corners in images
    """
    logging.info('finding chessboard corners in images ...')
    for i in range(len(left_images)):
      limage = cv2.imread(left_images[i], cv2.IMREAD_GRAYSCALE)
      rimage = cv2.imread(right_images[i], cv2.IMREAD_GRAYSCALE)

      if limage is None:
        raise ValueError(f'failed to load image {left_images[i]}')

      if rimage is None:
        raise ValueError(f'failed to load image {right_images[i]}')

      if h is None:
        h, w = limage.shape[:2]
      elif (h, w) != limage.shape[:2]:
        raise ValueError(
          f'image {left_images[i]} has different size from the first image')
      else:
        pass

      found, lcorners = cv2.findChessboardCorners(
        limage,
        self.border_size,
        flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)

      if not found:
        logging.warning(f'chessboard not found in image {left_images[i]}')
        continue

      found, rcorners = cv2.findChessboardCorners(
        rimage,
        self.border_size,
        flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)

      if not found:
        logging.warning(f'chessboard not found in image {right_images[i]}')
        continue

      term_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30,
                       0.01)
      cv2.cornerSubPix(limage, lcorners, (11, 11), (-1, -1), term_criteria)
      cv2.cornerSubPix(rimage, rcorners, (11, 11), (-1, -1), term_criteria)

      corners[0].append(lcorners)
      corners[1].append(rcorners)
      valid_image_pairs.append(i)
    """
    Stereo calibration
    """
    logging.info('stereo calibration ...')
    term_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100,
                     1e-5)
    obj_points = np.zeros((self.border_size[0] * self.border_size[1], 3),
                          np.float32)
    obj_points[:, :2] = np.mgrid[0:self.border_size[0],
                                 0:self.border_size[1]].T.reshape(-1, 2)
    obj_points *= self.square_size

    intrins[0] = cv2.initCameraMatrix2D([obj_points] * len(corners[0]),
                                        corners[0], (w, h), 0)
    intrins[1] = cv2.initCameraMatrix2D([obj_points] * len(corners[1]),
                                        corners[1], (w, h), 0)

    calib_rms, intrins[0], dist_coeffs[0], intrins[1], dist_coeffs[
      1], R, T, E, F = cv2.stereoCalibrate(
        [obj_points] * len(corners[0]),
        corners[0],
        corners[1],
        intrins[0],
        None,
        intrins[1],
        None, (w, h),
        flags=(cv2.CALIB_FIX_ASPECT_RATIO + cv2.CALIB_ZERO_TANGENT_DIST +
               cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_SAME_FOCAL_LENGTH +
               cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_K3 + cv2.CALIB_FIX_K4 +
               cv2.CALIB_FIX_K5),
        criteria=term_criteria)
    """
    Check calibration quality
    """
    if check_quality:
      logging.info('checking calibration quality ...')
      epipolar_err = 0
      err_cnt = len(corners[0]) * len(corners[0][0])
      epipolar_lines = [[], []]
      for i in range(len(corners[0])):
        """
        undistort corner points
        """
        for k in range(2):
          corners[k][i] = cv2.undistortPoints(corners[k][i],
                                              intrins[k],
                                              dist_coeffs[k],
                                              R=None,
                                              P=intrins[k])
          epipolar_lines[k] = cv2.computeCorrespondEpilines(
            corners[k][i], k + 1, F)

        for j in range(len(corners[0][i])):
          epipolar_err += abs(
            corners[0][i][j][0][0] * epipolar_lines[1][j][0][0] +
            corners[0][i][j][0][1] * epipolar_lines[1][j][0][1] +
            epipolar_lines[1][j][0][2]) + abs(
              corners[1][i][j][0][0] * epipolar_lines[0][j][0][0] +
              corners[1][i][j][0][1] * epipolar_lines[0][j][0][1] +
              epipolar_lines[0][j][0][2])

      epipolar_err /= err_cnt
    """
    Get stereo rectification parameters 
    """
    logging.info('computing stereo rectification parameters ...')
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
      intrins[0],
      dist_coeffs[0],
      intrins[1],
      dist_coeffs[1], (w, h),
      R,
      T,
      flags=cv2.CALIB_ZERO_DISPARITY,
      alpha=-1)

    params = StereoCalibParams(intrins[0], dist_coeffs[0], intrins[1],
                               dist_coeffs[1], R, T, E, F, R1, R2, P1, P2, Q,
                               roi1, roi2)

    return params, calib_rms, epipolar_err, corners, valid_image_pairs
