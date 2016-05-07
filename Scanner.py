from collections import Counter
from cube_interactive import Cube
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import widgets
from projection import Quaternion, project_points

import json
import math
import cv2

from rubik import Rubik
from cpp_solver import solve

class Scanner:
    faces = {}
    current_face = []
    COLOR_SAMPLES = []
    COLORS = []
    POSSIBLE_FACES = ['B', 'L', 'F', 'R', 'D', 'U']

    def __init__(self, dimensions = 3, frame_size = (640, 480), proportion = 3, color_samples = 'resources/color_samples.json', colors = 'resources/colors.json'):
        self.dimensions = dimensions
        self.grid_size = frame_size[1] / 3
        self.cell_size = self.grid_size / self.dimensions
        self.margin = 7
        # Grid starting position
        self.grid_pos_x = (frame_size[0] / 2) - (self.grid_size / 2)
        self.grid_pos_y = (frame_size[1] / 2) - (self.grid_size / 2)
        with open(color_samples) as json_file:
            self.COLOR_SAMPLES = json.load(json_file)
        with open(colors) as json_file:
            self.COLORS = json.load(json_file)

    def draw_grid(self, frame):        
        #self.detect_shapes(frame)
        # Iterate cells
        self.current_face = []
        for i in xrange(self.dimensions):
            self.current_face.append([])
            for j in xrange(self.dimensions):
                # Drawing cells
                pos_x = self.grid_pos_x + self.cell_size * i
                pos_y = self.grid_pos_y + self.cell_size * j
                pos_x_end = pos_x + self.cell_size
                pos_y_end = pos_y + self.cell_size

                cv2.rectangle(frame, (pos_x, pos_y), (pos_x_end, pos_y_end), (255, 255, 255), self.margin)
                
                mean_color = self.draw_mean_color(frame, (pos_x, pos_y), (pos_x_end, pos_y_end), (i, j))              
                self.current_face[i].append(mean_color)

        self.draw_faces(frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            self.capture_face()
        if cv2.waitKey(1) & 0xFF == ord('d'):
            self.delete_face()

    def capture_face(self):
        if len(self.faces) < 6:
            face = []
            for row in self.current_face:
                face.append([])
                for cell in row:
                    face[-1].append(cell)

            next_face = self.POSSIBLE_FACES[len(self.faces)]
            
            if next_face == "B":
                # DONE!!!!!
                #face = face[::-1] # Hacer espejo vertical, no horizontal
                for i in xrange(len(face)):
                    face[i] = face[i][::-1]
            elif next_face == "R":
                face = face[::-1]
                face = zip(*face[::-1])
                # Girar 90 grados
                # face = face[::-1]
                # girar 90 grados, hacer espejo horizontal
            elif next_face == "L":
                # DONE!!!!
                for i in xrange(len(face)):
                    face[i] = face[i][::-1]
                face = zip(*face[::-1])
                
            elif next_face == "F":
                # DONE!!!!!
                face = face[::-1]
            elif next_face == "U":
                face = face[::-1]
                face = zip(*face[::-1])
                pass # Girar 270 grados
            elif next_face == "D":
                face = face[::-1]
                face = zip(*face[::-1])
                pass # Espejo y 90 grados
            
            self.faces[next_face] = face
            print face

        if len(self.faces) == 6:
            colors = []
            colors.append(self.map_face( self.faces["B"] ))
            colors.append(self.map_face( self.faces["F"] ))
            colors.append(self.map_face( self.faces["R"] ))
            colors.append(self.map_face( self.faces["L"] ))
            colors.append(self.map_face( self.faces["D"] ))
            colors.append(self.map_face( self.faces["U"] ))

            
            # colors = [[0,1,2,3,4,5,3,2,4], [0,1,2,3,4,5,3,2,4], [0,1,2,3,4,5,3,2,4], [0,1,2,3,4,5,3,2,4], [0,1,2,3,4,5,3,2,4], [0,1,2,3,4,5,3,2,4]]
            

            colors_rgb = {}
            colors_rgb["B"] = self.map_face_RGB( self.flip_matrix( self.rotate_matrix(self.faces["B"], 3)))
            colors_rgb["F"] = self.map_face_RGB( self.flip_matrix( self.rotate_matrix(self.faces["F"], 3)))
            colors_rgb["R"] = self.map_face_RGB( self.flip_matrix( self.rotate_matrix(self.faces["R"], 3)))
            colors_rgb["L"] = self.map_face_RGB( self.flip_matrix( self.rotate_matrix(self.faces["L"], 3)))
            colors_rgb["U"] = self.map_face_RGB( self.flip_matrix( self.rotate_matrix(self.faces["D"], 1)))
            colors_rgb["D"] = self.map_face_RGB( self.flip_matrix( self.rotate_matrix(self.faces["U"], 3)))

            rubik = Rubik(colors_rgb)
            rubik.describe()



            c = Cube(self.dimensions, None, None, colors)
            c.draw_interactive()
            plt.show()
            
            solve(Rubik(colors_rgb))
            # Cube visualization

    def rotate_matrix(self, matrix, n):
        for i in xrange(n):
            matrix = [[matrix[3 - j - 1][i] for j in range(3)] for i in range (3)]
        return matrix

    def flip_matrix(self, matrix):
        for i in xrange(len(matrix)):
            tmp = None
            tmp = matrix[i][0]
            matrix[i][0] = matrix[i][2]
            matrix[i][2] = tmp
        return matrix

    def map_face_RGB(self, value):
        face = [["" for _ in xrange(3)] for _ in xrange(3)]
        for i in xrange(len(value)):
            for j in xrange(len(value[i])):
                if value[i][j] == [255.0, 255.0, 255.0]: # White
                    face[i][j] = "W"
                elif value[i][j] == [255.0, 255.0, 0]: # Yellow
                    face[i][j] = "Y"
                elif value[i][j] == [0.0, 0.0, 255.0]: # Blue
                    face[i][j] = "B"
                elif value[i][j] == [0.0, 255.0, 0.0]: # Green
                    face[i][j] = "G"
                elif value[i][j] == [255.0, 128.0, 0.0]: #Orange
                    face[i][j] = "O"
                elif value[i][j] == [255.0, 0.0, 0.0]: # Red
                    face[i][j] = "R"
        return face
        
    def map_face(self, value):
        face = []
        for row in value:
            for color in row:
                if color == [255.0, 255.0, 255.0]: # White
                    face.append(0)
                elif color == [255.0, 255.0, 0]: # Orange
                    face.append(1)
                elif color == [0.0, 0.0, 255.0]: # Blue
                    face.append(2)
                elif color == [0.0, 255.0, 0.0]: # Green
                    face.append(3)
                elif color == [255.0, 128.0, 0.0]: #Orange
                    face.append(4)
                elif color == [255.0, 0.0, 0.0]: # Red
                    face.append(5)
                print color
        return face

    def delete_face(self):
        if len(self.faces) >= 0:
            del self.faces[self.POSSIBLE_FACES[len(self.faces) - 1]]

    def draw_mean_color(self, frame, start, end, cell_indexes, debug = False):
        # Getting mean color 
        i = cell_indexes[0]
        j = cell_indexes[1]

        cell = frame[start[1] + self.margin:end[1] - self.margin, start[0] + self.margin:end[0] - self.margin]
        mean = self.get_mean_color(cell)
        closest_color = self.get_closest_color({"r": mean[0], "g": mean[1], "b": mean[2]})

        cv2.rectangle(  frame, 
                        (self.cell_size * i + self.margin, self.cell_size * j + self.margin), 
                        (self.cell_size * i + self.cell_size - self.margin, self.cell_size * j + self.cell_size - self.margin), 
                        closest_color,
                        cv2.cv.CV_FILLED
                    )
        if debug:
            # Mean color
            cv2.rectangle(  frame, 
                            (self.cell_size * i + self.margin + self.grid_size * 3, self.cell_size * j + self.margin), 
                            (self.cell_size * i + self.cell_size - self.margin + self.grid_size * 3, self.cell_size * j + self.cell_size - self.margin), 
                            tuple(color for color in mean), 
                            cv2.cv.CV_FILLED
                        )

        return closest_color
    
    def get_mean_color(self, cell):
        pixels = []
        for pixels_row in cell:
            for pixel in pixels_row:
                pixels.append(tuple([float(pixel[0]), float(pixel[1]), float(pixel[2]), 0.0]))
        
        counter = Counter(pixels)
        max_count = max(counter.values())
        mode = [[k, v] for k,v in counter.items() if v == max_count]

        #print mode[0][0]
        return mode[0][0]
        #return cv2.mean(cell)

    def distance(self, a, b):
        return math.sqrt(math.pow(a["r"] - b["r"], 2) + math.pow(a["g"] - b["g"], 2) + math.pow(a["b"] - b["b"], 2))

    def get_closest_color(self, mean_color):
        closest = {}
        min_distance = float("inf")

        for i in xrange(len(self.COLOR_SAMPLES)):
            dist = self.distance(mean_color, self.COLOR_SAMPLES[i])
            if dist < min_distance:
                closest = self.COLOR_SAMPLES[i]
                min_distance = dist
        
        return self.COLORS[closest['name']]

    def draw_faces(self, frame):
        #self.POSSIBLE_FACES = ['B', 'R', 'F', 'L', 'D', 'U']

        # Iterate faces
        for key, value in self.faces.iteritems():
            # Iterate rows
            for i in xrange(len(self.faces[key])):
                #Iterate columns
                for j in xrange(len(self.faces[key][i])):
                    cv2.rectangle(  frame, 
                                    (30 * i + self.margin + self.POSSIBLE_FACES.index(key) * 105, 30 * j + self.margin + 390), 
                                    (30 * i + 30 - self.margin + self.POSSIBLE_FACES.index(key) * 105, 30 * j + 30 - self.margin + 390), 
                                    self.faces[key][i][j], 
                                    cv2.cv.CV_FILLED
                                )