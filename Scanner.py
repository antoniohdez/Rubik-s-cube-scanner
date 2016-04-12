import numpy as np
import cv2

# OpenCV camera properties
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

# Setting camera properties
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH);
cap.set(CV_CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT);

grid_size = VIDEO_HEIGHT / 2
cell_size = grid_size / 3

grid_pos_x = (VIDEO_WIDTH / 2) - (grid_size / 2)
grid_pos_y = (VIDEO_HEIGHT / 2) - (grid_size / 2)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    for i in xrange(3):
        for j in xrange(3):
            pos_x = grid_pos_x + cell_size * i
            pos_y = grid_pos_y + cell_size * j
            cv2.rectangle(frame, (pos_x, pos_y), (pos_x + cell_size, pos_y + cell_size), (255, 255, 255), 3)        

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
