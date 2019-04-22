import pygame
from pygame.locals import *
import storage


class Game:
	columnvalues = [61,114,167,220,273,326,379,432] # x-coords for the board's columns
	rowvalues = [432,379,326,273,220,167,114,63] # y-coords for the board's rows
	whitescore = 0
	blackscore = 0
	showactions = False
	turnowner = "w"
	pieceactshowed = ""

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
					for piece in self.pieces:
						if 1:#self.teaminturn(piece):
							if self.pieces.get(piece)["obj_rect"].collidepoint(pos):
								self.toshow = self.showmoves(piece)
								break
					if self.showactions:
						for action in range(len(self.toshow)):
							if self.toshow[action]["obj_rect"].collidepoint(pos):
								newcoord = [self.toshow[action]["coord"][0],self.toshow[action]["coord"][1]]
								self.pieces.get(self.pieceactshowed)["pos"] = newcoord
								if self.toshow[action]["kill"]:
									for piece in self.pieces:
										if self.pieces.get(piece)["pos"] == newcoord:
											self.pieces.get(piece)["pos"] = None
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

	def showmoves(self, piece): #returns showacts which is set to self.toshow
		showacts = []
		actions = self.availableactions(piece) #actions = [{pos:(x,y),kill:True/False}]
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

	def availableactions(self, piece):
		type = str(piece)
		if type[1:2] == "p":
			badj = 1
			if type[:1] == "b":
				badj = -1
			actions = []
			fwdactpos = [[self.pieces.get(piece)["pos"][0], self.pieces.get(piece)["pos"][1]+(1*badj)]]
			if (self.pieces.get(piece)["pos"][1] == 1 and str(piece)[:1] == "w") or (self.pieces.get(piece)["pos"][1] == 6 and str(piece)[:1] == "b"): #Is pawn in init location
				fwdactpos.append([self.pieces.get(piece)["pos"][0], self.pieces.get(piece)["pos"][1]+(2*badj)])
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in fwdactpos:
					if self.pieces.get(piece)["pos"][1] + (1*badj) == self.pieces.get(targetP)["pos"]:
						fwdactpos = []
						break
					else:
						fwdactpos.pop(fwdactpos.index(self.pieces.get(targetP)["pos"]))
						break
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in fwdactpos:
					if self.pieces.get(piece)["pos"][1] + (1*badj) == self.pieces.get(targetP)["pos"]:
						fwdactpos.clear()
					else:
						fwdactpos.pop(fwdactpos.index(self.pieces.get(targetP)["pos"]))
					break
			for actpos in fwdactpos:
				actions.append({"pos": (actpos[0], actpos[1]), "kill": False})
			diagactpos = [
						[self.pieces.get(piece)["pos"][0]-1, self.pieces.get(piece)["pos"][1]+(1*badj)],
						[self.pieces.get(piece)["pos"][0]+1, self.pieces.get(piece)["pos"][1]+(1*badj)]
						]
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in diagactpos:
					diagactpos.pop(diagactpos.index(self.pieces.get(targetP)["pos"]))
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in diagactpos:
					actions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
			self.pieceactshowed = str(piece)
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

	def teaminturn(self, piece):
		if str(piece)[1:] == "K" or str(piece)[:1] == "Q":
			if str(piece)[:1] == self.turnowner:
				return True
		elif str(piece)[:1] == self.turnowner:
			return True
		else:
			return False

	def loadpieceimg(self):

			#Starting with White Pieces that are alive
			for piece in self.pieces:
				if self.isalive(piece):
					sqcord = self.pieces.get(piece)["pos"]
					coords = self.getposxy(sqcord[0], sqcord[1])
					self.pieces.get(piece)["obj"] = pygame.image.load(self.pieces.get(piece)["img"]).convert_alpha()
					self.pieces.get(piece)["obj_rect"] = self.pieces.get(piece)["obj"].get_rect()
					self.pieces.get(piece)["obj_rect"].centerx = coords[0]
					self.pieces.get(piece)["obj_rect"].centery = coords[1]
					rectcoords = rectx, recty = self.pieces.get(piece)["obj_rect"].x, self.pieces.get(piece)["obj_rect"].y
					self.screen.blit(self.pieces.get(piece)["obj"], (rectx, recty) )

			#
			# #Starting with Black Pieces that are alive
			# for piece in self.pieces:
			# 	if self.isalive(piece):
			# 		sqcord = self.pieces.get(piece)["pos"]
			# 		coords = self.getposxy(sqcord[0], sqcord[1])
			# 		self.pieces.get(piece)["obj"] = pygame.image.load(self.pieces.get(piece)["img"]).convert_alpha()
			# 		self.pieces.get(piece)["obj_rect"] = self.pieces.get(piece)["obj"].get_rect()
			# 		self.pieces.get(piece)["obj_rect"].centerx = coords[0]
			# 		self.pieces.get(piece)["obj_rect"].centery = coords[1]
			# 		rectcoords = rectx, recty = self.pieces.get(piece)["obj_rect"].x, self.pieces.get(piece)["obj_rect"].y
			# 		self.screen.blit(self.pieces.get(piece)["obj"], (rectx, recty) )
			#

	pieces = {
		"wp1":{"pos":[0,1], "img":"assets/wpawn.png"},
		"wp2":{"pos":[1,1], "img":"assets/wpawn.png"},
		"wp3":{"pos":[2,1], "img":"assets/wpawn.png"},
		"wp4":{"pos":[3,1], "img":"assets/wpawn.png"},
		"wp5":{"pos":[4,1], "img":"assets/wpawn.png"},
		"wp6":{"pos":[5,1], "img":"assets/wpawn.png"},
		"wp7":{"pos":[6,1], "img":"assets/wpawn.png"},
		"wp8":{"pos":[7,1], "img":"assets/wpawn.png"},
		"wb1":{"pos":[2,0], "img":"assets/wbishop.png"},
		"wb2":{"pos":[5,0], "img":"assets/wbishop.png"},
		"wk1":{"pos":[1,0], "img":"assets/wknight.png"},
		"wr1":{"pos":[0,0], "img":"assets/wrook.png"},
		"wk2":{"pos":[6,0], "img":"assets/wknight.png"},
		"wr2":{"pos":[7,0], "img":"assets/wrook.png"},
		"wK":{"pos":[4,0], "img":"assets/wking.png"},
		"wQ":{"pos":[3,0], "img":"assets/wqueen.png"},

		"bp1":{"pos":[0,6], "img":"assets/bpawn.png"},
		"bp2":{"pos":[1,6], "img":"assets/bpawn.png"},
		"bp3":{"pos":[2,6], "img":"assets/bpawn.png"},
		"bp4":{"pos":[3,6], "img":"assets/bpawn.png"},
		"bp5":{"pos":[4,6], "img":"assets/bpawn.png"},
		"bp6":{"pos":[5,6], "img":"assets/bpawn.png"},
		"bp7":{"pos":[6,6], "img":"assets/bpawn.png"},
		"bp8":{"pos":[7,6], "img":"assets/bpawn.png"},
		"bb1":{"pos":[2,7], "img":"assets/bbishop.png"},
		"bb2":{"pos":[5,7], "img":"assets/bbishop.png"},
		"bk1":{"pos":[1,7], "img":"assets/bknight.png"},
		"bk2":{"pos":[6,7], "img":"assets/bknight.png"},
		"br1":{"pos":[0,7], "img":"assets/brook.png"},
		"br2":{"pos":[7,7], "img":"assets/brook.png"},
		"bK":{"pos":[4,7], "img":"assets/bking.png"},
		"bQ":{"pos":[3,7], "img":"assets/bqueen.png"}
	}

	def isalive(self, piece):
		if self.pieces.get(piece)["pos"] is None:
			return False
		else:
			return True
