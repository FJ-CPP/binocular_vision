import cv2
import numpy as np
import sys


def mouse_callback(event, x, y, flags, param):
  global img_display
  if event == cv2.EVENT_MOUSEMOVE:
    gray_value = img[y, x]
    img_display = np.copy(img)
    text = f"Grayscale value at ({x}, {y}): {gray_value}"
    cv2.putText(img_display, text, (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.4, (255, 255, 255), 1)


if __name__ == "__main__":
  img = cv2.imread(f'{sys.argv[1]}', cv2.IMREAD_GRAYSCALE)
  img_display = np.copy(img)

  cv2.namedWindow("Image")

  cv2.setMouseCallback("Image", mouse_callback)

  while True:
    cv2.imshow("Image", img_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

    cv2.destroyAllWindows()
