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
	return needed_moves


def execute(possible_instructions, step):
	for instruction in possible_instructions[step]:
		instruction()
	return step

def phase_one(rubik, debug):
	tree = Tree()
	tree.add_node(Node(tag = copy.deepcopy(rubik.get_state())))
	possible_moves = {'u': [rubik.move_u],
					'd': [rubik.move_d],
					'l': [rubik.move_l],
					'r': [rubik.move_r],
					'f2': [rubik.move_f, rubik.move_f],
					'b2': [rubik.move_b, rubik.move_b]}

	#TODO add code here to solve phase one, and evaluate
	
	#rub = Rubik(faces = tree.get_node(tree.root).tag)
	#rub.describe()

	return []

if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	moves = solve(rubik, debug=True)
	print moves