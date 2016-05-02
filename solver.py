# Using this tutorial to solve the cube --> http://www.ryanheise.com/cube/human_thistlethwaite_algorithm.html
# encoding=utf-8
from treelib import Node, Tree
from collections import deque
from rubik import Rubik
from sets import Set

def get_moves(rubik, type):
	moves = {
		'u': [rubik.move_u],
		'd': [rubik.move_d],
		'l': [rubik.move_l],
		'r': [rubik.move_r],
		'f': [rubik.move_r],
		'b': [rubik.move_r],
		'l2': [rubik.move_l2],
		'r2': [rubik.move_r2],
		'u2': [rubik.move_u2],
		'd2': [rubik.move_d2],
		'f2': [rubik.move_f2],
		'b2': [rubik.move_b2],
		'uP': [rubik.move_u_prima],
		'dP': [rubik.move_d_prima],
		'lP': [rubik.move_l_prima],
		'rP': [rubik.move_r_prima],
		'fP': [rubik.move_f_prima],
		'bP': [rubik.move_b_prima]
	}
	if type == 'phase_one': #all moves possible
		return moves
	elif type == 'phase_two': #G1 moves <L2,R2,F,B,U,D>
		return {
			'l2': moves['l2'],
			'r2': moves['r2'],
			'f': moves['f'],
			'fP': moves['fP'],
			'f2': moves['f2'],
			'b': moves['b'],
			'bP': moves['bP'],
			'b2': moves['b2'],
			'u': moves['u'],
			'uP': moves['uP'],
			'u2': moves['u2'],
			'd': moves['d'],
			'dP': moves['dP'],
			'd2': moves['d2']
		}

	elif type == 'phase_three': #G2 moves <L2,R2,F2,B2,U,D>
		return {
			'l2': moves['l2'],
			'r2': moves['r2'],
			'f2': moves['f2'],
			'b2': moves['b2'],
			'u': moves['u'],
			'uP': moves['uP'],
			'u2': moves['u2'],
			'd': moves['d'],
			'dP': moves['dP'],
			'd2': moves['d2']
		}

	elif type == 'phase_four': #G3 moves <L2,R2,F2,B2,U2,D2>
		return {
			'l2': moves['l2'],
			'r2': moves['r2'],
			'f2': moves['f2'],
			'b2': moves['b2'],
			'u2': moves['u2'],
			'd2': moves['d2']
		}

def solve(rubik, debug=False):
	needed_moves = []
	if debug:
		rubik.describe()
	moves,rubik = phase_one(rubik, debug);
	needed_moves.extend(moves)
	if debug:
		print needed_moves
		rubik.describe()
	moves,rubik = phase_two(rubik, debug);
	needed_moves.extend(moves)
	if debug:
		print needed_moves
		rubik.describe()
	moves,rubik = phase_three(rubik, debug);
	needed_moves.extend(moves)
	if debug:
		print needed_moves
		rubik.describe()
	moves,rubik = phase_four(rubik, debug);
	needed_moves.extend(moves)
	if debug:
		print needed_moves
		rubik.describe()


	return needed_moves

def create_cube_from_node(tree, node_id):
	return Rubik(tree.get_node(node_id).identifier)

def init_phase(rubik, steps_required = []):
	tree = Tree()
	tree.add_node(Node(identifier = rubik.copy(), tag = {'steps': steps_required}))
	return tree

def execute(instructions, step):
	for instruction in instructions[step]:
		instruction()
	return step

def add_movements(tree, parent_node_id, phase, states):
	moves = get_moves(tree.get_node(parent_node_id).identifier, phase).keys()
	for move in moves:
		rubik = tree.get_node(parent_node_id).identifier.copy()
		step = execute(get_moves(rubik, phase), move)
		steps = tree.get_node(parent_node_id).tag['steps'][:]
		steps.append(step)
		if (str(rubik.get_state()) not in states):
			states.add(str(rubik.get_state()))
			tree.create_node(identifier = rubik, parent = parent_node_id, tag = {'steps': steps})

def bfs(rubik, tree, phase, validate_state):
	states = Set()
	add_movements(tree, tree.root, phase, states)
	q = deque([tree.get_node(tree.root)])
	while q:
		current = q.popleft()
		for node in tree.children(current.identifier):
			add_movements(tree, node.identifier, phase, states)
			if (validate_state(current.identifier)):
				rubik = current.identifier
				return current.tag['steps'], rubik
			q.append(node)

def validate_phase_one(rubik):
	for i in xrange(3):
		for j in xrange(3):
			if(rubik.faces['F'][i][j] == 'R' or rubik.faces['F'][i][j] == 'O' or
					rubik.faces['B'][i][j] == 'R' or rubik.faces['B'][i][j] == 'O' or
					rubik.faces['U'][i][j] == 'W' or rubik.faces['U'][i][j] == 'Y' or
					rubik.faces['D'][i][j] == 'W' or rubik.faces['D'][i][j] == 'Y'):
				return False
	return True

