# Using this tutorial to solve the cube --> http://www.ryanheise.com/cube/human_thistlethwaite_algorithm.html
# encoding=utf-8
from treelib import Node, Tree
from collections import deque
from copy import deepcopy
from rubik import Rubik
from sets import Set

class Solver(object):
	"""Rubik's Cube Solver"""
	rubik = None
	moves = {}
	phase_one_moves = {}
	phase_two_moves = {}
	phase_three_moves = {}
	phase_four_moves = {}

	def __init__(self, rubik):
		self.rubik = rubik
		self.moves = {
			'u': [self.rubik.move_u],
			'd': [self.rubik.move_d],
			'l': [self.rubik.move_l],
			'r': [self.rubik.move_r],
			'l2': [self.rubik.move_l, self.rubik.move_l],
			'r2': [self.rubik.move_r, self.rubik.move_r],
			'u2': [self.rubik.move_u, self.rubik.move_u],
			'd2': [self.rubik.move_d, self.rubik.move_d],
			'f2': [self.rubik.move_f, self.rubik.move_f],
			'b2': [self.rubik.move_b, self.rubik.move_b]
		}

		self.phase_one_moves = {
			'u': self.moves['u'],
			'd': self.moves['d'],
			'l': self.moves['l'],
			'r': self.moves['r'],
			'f2': self.moves['f2'],
			'b2': self.moves['b2']
		}

		self.phase_two_moves = {
			'u': self.moves['u'],
			'd': self.moves['d'],
			'l2': self.moves['l2'],
			'r2': self.moves['r2'],
			'f2': self.moves['f2'],
			'b2': self.moves['b2']
		}

		self.phase_three_moves = {
			'u2': self.moves['u2'],
			'd2': self.moves['d2'],
			'l2': self.moves['l2'],
			'r2': self.moves['r2'],
			'f2': self.moves['f2'],
			'b2': self.moves['b2']
		}

		self.phase_four_moves = self.phase_three_moves
		
	def solve(self, debug=False):
		needed_moves = []
		if debug:
			rubik.describe()

		for move in self.phase_one(rubik, needed_moves, debug):
			needed_moves.append(move)

		for move in self.phase_two(rubik, debug):
			needed_moves.append(move)

		return needed_moves

	def create_cube_from_node(self, tree, node_id):
		return Rubik(faces = tree.get_node(node_id).tag['state'])

	def init_phase(self, rubik, steps_required = []):
		tree = Tree()
		tree.add_node(Node(tag = {'state': deepcopy(rubik.get_state()), 'steps_required': steps_required}))
		return tree

	def execute(self, instructions, step):
		for instruction in instructions[step]:
			instruction()
		return step


	def add_state(self, tree, node_id, state, states, step):
		steps = deepcopy(tree.get_node(node_id).tag['steps_required'])
		if str(state) not in states:
			steps.append(step)
			states.add(str(state))
			tree.create_node(parent=node_id, tag={'rubik': state, 'steps_required': steps})

	def bfs(self, tree, moves, validate_state):
		states = Set()
		rubikHolder = deepcopy(self.rubik)
		for move in moves.keys():
			step = self.execute(moves, move)
			self.add_state(tree, tree.root, self.rubik.get_state(), states, step)
			self.rubik = rubikHolder
		q = deque([tree.get_node(tree.root)])
		while q:
			current = q.popleft()
			for node in tree.children(current.identifier):
				rubikHolder = deepcopy(self.rubik)
				for move in moves.keys():
					step = self.execute(moves, move)
					self.add_state(tree, current.identifier, self.rubik.get_state(), states, step)
					self.rubik = rubikHolder
					q.append(node)

		print tree


	def validate_phase_one(self, state):
		return False

	def phase_one(self, rubik, needed_moves, debug):
		tree = self.init_phase(rubik)
		moves = []

		self.bfs(tree, self.phase_one_moves, self.validate_phase_one)


		#TODO add code here to solve phase one, and evaluate
		return moves

	def phase_two(self, rubik, debug):
		tree = self.init_phase(rubik)
		moves = []

		#TODO add code here to solve phase two, and evaluate

		return moves

	def phase_two_edges(self, rubik, possible_moves, debug):
		pass


	def phase_two_corners(self, rubik, possible_moves, debug):
		pass

	def phase_three(self, rubik, debug):
		tree = self.init_phase(rubik)
		moves = []

		#TODO add code here to solve phase three, and evaluate

		return moves

	def phase_three_corners(self, rubik, possible_moves, debug):
		pass

	def phase_three_edges(self, rubik, possible_moves, debug):
		pass

	def phase_four(self, rubik, debug):
		tree = init_phase(rubik)
		moves = []

		#TODO add code here to solve phase four, and evaluate

		return moves

if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	solver = Solver(rubik)
	moves = solver.solve(debug=True)
	print moves