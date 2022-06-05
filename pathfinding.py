import pygame, sys
from debug import *
from pathfindingAlgorithms import PathFinding

# Environment class for pygame loop
class Env:
	DIMESIONS = (600, 600)
	TILESIZE = 20
	FPS = 120

	def __init__(self):
		# Basic pygame setup
		self.win = pygame.display.set_mode(Env.DIMESIONS)
		self.clock = pygame.time.Clock()
		self.pathToDraw = []

		pygame.display.set_caption('PathFinding Visualization - Francis')

		# Defining the map which splits the screen into tiles which are either empty (0) or obstacles (1)
		self.map_template = [[0 for _ in range(Env.DIMESIONS[0] // Env.TILESIZE)] for _ in range(Env.DIMESIONS[1] // Env.TILESIZE)]
		self.map = self.map_template

	
	def drawMap(self):
		self.win.fill((255, 255, 255))
		for rowIdx, row in enumerate(self.map):
			for colIdx, col in enumerate(row):
				if col == 1:
					pygame.draw.rect(self.win, (125, 125, 125), (rowIdx * Env.TILESIZE, colIdx * Env.TILESIZE, Env.TILESIZE, Env.TILESIZE))
				elif col == 2:
					pygame.draw.circle(self.win, (3, 213, 255), (rowIdx * Env.TILESIZE + Env.TILESIZE // 2, colIdx * Env.TILESIZE + Env.TILESIZE // 2), Env.TILESIZE / 2)
				elif col == 3:
					pygame.draw.circle(self.win, (227, 32, 18), (rowIdx * Env.TILESIZE + Env.TILESIZE // 2, colIdx * Env.TILESIZE + Env.TILESIZE // 2), Env.TILESIZE / 2)


	def prompt(self, message):
		font = pygame.font.SysFont('Consolas', 25 )
		fontImage = font.render(str(message), True, 'black')
		fontRect = fontImage.get_rect(midtop = (Env.DIMESIONS[0] // 2, Env.DIMESIONS[1] // 2))
		self.win.blit(fontImage, fontRect)

	def run(self):
		promptStage = 0
		mouseDown = False
		promptDict = {0: 'Place Start Point', 1: 'Place End Point', 2: 'Draw Obstacles, Press Space To Begin', 3: ''}
		# Standard pygame main loop
		while True:
			mouseX, mouseY = pygame.mouse.get_pos()
			self.drawMap()
			for i in range(len(self.pathToDraw) - 1):
				pygame.draw.line(self.win, 'green', (self.pathToDraw[i].pos[0] * Env.TILESIZE + (0.5 * Env.TILESIZE), self.pathToDraw[i].pos[1] * Env.TILESIZE + (0.5 * Env.TILESIZE)), (self.pathToDraw[i + 1].pos[0] * Env.TILESIZE + (0.5 * Env.TILESIZE), self.pathToDraw[i + 1].pos[1] * Env.TILESIZE + (0.5 * Env.TILESIZE)), width = 5)
			self.prompt(promptDict[promptStage])
			currentTilePos = (mouseX // Env.TILESIZE, mouseY // Env.TILESIZE)

			# Handling events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and promptStage == 2:
						path = PathFinding.Find(self.map)
						if path:
							promptDict[3] = 'Path Found!'
							path.reverse()
							for i in path:
								self.pathToDraw.append(i)
						else:
							promptDict[3] = 'No Valid Path Found!'
						promptStage += 1
				
					if event.key == pygame.K_BACKSPACE and promptStage == 3:
						self.map = [[0 for i in row] for row in self.map]
						self.pathToDraw.clear()
						promptStage -= 3


				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and promptStage == 0:
					if self.map[currentTilePos[0]][currentTilePos[1]] == 0:
						self.map[currentTilePos[0]][currentTilePos[1]] = 2
						promptStage += 1
						break

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and promptStage == 1:
					if self.map[currentTilePos[0]][currentTilePos[1]] == 0:
						self.map[currentTilePos[0]][currentTilePos[1]] = 3
						promptStage += 1
						break

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and promptStage == 2:
					mouseDown = True

				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and promptStage == 2:
					mouseDown = False

			if mouseDown:
				if self.map[currentTilePos[0]][currentTilePos[1]] == 0:
					self.map[currentTilePos[0]][currentTilePos[1]] = 1

			pygame.display.update()
			self.clock.tick(Env.FPS)

Env().run()