def phase_one(rubik, debug):
	tree = init_phase(rubik)
	moves = bfs(rubik, tree, 'phase_one', validate_phase_one)
	if debug:
		pass #print tree
	return moves


def validate_phase_two_edges(rubik):
	if (rubik.faces['U'][0][1] != 'R' and rubik.faces['U'][0][1] != 'O' or
			rubik.faces['U'][1][0] != 'R' and rubik.faces['U'][1][0] != 'O' or
			rubik.faces['U'][1][1] != 'R' and rubik.faces['U'][1][1] != 'O' or
			rubik.faces['U'][1][2] != 'R' and rubik.faces['U'][1][2] != 'O' or
			rubik.faces['U'][2][1] != 'R' and rubik.faces['U'][2][1] != 'O' or
			rubik.faces['D'][0][1] != 'R' and rubik.faces['D'][0][1] != 'O' or
			rubik.faces['D'][1][0] != 'R' and rubik.faces['D'][1][0] != 'O' or
			rubik.faces['D'][1][1] != 'R' and rubik.faces['D'][1][1] != 'O' or
			rubik.faces['D'][1][2] != 'R' and rubik.faces['D'][1][2] != 'O' or
			rubik.faces['D'][2][1] != 'R' and rubik.faces['D'][2][1] != 'O'):
		return False
	return True

def validate_phase_two_corners(rubik):
	for i in xrange(3):
		for j in xrange(3):
			if(rubik.faces['U'][i][j] != 'R' and rubik.faces['U'][i][j] != 'O' or
					rubik.faces['D'][i][j] != 'R' and rubik.faces['D'][i][j] == 'O'):
				return False
	return True

def phase_two(rubik, debug):
	moves = []
	moves.extend(phase_two_edges(rubik, debug))
	moves.extend(phase_two_corners(rubik, debug))
	return moves

def phase_two_edges(rubik, debug):
	tree = init_phase(rubik)
	moves = bfs(rubik, tree, 'phase_two', validate_phase_two_edges)
	if debug:
		pass #print tree
	return moves


def phase_two_corners(rubik, debug):
	tree = init_phase(rubik)
	moves = bfs(rubik, tree, 'phase_two', validate_phase_two_corners)
	if debug:
		pass #print tree
	return moves

def validate_phase_three_edges(rubik):
	for i in xrange(3):
		for j in xrange(3):
			if(rubik.faces['F'][i][j] != 'W' and rubik.faces['F'][i][j] != 'Y' or
					rubik.faces['B'][i][j] != 'W' and rubik.faces['B'][i][j] != 'Y' or
					rubik.faces['U'][i][j] != 'R' and rubik.faces['U'][i][j] != 'O' or
					rubik.faces['D'][i][j] != 'R' and rubik.faces['D'][i][j] != 'O' or
					rubik.faces['R'][i][j] != 'G' and rubik.faces['R'][i][j] != 'B' or
					rubik.faces['L'][i][j] != 'G' and rubik.faces['L'][i][j] != 'B' ):
				return False
	return True

def validate_phase_three_corners(rubik):
	if(rubik.faces['D'][0][0] == rubik.faces['U'][0][2]): # all matches
		if(rubik.faces['D'][0][2] == rubik.faces['U'][2][2] and
				rubik.faces['D'][2][0] == rubik.faces['U'][0][0] and
				rubik.faces['D'][2][2] == rubik.faces['U'][0][2]):
			return True
	else: #no matches
		if(rubik.faces['D'][0][2] != rubik.faces['U'][2][2] and
				rubik.faces['D'][2][0] != rubik.faces['U'][0][0] and
				rubik.faces['D'][2][2] != rubik.faces['U'][0][2]):
			return True
	return False

def phase_three(rubik, debug):
	moves = []
	moves.extend(phase_three_corners(rubik, debug))
	moves.extend(phase_three_edges(rubik, debug))
	return moves

def phase_three_corners(rubik, debug):
	tree = init_phase(rubik)
	moves = bfs(rubik, tree, 'phase_three', validate_phase_three_corners)
	if debug:
		pass #print tree
	return moves

def phase_three_edges(rubik, debug):
	tree = init_phase(rubik)
	moves = bfs(rubik, tree, 'phase_three', validate_phase_three_edges)
	if debug:
		pass #print tree
	return moves

def validate_phase_four(rubik):
	return rubik.is_solved()

def phase_four(rubik, debug):
	tree = init_phase(rubik)
	moves = bfs(rubik, tree, 'phase_four', validate_phase_four)
	if debug:
		pass #print tree
	return moves

if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	moves = solve(rubik, debug=True)
	print moves
