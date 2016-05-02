from treelib import Node, Tree
from rubik import Rubik

def solve(rubik, debug=False):
	needed_moves = []
	if debug:
		rubik.describe()

	return needed_moves


if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	moves = solve(rubik, debug=True)
	print moves