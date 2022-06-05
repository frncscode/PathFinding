import math, time

class Node:

	def __init__(self, val, pos):
		self.pos = pos
		self.val = val
		self.g = 0
		self.h = 0 
		self.parent = None
		self.cost = 10


class PathFinding:		

	def gridToNode(grid):
		return [[Node(col, (rowIdx, colIdx)) for colIdx, col in enumerate(row)] for rowIdx, row in enumerate(grid)]

	def heuristic(current_pos, target_pos):
		# Using Euclidean Distance Heuristic
		# Assuming Each Square weighs 10 Distance
		current_node_pos = (current_pos[0] * 10, current_pos[1] * 10)
		target_node_pos = (target_pos[0] * 10, target_pos[1] * 10)
		return int(math.sqrt((current_node_pos[0] - target_node_pos[0])**2 + (current_node_pos[1] - target_node_pos[1]) ** 2))

	def getDiagonals(pos, grid):
		left, right = (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)
		top, bottom = (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])
		topright, topleft = (right[0] - 1, right[1]), (left[0] - 1, left[1])
		bottomright, bottomleft = (right[0] + 1, right[1]), (left[0] + 1, left[1])
		return [topright, topleft, bottomright, bottomleft]


	def children(pos, grid):
		# Getting the Adjacent Nodes
		left, right = (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)
		top, bottom = (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])
		topright, topleft = (right[0] - 1, right[1]), (left[0] - 1, left[1])
		bottomright, bottomleft = (right[0] + 1, right[1]), (left[0] + 1, left[1])

		# Only returning valid children
		res = [childPos for childPos in [left, right, top, bottom] if (0 <= childPos[0] < len(grid[0]) and 0 <= childPos[1] < len(grid))]
		
		if top in res:
			if grid[top[0]][top[1]].val == 1:
				if topleft in res:
					res.remove(topleft)
				if topright in res:
					res.remove(topright)
		if bottom in res:
			if grid[bottom[0]][bottom[1]].val == 1:
				if bottomright in res:
					res.remove(bottomright)
				if bottomleft in res:
					res.remove(bottomleft)

		return res

	def Find(grid):
		grid = PathFinding.gridToNode(grid)
		# Parsing the Grid for start and end nodes
		for row in grid:
			for node in row:
				if node.val == 2: # Start Node
					start = node
				elif node.val == 3:
					end = node

		return PathFinding.AStar(start, end, grid)
		
	def AStar(source, target, grid):
		# Defining the starting lists
		openList = set([source])
		closedList = set()

		while openList:
			# Finding Node with lowest fitness value
			current = min(openList, key = lambda node: node.g + node.h)

			if current == target:
				path = [target]
				while current != source:
					path.append(current.parent)
					current = current.parent
				return path
				
			openList.remove(current)
			closedList.add(current)

			for childPos in PathFinding.children(current.pos, grid):
				childNode = grid[childPos[0]][childPos[1]]
				if not(childNode in closedList or childNode.val == 1): # 1 means obstacle
					if childNode not in openList:
						openList.add(childNode)
						childNode.parent = current
						cost = 10
						if childNode.pos in PathFinding.getDiagonals(current.pos, grid):
							cost = 14
						childNode.g = current.g + cost
						childNode.h = PathFinding.heuristic(childNode.pos, target.pos)
					elif childNode in openList:
						if current.g + childNode.cost < childNode.g:
							childNode.parent = current
							childNode.g = current.g + cost
							childNode.h = PathFinding.heuristic(childNode.pos, target.pos)



if __name__ == '__main__':
	testMap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	for i in testMap:
		print(i)
	for i in PathFinding.Find(testMap):
		testMap[i.pos[0]][i.pos[1]] = 'x'
	for i  in testMap:
		print(i)
