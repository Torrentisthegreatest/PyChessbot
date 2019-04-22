import pygame
from pygame.locals import *
import storage


class Game:
	columnvalues = [61,114,167,220,273,326,379,432] # x-coords for the board's columns
	rowvalues = [432,379,326,273,220,167,114,63] # y-coords for the board's rows
	whitescore = 0
	blackscore = 0
	showactions = False
	pieceactshowed = {}
	turnowner = "white"

	def __init__(self, configdata):
		self.GameOn = True
		self.config = configdata
		self.screensize = self.width, self.height = 500, 500
		pygame.init()
		self.screen = pygame.display.set_mode(self.screensize)
		pygame.display.set_caption('PyChess')
		
		self.background = pygame.image.load("assets/chessboard.jpg")
		self.background = pygame.transform.scale(self.background, self.screensize)


		while self.GameOn:
			self.screen.blit(self.background,(0,0))
			self.loadpieceimg()
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					pos = x,y = pygame.mouse.get_pos()
					if self.turnowner == "white":
						for piece in self.whitepieces:
							if self.whitepieces.get(piece)["obj_rect"].collidepoint(pos):
								self.toshow = self.wshowmoves(piece)
								break
					if self.turnowner == "black":
						for piece in self.blackpieces:
							if self.blackpieces.get(piece)["obj_rect"].collidepoint(pos):
								self.bshowmoves(piece)
								break
					if self.showactions:
						for action in range(len(self.toshow)):
							if self.toshow[action]["obj_rect"].collidepoint(pos):
								if self.pieceactshowed["team"] == "black":
									newcoord = [self.toshow[action]["coord"][0],self.toshow[action]["coord"][1]]
									self.blackpieces.get(self.pieceactshowed["name"])["pos"] = newcoord
									if self.toshow[action]["kill"]:
										for piece in self.whitepieces:
											if self.whitepieces.get(piece)["pos"] == newcoord:
												self.whitepieces.get(piece)["pos"] = None
												break
								if self.pieceactshowed["team"] == "white":
									newcoord = [self.toshow[action]["coord"][0],self.toshow[action]["coord"][1]]
									self.whitepieces.get(self.pieceactshowed["name"])["pos"] = newcoord
									if self.toshow[action]["kill"]:
										for piece in self.blackpieces:
											if self.blackpieces.get(piece)["pos"] == newcoord:
												self.blackpieces.get(piece)["pos"] = None
												break
								self.showactions = False
								break
			if self.showactions:
				for i in range(len(self.toshow)):
					self.screen.blit(self.toshow[i]["obj"], self.toshow[i]["pos"])
					
			pygame.display.flip()
	
	def getposxy(self, col, row): #returns tuple
		x = self.columnvalues[int(col)]
		y = self.rowvalues[int(row)]
		return (x,y)

	def wshowmoves(self, piece): #returns showacts which is set to self.toshow
		showacts = []
		actions = self.wavailableactions(piece) #actions = [{pos:(x,y),kill:True/False}]
		for actdict in actions:
			act = actions.index(actdict)
			if actions[act]["kill"]:
				actions[act]["obj"] = pygame.image.load("assets/killspace.png").convert_alpha()
				actions[act]["obj_rect"] = actions[act]["obj"].get_rect()
			else:
				actions[act]["obj"] = pygame.image.load("assets/avalspace.png").convert_alpha()
				actions[act]["obj_rect"] = actions[act]["obj"].get_rect()
			actcenterpos = actions[act]["obj_rect"].centerx , actions[act]["obj_rect"].centery = self.getposxy(actions[act]["pos"][0], actions[act]["pos"][1])
			showacts.append({"obj": actions[act]["obj"], "pos": (actions[act]["obj_rect"].x, actions[act]["obj_rect"].y), "coord": actions[act]["pos"], "obj_rect": actions[act]["obj_rect"], "kill": actions[act]["kill"] })
		self.showactions = True
		return showacts

	def wavailableactions(self, piece):
		type = str(piece)[:1]
		if type == "p":
			actions = []
			fwdactpos = [[self.whitepieces.get(piece)["pos"][0], self.whitepieces.get(piece)["pos"][1]+1]]
			if self.whitepieces.get(piece)["pos"][1] == 1: #Is pawn in init location
				fwdactpos.append([self.whitepieces.get(piece)["pos"][0], self.whitepieces.get(piece)["pos"][1]+2])
			for targetP in self.whitepieces:
				if self.whitepieces.get(targetP)["pos"] in fwdactpos:
					fwdactpos.pop(fwdactpos.index(self.whitepieces.get(targetP)["pos"]))
					break
			for targetP in self.blackpieces:
				if self.blackpieces.get(targetP)["pos"] in fwdactpos:
					fwdactpos.pop(fwdactpos.index(self.blackpieces.get(targetP)["pos"]))
					break
			for actpos in fwdactpos:
				actions.append({"pos": (actpos[0], actpos[1]), "kill": False})
			diagactpos = [
						[self.whitepieces.get(piece)["pos"][0]-1, self.whitepieces.get(piece)["pos"][1]+1],
						[self.whitepieces.get(piece)["pos"][0]+1, self.whitepieces.get(piece)["pos"][1]+1]
						]
			for targetP in self.whitepieces:
				if self.whitepieces.get(targetP)["pos"] in diagactpos:
					diagactpos.pop(diagactpos.index(self.whitepieces.get(targetP)["pos"]))
			for targetP in self.blackpieces:
				if self.blackpieces.get(targetP)["pos"] in diagactpos:
					actions.append({"pos": self.blackpieces.get(targetP)["pos"], "kill": True})
			self.pieceactshowed = {"name": str(piece), "team": "white"}
			return actions
		elif type == "b":
			return "bishop"
		elif type == "k":
			return "knight"
		elif type == "r":
			return "rook"
		elif type == "K":
			return "King"
		elif type == "Q":
			return "Queen"
		else:
			raise Exception("White Available Actions: ", "Invalid piece type")

	def loadpieceimg(self):

			#Starting with White Pieces that are alive
			for piece in self.whitepieces:
				if self.whiteisalive(piece):
					sqcord = self.whitepieces.get(piece)["pos"]
					coords = self.getposxy(sqcord[0], sqcord[1])
					self.whitepieces.get(piece)["obj"] = pygame.image.load(self.whitepieces.get(piece)["img"]).convert_alpha()
					self.whitepieces.get(piece)["obj_rect"] = self.whitepieces.get(piece)["obj"].get_rect()
					#imgsize = imgwidth, imgheight = self.whitepieces.get(piece)["obj_rect"].width, self.whitepieces.get(piece)["obj_rect"].height
					self.whitepieces.get(piece)["obj_rect"].centerx = coords[0]
					self.whitepieces.get(piece)["obj_rect"].centery = coords[1]
					rectcoords = rectx, recty = self.whitepieces.get(piece)["obj_rect"].x, self.whitepieces.get(piece)["obj_rect"].y
					self.screen.blit(self.whitepieces.get(piece)["obj"], (rectx, recty) )


			#Starting with Black Pieces that are alive
			for piece in self.blackpieces:
				if self.blackisalive(piece):
					sqcord = self.blackpieces.get(piece)["pos"]
					coords = self.getposxy(sqcord[0], sqcord[1])
					self.blackpieces.get(piece)["obj"] = pygame.image.load(self.blackpieces.get(piece)["img"]).convert_alpha()
					self.blackpieces.get(piece)["obj_rect"] = self.blackpieces.get(piece)["obj"].get_rect()
					#imgsize = imgwidth, imgheight = self.blackpieces.get(piece)["obj_rect"].width, self.blackpieces.get(piece)["obj_rect"].height
					self.blackpieces.get(piece)["obj_rect"].centerx = coords[0]
					self.blackpieces.get(piece)["obj_rect"].centery = coords[1]
					rectcoords = rectx, recty = self.blackpieces.get(piece)["obj_rect"].x, self.blackpieces.get(piece)["obj_rect"].y
					self.screen.blit(self.blackpieces.get(piece)["obj"], (rectx, recty) )
			

	whitepieces = {
		"p1":{"pos":[0,1], "img":"assets/wpawn.png"},
		"p2":{"pos":[1,1], "img":"assets/wpawn.png"},
		"p3":{"pos":[2,1], "img":"assets/wpawn.png"},
		"p4":{"pos":[3,1], "img":"assets/wpawn.png"},
		"p5":{"pos":[4,1], "img":"assets/wpawn.png"},
		"p6":{"pos":[5,1], "img":"assets/wpawn.png"},
		"p7":{"pos":[6,1], "img":"assets/wpawn.png"},
		"p8":{"pos":[7,1], "img":"assets/wpawn.png"},
		"b1":{"pos":[2,0], "img":"assets/wbishop.png"},
		"b2":{"pos":[5,0], "img":"assets/wbishop.png"},
		"k1":{"pos":[1,0], "img":"assets/wknight.png"},
		"k2":{"pos":[6,0], "img":"assets/wknight.png"},
		"r1":{"pos":[0,0], "img":"assets/wrook.png"},
		"r2":{"pos":[7,0], "img":"assets/wrook.png"},
		"K":{"pos":[4,0], "img":"assets/wking.png"},
		"Q":{"pos":[3,0], "img":"assets/wqueen.png"}
	}

	blackpieces = {
		"p1":{"pos":[0,6], "img":"assets/bpawn.png"},
		"p2":{"pos":[1,6], "img":"assets/bpawn.png"},
		"p3":{"pos":[2,6], "img":"assets/bpawn.png"},
		"p4":{"pos":[3,6], "img":"assets/bpawn.png"},
		"p5":{"pos":[4,6], "img":"assets/bpawn.png"},
		"p6":{"pos":[5,6], "img":"assets/bpawn.png"},
		"p7":{"pos":[6,6], "img":"assets/bpawn.png"},
		"p8":{"pos":[7,6], "img":"assets/bpawn.png"},
		"b1":{"pos":[2,7], "img":"assets/bbishop.png"},
		"b2":{"pos":[5,7], "img":"assets/bbishop.png"},
		"k1":{"pos":[1,7], "img":"assets/bknight.png"},
		"k2":{"pos":[6,7], "img":"assets/bknight.png"},
		"r1":{"pos":[0,7], "img":"assets/brook.png"},
		"r2":{"pos":[7,7], "img":"assets/brook.png"},
		"K":{"pos":[4,7], "img":"assets/bking.png"},
		"Q":{"pos":[3,7], "img":"assets/bqueen.png"}
	}

	def whiteisalive(self, piece):
		if self.whitepieces.get(piece)["pos"] == None:
			return False
		else:
			return True

	def blackisalive(self, piece):
		if self.blackpieces.get(piece)["pos"] == None:
			return False
		else:
			return True

