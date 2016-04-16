from collections import Counter
import numpy as np
import math
import cv2

class Scanner:

    COLORS = [
            {"name": "red",   "r": 255, "g": 0,   "b": 0  },
            {"name": "green", "r": 0,   "g": 255, "b": 0  },
            {"name": "blue",  "r": 0,   "g": 0,   "b": 255},
            {"name": "yellow","r": 255, "g": 255, "b": 0  },
            {"name": "white", "r": 255, "g": 255, "b": 255},
            {"name": "orange","r": 255, "g": 128, "b": 0  }
        ]

    def __init__(self, dimensions = 3, frame_size = (640, 480), proportion = 3):
        self.dimensions = dimensions
        self.grid_size = frame_size[1] / 3
        self.cell_size = self.grid_size / self.dimensions
        self.margin = 5
        # Grid starting position
        self.grid_pos_x = (frame_size[0] / 2) - (self.grid_size / 2)
        self.grid_pos_y = (frame_size[1] / 2) - (self.grid_size / 2)

    def draw_grid(self, frame):
        # Iterate cells
        for i in xrange(self.dimensions):
            for j in xrange(self.dimensions):
                # Drawing cells
                pos_x = self.grid_pos_x + self.cell_size * i
                pos_y = self.grid_pos_y + self.cell_size * j
                pos_x_end = pos_x + self.cell_size
                pos_y_end = pos_y + self.cell_size

                cv2.rectangle(frame, (pos_x, pos_y), (pos_x_end, pos_y_end), (255, 255, 255), self.margin)
                
                self.draw_mean_color(frame, (pos_x, pos_y), (pos_x_end, pos_y_end), (i, j))              

    def draw_mean_color(self, frame, start, end, cell_indexes):
        # Getting mean color 
        i = cell_indexes[0]
        j = cell_indexes[1]

        cell = frame[start[1] + self.margin:end[1] - self.margin, start[0] + self.margin:end[0] - self.margin]
        mean = self.get_mean_color(cell)

        cv2.rectangle(  frame, 
                        (self.cell_size * i + self.margin, self.cell_size * j + self.margin), 
                        (self.cell_size * i + self.cell_size - self.margin, self.cell_size * j + self.cell_size - self.margin), 
                        self.get_closest_color({"r": mean[0], "g": mean[1], "b": mean[2]}), # tuple(color * 2.5 for color in mean), 
                        cv2.cv.CV_FILLED
                    )

        # Mean color
        cv2.rectangle(  frame, 
                        (self.cell_size * i + self.margin + self.grid_size * 3, self.cell_size * j + self.margin), 
                        (self.cell_size * i + self.cell_size - self.margin + self.grid_size * 3, self.cell_size * j + self.cell_size - self.margin), 
                        tuple(color for color in mean), 
                        cv2.cv.CV_FILLED
                    )
    
    def get_mean_color(self, cell):
        pixels = []
        for pixels_row in cell:
            for pixel in pixels_row:
                pixels.append(tuple([pixel[0], pixel[1], pixel[2]]))
        
        counter = Counter(pixels)
        max_count = max(counter.values())
        mode = [[k, v] for k,v in counter.items() if v == max_count]
        
        #print mode
        #return mode[0][0]
        return cv2.mean(cell)

    def distance(self, a, b):
        return math.sqrt(math.pow(a["r"] - b["r"], 2) + math.pow(a["g"] - b["g"], 2) + math.pow(a["b"] - b["b"], 2))

    def get_closest_color(self, mean_color):
        closest = {}
        min_distance = float("inf")

        for i in xrange(len(self.COLORS)):
            dist = self.distance(mean_color, self.COLORS[i])
            if dist < min_distance:
                closest = self.COLORS[i]
                min_distance = dist

        return ([closest["r"], closest["g"], closest["b"]])










