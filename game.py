import pygame
from pygame.locals import *
import storage
import time


class Game:
	columnvalues = [61, 114, 167, 220, 273, 326, 379, 432]  # x-coords for the board's columns
	rowvalues = [432, 379, 326, 273, 220, 167, 114, 63]  # y-coords for the board's rows
	whitescore = 0
	blackscore = 0
	showactions = False
	turnowner = "w"
	pieceactshowed = ""
	score = {"w": 0, "b": 0}
	texttoshow = {"W Score: ": True, "B Score: ": True}
	#teamincheck = None  # "w" or "b"

	def addscore(self, team, ptaken):
		if str(ptaken)[1:2] == "K":
			self.WinCond(self.turnowner)
			from main import restart
			restart()
		self.score[str(team)] += int(self.pvalues[str(ptaken[1:2])])

	def text_display(self, text, xpos, ypos, size):
		largeText = pygame.font.Font('freesansbold.ttf', size)
		TextSurf, TextRect = self.text_objects(text, largeText)
		TextRect.center = (xpos, ypos)
		self.screen.blit(TextSurf, TextRect)

	def text_objects(self, text, font):
		textSurface = font.render(text, True, (0, 255, 0))
		return textSurface, textSurface.get_rect()

	def __init__(self, configdata):
		self.GameOn = True
		self.config = configdata
		self.pvalues = self.config["PIECEVALUES"]
		self.screensize = self.width, self.height = 500, 500
		pygame.init()
		self.screen = pygame.display.set_mode(self.screensize)
		pygame.display.set_caption('PyChess')
		self.pieces = {
			"wp1": {"pos": [0, 1], "img": "assets/wpawn.png"},
			"wp2": {"pos": [1, 1], "img": "assets/wpawn.png"},
			"wp3": {"pos": [2, 1], "img": "assets/wpawn.png"},
			"wp4": {"pos": [3, 1], "img": "assets/wpawn.png"},
			"wp5": {"pos": [4, 1], "img": "assets/wpawn.png"},
			"wp6": {"pos": [5, 1], "img": "assets/wpawn.png"},
			"wp7": {"pos": [6, 1], "img": "assets/wpawn.png"},
			"wp8": {"pos": [7, 1], "img": "assets/wpawn.png"},
			"wb1": {"pos": [2, 0], "img": "assets/wbishop.png"},
			"wb2": {"pos": [5, 0], "img": "assets/wbishop.png"},
			"wk1": {"pos": [1, 0], "img": "assets/wknight.png"},
			"wr1": {"pos": [0, 0], "img": "assets/wrook.png"},
			"wk2": {"pos": [6, 0], "img": "assets/wknight.png"},
			"wr2": {"pos": [7, 0], "img": "assets/wrook.png"},
			"wK_": {"pos": [4, 0], "img": "assets/wking.png"},
			"wQ_": {"pos": [3, 0], "img": "assets/wqueen.png"},

			"bp1": {"pos": [0, 6], "img": "assets/bpawn.png"},
			"bp2": {"pos": [1, 6], "img": "assets/bpawn.png"},
			"bp3": {"pos": [2, 6], "img": "assets/bpawn.png"},
			"bp4": {"pos": [3, 6], "img": "assets/bpawn.png"},
			"bp5": {"pos": [4, 6], "img": "assets/bpawn.png"},
			"bp6": {"pos": [5, 6], "img": "assets/bpawn.png"},
			"bp7": {"pos": [6, 6], "img": "assets/bpawn.png"},
			"bp8": {"pos": [7, 6], "img": "assets/bpawn.png"},
			"bb1": {"pos": [2, 7], "img": "assets/bbishop.png"},
			"bb2": {"pos": [5, 7], "img": "assets/bbishop.png"},
			"bk1": {"pos": [1, 7], "img": "assets/bknight.png"},
			"bk2": {"pos": [6, 7], "img": "assets/bknight.png"},
			"br1": {"pos": [0, 7], "img": "assets/brook.png"},
			"br2": {"pos": [7, 7], "img": "assets/brook.png"},
			"bK_": {"pos": [4, 7], "img": "assets/bking.png"},
			"bQ_": {"pos": [3, 7], "img": "assets/bqueen.png"}
		}
		self.background = pygame.image.load("assets/chessboard.jpg")
		self.background = pygame.transform.scale(self.background, self.screensize)

		while self.GameOn:
			self.screen.blit(self.background, (0, 0))
			self.loadpieceimg()
			for event in (event for event in pygame.event.get() if event.type == MOUSEBUTTONDOWN and event.button == 1):
				pos = x, y = pygame.mouse.get_pos()
				for piece in self.pieces:
					if self.teaminturn(piece) and self.pieces.get(piece)["obj_rect"].collidepoint(pos) and \
							self.pieces.get(piece)["pos"] is not None:
						if self.teamincheck != self.turnowner:
							self.toshow = self.showmoves(piece)
						break
				if self.showactions:
					for action in filter(lambda action: self.toshow[action]["obj_rect"].collidepoint(pos), range(len(self.toshow))):
						if self.toshow[action]["obj_rect"].collidepoint(pos):
							newcoord = [self.toshow[action]["coord"][0], self.toshow[action]["coord"][1]]
							if self.toshow[action]["kill"]:
								for piece in self.pieces:
									if self.pieces.get(piece)["pos"] == newcoord:
										self.pieces.get(piece)["pos"] = None
										self.addscore(self.turnowner, piece)
										break
							self.pieces.get(self.pieceactshowed)["pos"] = newcoord
							self.switchteams()
							self.showactions = False
							break
			if self.showactions:
				for i in range(len(self.toshow)):
					x, y = self.toshow[i]["pos"]
					self.screen.blit(self.toshow[i]["obj"], (x + 3, y + 2))
			for txt in filter(lambda txt: self.texttoshow[txt] is True, self.texttoshow):
				if txt[:1] == "W":
					self.text_display((txt + str(self.score["w"])), 60, 20, 20)
				elif txt[:1] == "B":
					self.text_display((txt + str(self.score["b"])), 420, 20, 20)
			pygame.display.flip()

	def WinCond(self, winner):
		teamname = {"w": "White", "b": "Black"}
		t_end = time.time() + 10
		while time.time() < t_end:
			self.text_display((teamname[winner] + " Team Won!"), 250, 250, 50)
			pygame.display.flip()


	def switchteams(self):
		if self.turnowner == "w":
			self.turnowner = "b"
		elif self.turnowner == "b":
			self.turnowner = "w"

	def getposxy(self, col, row):  # returns tuple
		if col < 0 or row < 0:
			return None, None
		try:
			x = self.columnvalues[int(col)]
			y = self.rowvalues[int(row)]
		except IndexError:
			x, y = None, None
		finally:
			return (x, y)

	def showmoves(self, piece):  # returns showacts which is set to self.toshow
		showacts = []
		actions = self.availableactions(piece)  # actions = [{pos:(x,y),kill:True/False}]
		for actdict in actions:
			act = actions.index(actdict)
			if actions[act]["kill"]:
				actions[act]["obj"] = pygame.image.load("assets/killspace.png").convert_alpha()
			else:
				actions[act]["obj"] = pygame.image.load("assets/avalspace.png").convert_alpha()
			actions[act]["obj"] = pygame.transform.scale(actions[act]["obj"], (52, 52))
			actions[act]["obj_rect"] = actions[act]["obj"].get_rect()
			try:
				actions[act]["obj_rect"].centerx, actions[act]["obj_rect"].centery = self.getposxy(
					actions[act]["pos"][0], actions[act]["pos"][1])
				showacts.append({
					                "obj": actions[act]["obj"],
					                "pos": (actions[act]["obj_rect"].x, actions[act]["obj_rect"].y),
					                "coord": actions[act]["pos"], "obj_rect": actions[act]["obj_rect"],
					                "kill": actions[act]["kill"]
				                })
			except TypeError:
				pass  # if pawn @ far end set pawn to other piece
		if len(showacts) > 0:
			self.showactions = True
		return showacts

	def availableactions(self, piece):
		type = str(piece)
		if type[1:2] == "p":
			badj = 1
			if type[:1] == "b":
				badj = -1
			actions = []
			fwdactpos = [[self.pieces.get(piece)["pos"][0], self.pieces.get(piece)["pos"][1] + (1 * badj)]]
			if (self.pieces.get(piece)["pos"][1] == 1 and str(piece)[:1] == "w") or (
					self.pieces.get(piece)["pos"][1] == 6 and str(piece)[:1] == "b"):  # Is pawn in init location
				fwdactpos.append([self.pieces.get(piece)["pos"][0], self.pieces.get(piece)["pos"][1] + (2 * badj)])
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in fwdactpos:
					if self.pieces.get(piece)["pos"][1] + (1 * badj) == self.pieces.get(targetP)["pos"]:
						fwdactpos = []
						break
					else:
						fwdactpos.pop(fwdactpos.index(self.pieces.get(targetP)["pos"]))
						break
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in fwdactpos:
					if self.pieces.get(piece)["pos"][1] + (1 * badj) == self.pieces.get(targetP)["pos"]:
						fwdactpos.clear()
					else:
						fwdactpos.pop(fwdactpos.index(self.pieces.get(targetP)["pos"]))
					break
			for actpos in fwdactpos:
				actions.append({"pos": (actpos[0], actpos[1]), "kill": False})
			diagactpos = [
				[self.pieces.get(piece)["pos"][0] - 1, self.pieces.get(piece)["pos"][1] + (1 * badj)],
				[self.pieces.get(piece)["pos"][0] + 1, self.pieces.get(piece)["pos"][1] + (1 * badj)]
			]
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in diagactpos and str(targetP)[:1] == self.turnowner:
					diagactpos.pop(diagactpos.index(self.pieces.get(targetP)["pos"]))
			for targetP in self.pieces:
				if self.pieces.get(targetP)["pos"] in diagactpos and str(targetP)[:1] != self.turnowner:
					actions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
			self.pieceactshowed = str(piece)
			return actions
		elif type[1:2] == "b":
			actions = []
			diagactpospp = []
			diagactposnp = []
			diagactpospn = []
			diagactposnn = []
			strtx, strty = self.pieces.get(piece)["pos"]
			x = strtx
			y = strty
			while self.getposxy(x + 1, y + 1)[0] is not None and self.getposxy(x + 1, y + 1)[1] is not None:
				diagactpospp.append([x + 1, y + 1])
				x += 1
				y += 1
			x = strtx
			y = strty
			while self.getposxy(x - 1, y + 1)[0] is not None and self.getposxy(x - 1, y + 1)[1] is not None:
				diagactposnp.append([x - 1, y + 1])
				x -= 1
				y += 1
			x = strtx
			y = strty
			while self.getposxy(x - 1, y - 1)[0] is not None and self.getposxy(x - 1, y - 1)[1] is not None:
				diagactposnn.append([x - 1, y - 1])
				x -= 1
				y -= 1
			x = strtx
			y = strty
			while self.getposxy(x + 1, y - 1)[0] is not None and self.getposxy(x + 1, y - 1)[1] is not None:
				diagactpospn.append([x + 1, y - 1])
				x += 1
				y -= 1
			diagactpos = [diagactpospp, diagactposnp, diagactposnn, diagactpospn]
			for dactpos in diagactpos:
				for actpos in range(len(dactpos)):
					try:
						for targetP in filter(lambda targetP: self.pieces.get(targetP)["pos"] == dactpos[actpos],
						                      self.pieces):
							if str(targetP)[:1] == self.turnowner:
								for i in range(actpos, len(dactpos)):
									diagactpos[diagactpos.index(dactpos)].pop(actpos)
							elif str(targetP)[:1] != self.turnowner:
								actions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
								for i in range(actpos + 1, len(dactpos)):
									diagactpos[diagactpos.index(dactpos)].pop(actpos + 1)
					except IndexError:
						break
					try:
						actions.append({"pos": dactpos[actpos], "kill": False})
					except IndexError:
						pass
			self.pieceactshowed = str(piece)
			for kills in filter(lambda kills: actions[kills]["kill"] == True, range(len(actions))):
				for i in (i for i in range(len(actions)) if actions[i]["pos"] == actions[kills]["pos"] and i != kills):
					actions.pop(i)
					break
				break
			return actions
		elif type[1:2] == "k":
			actions = []
			strtx, strty = self.pieces.get(piece)["pos"]
			actpos = [
				[strtx + 1, strty + 2], [strtx - 1, strty + 2],
				[strtx + 1, strty - 2], [strtx - 1, strty - 2],
				[strtx + 2, strty + 1], [strtx + 2, strty - 1],
				[strtx - 2, strty + 1], [strtx - 2, strty - 1],
			]
			try:
				for targetP in filter(lambda targetP: self.pieces.get(targetP)["pos"] in actpos, self.pieces):
					if str(targetP)[:1] == self.turnowner:
						actpos.pop(actpos.index(self.pieces.get(targetP)["pos"]))
					elif str(targetP)[:1] != self.turnowner:
						actions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
						actpos.pop(actpos.index(self.pieces.get(targetP)["pos"]))
			except IndexError:
				pass
			for finpos in actpos:
				actions.append({"pos": finpos, "kill": False})
			self.pieceactshowed = str(piece)
			return actions
		elif type[1:2] == "r":
			strtx, strty = self.pieces.get(piece)["pos"]
			actions = []
			upactpos = []
			x = strtx
			y = strty
			while self.getposxy(x, y + 1)[1] is not None:
				upactpos.append([x, y + 1])
				y += 1
			y = strty
			dwnactpos = []
			while self.getposxy(x, y - 1)[1] is not None:
				dwnactpos.append([x, y - 1])
				y -= 1
			y = strty
			rgtactpos = []
			while self.getposxy(x + 1, y)[1] is not None:
				rgtactpos.append([x + 1, y])
				x += 1
			x = strtx
			lftactpos = []
			while self.getposxy(x - 1, y)[1] is not None:
				lftactpos.append([x - 1, y])
				x -= 1
			actpos = [upactpos, dwnactpos, rgtactpos, lftactpos]
			for actdirect in actpos:
				for a in range(len(actdirect)):
					try:
						for targetP in filter(
								lambda targetP: self.pieces.get(targetP)["pos"] == actpos[actpos.index(actdirect)][a],
								self.pieces):
							if str(targetP)[:1] == self.turnowner:
								for i in range(a, len(actpos[actpos.index(actdirect)]) + 1):
									actpos[actpos.index(actdirect)].pop(a)
							elif str(targetP)[:1] != self.turnowner:
								actions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
								for i in range(a, len(actpos[actpos.index(actdirect)]) + 1):
									actpos[actpos.index(actdirect)].pop(a)
					except IndexError:
						pass
				try:
					for finpos in range(len(actpos[actpos.index(actdirect)])):
						actions.append({"pos": actpos[actpos.index(actdirect)][finpos], "kill": False})
				except IndexError:
					pass
			self.pieceactshowed = str(piece)
			return actions
		elif type[1:2] == "K":
			strtx, strty = self.pieces.get(piece)["pos"]
			actions = []
			remact = []
			actpos = [
				[strtx + 1, strty + 1], [strtx + 1, strty - 1],
				[strtx - 1, strty + 1], [strtx - 1, strty - 1],
				[strtx + 1, strty], [strtx - 1, strty],
				[strtx, strty + 1], [strtx, strty - 1]
			]
			for a in actpos:
				if self.getposxy(a[0], a[1])[0] is None or self.getposxy(a[0], a[1])[1] is None:
					actpos.pop(actpos.index(a))
			for a in range(len(actpos)):
				act = actpos[a]
				for targetP in self.pieces:
					if self.pieces.get(targetP)["pos"] == act:
						if str(targetP)[:1] == self.turnowner:
							remact.append(actpos[a])
						elif str(targetP)[:1] != self.turnowner:
							actions.append({"pos": actpos[a], "kill": True})
							remact.append(actpos[a])
			for rem in remact:
				actpos.pop(actpos.index(rem))
			for a in range(len(actpos)):
				actions.append({"pos": actpos[a], "kill": False})
			self.pieceactshowed = str(piece)
			return actions
		elif type[1:2] == "Q":
			strtx, strty = self.pieces.get(piece)["pos"]
			sidesactions = []
			actions = []
			upactpos = []
			x = strtx
			y = strty
			while self.getposxy(x, y + 1)[1] is not None:
				upactpos.append([x, y + 1])
				y += 1
			y = strty
			dwnactpos = []
			while self.getposxy(x, y - 1)[1] is not None:
				dwnactpos.append([x, y - 1])
				y -= 1
			y = strty
			rgtactpos = []
			while self.getposxy(x + 1, y)[1] is not None:
				rgtactpos.append([x + 1, y])
				x += 1
			x = strtx
			lftactpos = []
			while self.getposxy(x - 1, y)[1] is not None:
				lftactpos.append([x - 1, y])
				x -= 1
			actpos = [upactpos, dwnactpos, rgtactpos, lftactpos]
			for actdirect in actpos:
				for a in range(len(actdirect)):
					try:
						for targetP in filter(
								lambda targetP: self.pieces.get(targetP)["pos"] == actpos[actpos.index(actdirect)][a],
								self.pieces):
							if str(targetP)[:1] == self.turnowner:
								for i in range(a, len(actpos[actpos.index(actdirect)]) + 1):
									actpos[actpos.index(actdirect)].pop(a)
							elif str(targetP)[:1] != self.turnowner:
								sidesactions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
								for i in range(a, len(actpos[actpos.index(actdirect)]) + 1):
									actpos[actpos.index(actdirect)].pop(a)
					except IndexError:
						pass
				try:
					for finpos in range(len(actpos[actpos.index(actdirect)])):
						sidesactions.append({"pos": actpos[actpos.index(actdirect)][finpos], "kill": False})
				except IndexError:
					pass
			actions = []
			diagactpospp = []
			diagactposnp = []
			diagactpospn = []
			diagactposnn = []
			strtx, strty = self.pieces.get(piece)["pos"]
			x = strtx
			y = strty
			while self.getposxy(x + 1, y + 1)[0] is not None and self.getposxy(x + 1, y + 1)[1] is not None:
				diagactpospp.append([x + 1, y + 1])
				x += 1
				y += 1
			x = strtx
			y = strty
			while self.getposxy(x - 1, y + 1)[0] is not None and self.getposxy(x - 1, y + 1)[1] is not None:
				diagactposnp.append([x - 1, y + 1])
				x -= 1
				y += 1
			x = strtx
			y = strty
			while self.getposxy(x - 1, y - 1)[0] is not None and self.getposxy(x - 1, y - 1)[1] is not None:
				diagactposnn.append([x - 1, y - 1])
				x -= 1
				y -= 1
			x = strtx
			y = strty
			while self.getposxy(x + 1, y - 1)[0] is not None and self.getposxy(x + 1, y - 1)[1] is not None:
				diagactpospn.append([x + 1, y - 1])
				x += 1
				y -= 1
			diagactpos = [diagactpospp, diagactposnp, diagactposnn, diagactpospn]
			for dactpos in diagactpos:
				for actpos in range(len(dactpos)):
					try:
						for targetP in filter(lambda targetP: self.pieces.get(targetP)["pos"] == dactpos[actpos],
						                      self.pieces):
							if str(targetP)[:1] == self.turnowner:
								for i in range(actpos, len(dactpos)):
									diagactpos[diagactpos.index(dactpos)].pop(actpos)
							elif str(targetP)[:1] != self.turnowner:
								actions.append({"pos": self.pieces.get(targetP)["pos"], "kill": True})
								for i in range(actpos + 1, len(dactpos)):
									diagactpos[diagactpos.index(dactpos)].pop(actpos + 1)
					except IndexError:
						break
					try:
						actions.append({"pos": dactpos[actpos], "kill": False})
					except IndexError:
						pass
			for kills in filter(lambda kills: actions[kills]["kill"] == True, range(len(actions))):
				for i in (i for i in range(len(actions)) if actions[i]["pos"] == actions[kills]["pos"] and i != kills):
					actions.pop(i)
					break
				break
			actions = actions + sidesactions
			self.pieceactshowed = str(piece)
			return actions
		else:
			raise Exception("Available Actions: ", "Invalid piece type")

	def teaminturn(self, piece):
		if str(piece)[:1] == self.turnowner:
			return True
		else:
			return False

	def loadpieceimg(self):

		# Starting with White Pieces that are alive
		for piece in self.pieces:
			if self.isalive(piece):
				sqcord = self.pieces.get(piece)["pos"]
				coords = self.getposxy(sqcord[0], sqcord[1])
				self.pieces.get(piece)["obj"] = pygame.image.load(self.pieces.get(piece)["img"]).convert_alpha()
				self.pieces.get(piece)["obj_rect"] = self.pieces.get(piece)["obj"].get_rect()
				self.pieces.get(piece)["obj_rect"].centerx = coords[0]
				self.pieces.get(piece)["obj_rect"].centery = coords[1]
				rectx, recty = self.pieces.get(piece)["obj_rect"].x, self.pieces.get(piece)["obj_rect"].y
				self.screen.blit(self.pieces.get(piece)["obj"], (rectx, recty))

	def isalive(self, piece):
		if self.pieces.get(piece)["pos"] is None:
			return False
		else:
			return True
