# Using this tutorial to solve the cube --> http://www.ryanheise.com/cube/human_thistlethwaite_algorithm.html
# encoding=utf-8
from treelib import Node, Tree
from collections import deque
from rubik import Rubik
from sets import Set


rubik = None
moves = {}
phase_one_moves = {}
phase_two_moves = {}
phase_three_moves = {}
phase_four_moves = {}

def get_moves(rubik, type):
	moves = {
		'u': [rubik.move_u],
		'd': [rubik.move_d],
		'l': [rubik.move_l],
		'r': [rubik.move_r],
		'l2': [rubik.move_l, rubik.move_l],
		'r2': [rubik.move_r, rubik.move_r],
		'u2': [rubik.move_u, rubik.move_u],
		'd2': [rubik.move_d, rubik.move_d],
		'f2': [rubik.move_f, rubik.move_f],
		'b2': [rubik.move_b, rubik.move_b]
	}
	if type == 'phase_one':
		return {
			'u': moves['u'],
			'd': moves['d'],
			'l': moves['l'],
			'r': moves['r'],
			'f2': moves['f2'],
			'b2': moves['b2']
		}

	elif type == 'phase_two':
		return {
			'u': moves['u'],
			'd': moves['d'],
			'l2': moves['l2'],
			'r2': moves['r2'],
			'f2': moves['f2'],
			'b2': moves['b2']
		}

	elif type == 'phase_three' or type == 'phase_four':
		return {
			'u2': moves['u2'],
			'd2': moves['d2'],
			'l2': moves['l2'],
			'r2': moves['r2'],
			'f2': moves['f2'],
			'b2': moves['b2']
		}
	
def solve(rubik, debug=False):
	needed_moves = []
	if debug:
		rubik.describe()

	needed_moves.extend(phase_one(rubik, debug))
	needed_moves.extend(phase_two(rubik, debug))
	needed_moves.extend(phase_three(rubik, debug))
	needed_moves.extend(phase_four(rubik, debug))
		

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
				return current.tag['steps']
			q.append(node)

def validate_phase_one(rubik):
	return False

def phase_one(rubik, debug):
	tree = init_phase(rubik)
	return bfs(rubik, tree, 'phase_one', validate_phase_one)


def validate_phase_two_edges(rubik):
	return False

def validate_phase_two_corners(rubik):
	return False

def phase_two(rubik, debug):
	moves = []
	moves.extend(phase_two_edges(rubik, debug))
	moves.extend(phase_two_corners(rubik, debug))
	return moves

def phase_two_edges(rubik, debug):
	tree = init_phase(rubik)
	return bfs(rubik, tree, 'phase_two', validate_phase_two_edges)


def phase_two_corners(rubik, debug):
	tree = init_phase(rubik)
	return bfs(rubik, tree, 'phase_two', validate_phase_two_corners)

def validate_phase_three_edges(rubik):
	return False

def validate_phase_three_corners(rubik):
	return False

def phase_three(rubik, debug):
	moves = []
	moves.extend(phase_three_edges(rubik, debug))
	moves.extend(phase_three_corners(rubik, debug))
	return moves

def phase_three_corners(rubik, debug):
	tree = init_phase(rubik)
	return bfs(rubik, tree, 'phase_three', validate_phase_three_corners)

def phase_three_edges(rubik, debug):
	tree = init_phase(rubik)
	return bfs(rubik, tree, 'phase_three', validate_phase_three_edges)

def validate_phase_four(rubik):
	return rubik.is_solved()

def phase_four(rubik, debug):
	tree = init_phase(rubik)
	return bfs(rubik, tree, 'phase_four', validate_phase_four)

if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	moves = solve(rubik, debug=True)
	print moves