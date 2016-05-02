# Using this tutorial to solve the cube --> http://www.ryanheise.com/cube/human_thistlethwaite_algorithm.html
from treelib import Node, Tree
from rubik import Rubik
import copy

def solve(rubik, debug=False):
	needed_moves = []
	if debug:
		rubik.describe()

	for move in phase_one(rubik, debug):
		needed_moves.append(move)

	for move in phase_two(rubik, debug):
		needed_moves.append(move)

	return needed_moves

def create_cube_from_state(tree, nodeId):
	return Rubik(faces = tree.get_node(nodeId).tag)

def init_phase(rubik):
	tree = Tree()
	tree.add_node(Node(tag = copy.deepcopy(rubik.get_state())))
	return tree

def execute(instructions, step):
	for instruction in instructions[step]:
		instruction()
	return step

def phase_one(rubik, debug):
	tree = init_phase(rubik)
	moves = []
	possible_moves = {
		'u': [rubik.move_u],
		'd': [rubik.move_d],
		'l': [rubik.move_l],
		'r': [rubik.move_r],
		'f2': [rubik.move_f, rubik.move_f],
		'b2': [rubik.move_b, rubik.move_b]
	}

	#TODO add code here to solve phase one, and evaluate

	
	return moves

def phase_two(rubik, debug):
	tree = init_phase(rubik)
	moves = []
	possible_moves = {
		'u': [rubik.move_u],
		'd': [rubik.move_d],
		'l2': [rubik.move_l, rubik.move_l],
		'r2': [rubik.move_r, rubik.move_r],
		'f2': [rubik.move_f, rubik.move_f],
		'b2': [rubik.move_b, rubik.move_b]
	}	

	#TODO add code here to solve phase two, and evaluate

	return moves

def phase_two_edges(rubik, possible_moves, debug):
	pass


def phase_two_corners(rubik, possible_moves, debug):
	pass

def phase_three(rubik, debug):
	tree = init_phase(rubik)
	moves = []
	possible_moves = {
		'u2': [rubik.move_u, rubik.move_u],
		'd2': [rubik.move_d, rubik.move_d],
		'l2': [rubik.move_l, rubik.move_l],
		'r2': [rubik.move_r, rubik.move_r],
		'f2': [rubik.move_f, rubik.move_f],
		'b2': [rubik.move_b, rubik.move_b]
	}	

	#TODO add code here to solve phase three, and evaluate

	return moves

def phase_three_corners(rubik, possible_moves, debug):
	pass

def phase_three_edges(rubik, possible_moves, debug):
	pass

def phase_four(rubik, debug):
	tree = init_phase(rubik)
	moves = []

	#TODO add code here to solve phase four, and evaluate

	return moves

if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	moves = solve(rubik, debug=True)
	print moves