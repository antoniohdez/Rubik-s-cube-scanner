from rubik import Rubik



def first_layer(rubik):
	
	return []

def solve(rubik, debug=False):
	moves = []
	moves.extend(first_layer(rubik))
	return moves

if __name__ == '__main__':
	rubik = Rubik()
	rubik.scramble()
	rubik.describe()
	solve(rubik)