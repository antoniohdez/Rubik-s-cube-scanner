import numpy as np
import cv2
import sys

# OpenCV camera properties
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

cube_size = int(sys.argv[1])

# Setting camera properties
cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH);
cap.set(CV_CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT);

grid_size = VIDEO_HEIGHT / 3
cell_size = grid_size / cube_size
margin = 3

# Grid starting position
grid_pos_x = (VIDEO_WIDTH / 2) - (grid_size / 2)
grid_pos_y = (VIDEO_HEIGHT / 2) - (grid_size / 2)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Iterate cells
    for i in xrange(cube_size):
        for j in xrange(cube_size):
            # Drawing cells
            pos_x = grid_pos_x + cell_size * i
            pos_y = grid_pos_y + cell_size * j
            pos_x_end = pos_x + cell_size
            pos_y_end = pos_y + cell_size

            cv2.rectangle(frame, (pos_x, pos_y), (pos_x_end, pos_y_end), (255, 255, 255), 3)
            
            # Getting mean color 
            cell = frame[pos_y + margin:pos_y_end - margin, pos_x + margin:pos_x_end - margin]
            mean = cv2.mean(cell)


            cv2.rectangle(  frame, 
                            (cell_size * i + margin, cell_size * j + margin), 
                            (cell_size * i + cell_size - margin, cell_size * j + cell_size - margin), 
                            tuple(color * 2.5 for color in mean), 
                            cv2.cv.CV_FILLED
                        )

            # Get cell pixels
            for c_i in xrange(pos_x + margin, pos_x + cell_size - margin):
                for c_j in xrange(pos_y + margin, pos_y + cell_size - margin):
                    # Re-drawing grid in upper 'left' corner (right since there's a flip in the frame)
                    #frame[c_i - pos_x + (cell_size * i), c_j - pos_y + (cell_size * j)] = frame[c_i - grid_size / 2, c_j + grid_size / 2]
                    pass

    # Reflect and display the resulting frame
    frame = cv2.flip(frame,1)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
