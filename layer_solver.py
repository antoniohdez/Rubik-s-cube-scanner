from rubik import Rubik



def first_layer(rubik):

	return []

def solve(rubik, debug=False):
	moves = []
	moves.extend(first_layer(rubik))
	return moves

def first_cross(rubik, debug=False):
	# UB 21, #UR 12, #UF 01, #UL 10
	color_U = rubik.faces['U'][1][1]
	color_F = rubik.faces['F'][1][1]
	color_R = rubik.faces['R'][1][1]
	color_L = rubik.faces['L'][1][1]
	color_B = rubik.faces['B'][1][1]
	color_D = rubik.faces['D'][1][1]

	pieces = ['U21', 'U12', 'U01', 'U10']
	opposites = [color_B, color_R, color_F, color_L]
	red_blocks = rubik.is_top_cross_done()
	relatively_correct = [False, False, False, False]
	for i in xrange(len(red_blocks)):
		opposite = get_opposite_edge_color(rubik, pieces[i])
		relatively_correct[i] = red_blocks[i] and opposites[i] == opposite
	for i in xrange(len(relatively_correct)):
		if not relatively_correct[i]:
			face, x, y = find_edge(rubik, [color_U, opposites[i]])
			
def find_edge(rubik, colors):
	edge_coordinates = [(2,1),(1,2),(0,1),(1,0)]
	for face in rubik.faces.keys():
		for i,j in edge_coordinates:
			if rubik.faces[face][i][j] == colors[0] and get_opposite_edge_color(rubik, face + str(i) + str(j)) == colors[1]:
				return face, i, j


def get_opposite_edge_color(rubik, key):
	dictionary = {
		'U01': rubik.faces['F'][2][1],
		'U10': rubik.faces['L'][1][0],
		'U12': rubik.faces['R'][1][2],
		'U21': rubik.faces['B'][0][1],
	}
	return dictionary[key]
if __name__ == '__main__':
	rubik = Rubik()
	first_cross(rubik)
	rubik.describe()
	#solve(rubik)
