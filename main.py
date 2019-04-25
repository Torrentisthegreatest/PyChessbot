import configparser, storage, game, os

def SetConfig():
	config = configparser.ConfigParser()
	config.read('config.ini')

	return config

storage.connectdbcursor()
storage.checktables()

Game = game.Game(SetConfig())

def restart():
	Game.GameOn = False
	Game = None
	Game = game.Game(SetConfig())
