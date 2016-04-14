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

        self.scanner = Scanner(rubik_dimensions, camera_size, 3)
        
    def scan(self, fps = 30):
        while(True):
            ret, frame = self.camera.read()

            self.scanner.draw_grid(frame)

            # Reflect and display the resulting frame
            frame = cv2.flip(frame,1)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def release(self):
        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()


camera = Camera(int(sys.argv[1]))
camera.scan()
