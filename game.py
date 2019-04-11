import pygame
from pygame.locals import *
import storage
pygame.init()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)


class Game():
	whitescore = 0
	blackscore = 0

	whitepieces = {
		"p1":[0,0],
		"p2":[0,0],
		"p3":[0,0],
		"p4":[0,0],
		"p5":[0,0],
		"p6":[0,0],
		"p7":[0,0],
		"p8":[0,0],
		"b1":[0,0],
		"b2":[0,0],
		"k1":[0,0],
		"k2":[0,0],
		"r1":[0,0],
		"r2":[0,0],
		"K":[0,0],
		"Q":[0,0]
	}

	blackpieces = {
		"p1":[0,0],
		"p2":[0,0],
		"p3":[0,0],
		"p4":[0,0],
		"p5":[0,0],
		"p6":[0,0],
		"p7":[0,0],
		"p8":[0,0],
		"b1":[0,0],
		"b2":[0,0],
		"k1":[0,0],
		"k2":[0,0],
		"r1":[0,0],
		"r2":[0,0],
		"K":[0,0],
		"Q":[0,0]
	}

	def whiteisalive(self, piece):
		if self.whitepieces[piece] == None:
			return False
		else:
			return True

	def blackisalive(self, piece):
		if self.blackpieces[piece] == None:
			return False
		else:
			return True

