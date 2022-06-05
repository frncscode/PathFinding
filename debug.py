import pygame, sys

pygame.init()
font = pygame.font.SysFont('Consolas', 18)

def debug(data, colour = (38, 255, 0)): # Arguments like this: [('Position', pos), ('Colour', 'colour')]
	pos = pygame.math.Vector2()
	displaysurface = pygame.display.get_surface()
	font_surface = font.render('DEBUG:', True, colour)
	font_rect = font_surface.get_rect(topleft = pos)
	displaysurface.blit(font_surface, font_rect)
	pos.y += 20
	for d in data:
		font_surface = font.render(str(d[0]) + ' : ' + str(d[1]), True, colour)
		font_rect = font_surface.get_rect(topleft = pos)
		displaysurface.blit(font_surface, font_rect)
		pos.y += 20
