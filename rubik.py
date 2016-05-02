from random import randint, choice

class Rubik(object):
    """Matrix representation of a Rubik's cube"""
    #Constats for colors

    RED = 0
    GREEN = 1
    BLUE = 2
    ORANGE = 3
    YELLOW = 4
    WHITE = 5
    faces = {}

    def __init__(self, faces= {
            'U':[['Y' for i in range(3)] for j in range(3)], #Yellow
            'F':[['R' for i in range(3)] for j in range(3)], #Red
            'D':[['W' for i in range(3)] for j in range(3)], #White
            'B':[['O' for i in range(3)] for j in range(3)], #Orange
            'L':[['B' for i in range(3)] for j in range(3)], #Blue
            'R':[['G' for i in range(3)] for j in range(3)]  #Green
        }):
        #self.faces = faces
        self.faces = {
                'U':[[faces['U'][i][j] for j in range(3)] for i in range(3)],
                'F':[[faces['F'][i][j] for j in range(3)] for i in range(3)],
                'D':[[faces['D'][i][j] for j in range(3)] for i in range(3)],
                'B':[[faces['B'][i][j] for j in range(3)] for i in range(3)],
                'L':[[faces['L'][i][j] for j in range(3)] for i in range(3)],
                'R':[[faces['R'][i][j] for j in range(3)] for i in range(3)]
            }

    #Matrix setting methods
    def set_up_matrix(self, matrix):
        self.faces['U'] = [[matrix[i][j] for j in range(3)] for i in range(3)]
    def set_front_matrix(self, matrix):
        self.faces['F'] = [[matrix[i][j] for j in range(3)] for i in range(3)]
    def set_down_matrix(self, matrix):
        self.faces['D'] = [[matrix[i][j] for j in range(3)] for i in range(3)]
    def set_back_matrix(self, matrix):
        self.faces['B'] = [[matrix[i][j] for j in range(3)] for i in range(3)]
    def set_left_matrix(self, matrix):
        self.faces['L'] = [[matrix[i][j] for j in range(3)] for i in range(3)]
    def set_right_matrix(self, matrix):
        self.faces['R'] = [[matrix[i][j] for j in range(3)] for i in range(3)]
    #Rotates a matrix 90 degrees clockwise
    def rotate_matrix(self, matrix):
        return [[matrix[3 - j - 1][i] for j in range(3)] for i in range (3)]
    #Moves
    def move_r(self):
        self.faces['R'] = self.rotate_matrix(self.faces['R'])
        temp = [self.faces['U'][0][2], self.faces['U'][1][2], self.faces['U'][2][2]]
        self.faces['U'][0][2] = self.faces['F'][0][2]
        self.faces['U'][1][2] = self.faces['F'][1][2]
        self.faces['U'][2][2] = self.faces['F'][2][2]

        self.faces['F'][0][2] = self.faces['D'][0][2]
        self.faces['F'][1][2] = self.faces['D'][1][2]
        self.faces['F'][2][2] = self.faces['D'][2][2]

        self.faces['D'][0][2] = self.faces['B'][0][2]
        self.faces['D'][1][2] = self.faces['B'][1][2]
        self.faces['D'][2][2] = self.faces['B'][2][2]

        self.faces['B'][0][2] = temp[0]
        self.faces['B'][1][2] = temp[1]
        self.faces['B'][2][2] = temp[2]

    def move_r_prima(self):
        self.move_r()
        self.move_r()
        self.move_r()

    def move_l(self):
        self.faces['L'] = self.rotate_matrix(self.faces['L'])
        temp = [self.faces['D'][0][0], self.faces['D'][1][0], self.faces['D'][2][0]]
        self.faces['D'][0][0] = self.faces['F'][0][2]
        self.faces['D'][1][0] = self.faces['F'][1][2]
        self.faces['D'][2][0] = self.faces['F'][2][2]

        self.faces['F'][0][0] = self.faces['U'][0][2]
        self.faces['F'][1][0] = self.faces['U'][1][2]
        self.faces['F'][2][0] = self.faces['U'][2][2]

        self.faces['U'][0][0] = self.faces['B'][0][2]
        self.faces['U'][1][0] = self.faces['B'][1][2]
        self.faces['U'][2][0] = self.faces['B'][2][2]

        self.faces['B'][0][0] = temp[0]
        self.faces['B'][1][0] = temp[1]
        self.faces['B'][2][0] = temp[2]

    def move_l_prima(self):
        self.move_l()
        self.move_l()
        self.move_l()

    def move_u(self):
        self.faces['U'] = self.rotate_matrix(self.faces['U'])
        temp = [self.faces['F'][2][0], self.faces['F'][2][1], self.faces['F'][2][2]]
        self.faces['F'][2][0] = self.faces['R'][2][2]
        self.faces['F'][2][1] = self.faces['R'][1][2]
        self.faces['F'][2][2] = self.faces['R'][0][2]

        self.faces['R'][2][2] = self.faces['B'][0][2]
        self.faces['R'][1][2] = self.faces['B'][0][1]
        self.faces['R'][0][2] = self.faces['B'][0][0]

        self.faces['B'][0][2] = self.faces['L'][0][0]
        self.faces['B'][0][1] = self.faces['L'][1][0]
        self.faces['B'][0][0] = self.faces['L'][2][0]

        self.faces['L'][0][0] = temp[0]
        self.faces['L'][1][0] = temp[1]
        self.faces['L'][2][0] = temp[2]

    def move_u_prima(self):
        self.move_u()
        self.move_u()
        self.move_u()

    def move_d(self):
        self.faces['D'] = self.rotate_matrix(self.faces['D'])
        temp = [self.faces['F'][0][0], self.faces['F'][0][1], self.faces['F'][0][2]]
        self.faces['F'][0][0] = self.faces['L'][0][2]
        self.faces['F'][0][1] = self.faces['L'][1][2]
        self.faces['F'][0][2] = self.faces['L'][2][2]

        self.faces['L'][0][2] = self.faces['B'][2][2]
        self.faces['L'][1][2] = self.faces['B'][2][1]
        self.faces['L'][2][2] = self.faces['B'][2][0]

        self.faces['B'][2][2] = self.faces['R'][2][0]
        self.faces['B'][2][1] = self.faces['R'][1][0]
        self.faces['B'][2][0] = self.faces['R'][0][0]

        self.faces['R'][2][0] = temp[0]
        self.faces['R'][1][0] = temp[1]
        self.faces['R'][0][0] = temp[2]

    def move_d_prima(self):
        self.move_d()
        self.move_d()
        self.move_d()

    def move_f(self): #tested
        self.faces['F'] = self.rotate_matrix(self.faces['F'])
        temp = [self.faces['U'][0][0], self.faces['U'][0][1], self.faces['U'][0][2]]
        self.faces['U'][0][0] = self.faces['L'][2][2]
        self.faces['U'][0][1] = self.faces['L'][2][1]
        self.faces['U'][0][2] = self.faces['L'][2][0]

        self.faces['L'][2][2] = self.faces['D'][2][2]
        self.faces['L'][2][1] = self.faces['D'][2][1]
        self.faces['L'][2][0] = self.faces['D'][2][0]

        self.faces['D'][2][2] = self.faces['R'][2][2]
        self.faces['D'][2][1] = self.faces['R'][2][1]
        self.faces['D'][2][0] = self.faces['R'][2][0]

        self.faces['R'][2][2] = temp[0]
        self.faces['R'][2][1] = temp[1]
        self.faces['R'][2][0] = temp[2]

    def move_f_prima(self):
        self.move_f()
        self.move_f()
        self.move_f()

    def move_b(self): #tested
        self.faces['B'] = self.rotate_matrix(self.faces['B'])
        temp = [self.faces['U'][2][2], self.faces['U'][2][1], self.faces['U'][2][0]]
        self.faces['U'][2][2] = self.faces['R'][0][0]
        self.faces['U'][2][1] = self.faces['R'][0][1]
        self.faces['U'][2][0] = self.faces['R'][0][2]

        self.faces['R'][0][0] = self.faces['D'][0][0]
        self.faces['R'][0][1] = self.faces['D'][0][1]
        self.faces['R'][0][2] = self.faces['D'][0][2]

        self.faces['D'][0][0] = self.faces['L'][0][0]
        self.faces['D'][0][1] = self.faces['L'][0][1]
        self.faces['D'][0][2] = self.faces['L'][0][2]

        self.faces['L'][0][0] = temp[0]
        self.faces['L'][0][1] = temp[1]
        self.faces['L'][0][2] = temp[2]

    def move_b_prima(self):
        self.move_b()
        self.move_b()
        self.move_b()

    def is_solved(self):
        for face in ['U','D','R','L','F','B']:
            for i in range(3):
                for j in range(3):
                    if(self.faces[face][0][0] != self.faces[face][i][j]):
                        return False
        return True

    def describe(self):
        print 'Rubik\'s Cube Faces:\n'

        spaces = ' ' * (len(self.faces['B'][0]) * 5 + 1)
        print spaces + str(self.faces['B'][0])
        print spaces + str(self.faces['B'][1])
        print spaces + str(self.faces['B'][2])
        print ''

        print str(self.faces['L'][0]) + ' ' + str(self.faces['D'][0]) + ' ' + str(self.faces['R'][0])
        print str(self.faces['L'][1]) + ' ' + str(self.faces['D'][1]) + ' ' + str(self.faces['R'][1])
        print str(self.faces['L'][2]) + ' ' + str(self.faces['D'][2]) + ' ' + str(self.faces['R'][2])
        print ''

        print spaces + str(self.faces['F'][0])
        print spaces + str(self.faces['F'][1])
        print spaces + str(self.faces['F'][2])
        print ''
        
        print spaces + str(self.faces['U'][0])
        print spaces + str(self.faces['U'][1])
        print spaces + str(self.faces['U'][2])
        print ''

    def scramble(self):
        moves = [self.move_b, self.move_f, self.move_d, self.move_l, self.move_u, self.move_r, self.move_b_prima, self.move_f_prima, self.move_d_prima, self.move_l_prima, self.move_u_prima, self.move_r_prima]
        for i in xrange(1, randint(50, 100)):
            choice(moves)()

    def __str__(self):
        return str(self.faces)

if __name__ == '__main__':
    rubik = Rubik()
    rubik.describe()
    rubik.scramble()
    rubik.describe()