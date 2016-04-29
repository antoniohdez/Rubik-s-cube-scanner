import camera_properties as CV_CAP_PROP
import numpy as np
from scanner import Scanner
import cv2
import sys

class Camera:

    camera = None
    grid = None

    def __init__(self, rubik_dimensions = 3, camera_size = (640, 480)):
        """Initialize scanner

        Keyword arguments:
        rubik_dimensions  -- Rubik's cube size (default 3)
        camera_size       -- width and height of the camera (default (640, 480) )
        """
        self.cube_size = rubik_dimensions
        self.VIDEO_WIDTH = camera_size[0]
        self.VIDEO_HEIGHT = camera_size[1]

        # Setting camera properties
        self.camera = cv2.VideoCapture(0)
        self.camera.set(CV_CAP_PROP.CV_CAP_PROP_FRAME_WIDTH, self.VIDEO_WIDTH);
        self.camera.set(CV_CAP_PROP.CV_CAP_PROP_FRAME_HEIGHT, self.VIDEO_HEIGHT);

        self.camera.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 100)
        self.camera.set(cv2.cv.CV_CAP_PROP_CONTRAST, 100)

        self.scanner = Scanner(rubik_dimensions, camera_size, 3)
        
    def scan(self, fps = 30):
        while(True):
            ret, bgr_frame = self.camera.read()

            # Change from BGR to RGB
            b, g, r = cv2.split(bgr_frame)
            frame = cv2.merge([r, g, b])

            self.scanner.draw_grid(frame)

            # Back to BGR
            r, g, b = cv2.split(frame)
            bgr_frame = cv2.merge([b, g, r])

            # Reflect and display the resulting frame
            bgr_frame = cv2.flip(bgr_frame,1)
            cv2.imshow('Rubik\'s cube scanner', bgr_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def release(self):
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()


camera = Camera(int(sys.argv[1]))
camera.scan()
