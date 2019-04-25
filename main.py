import configparser, game, storage

def SetConfig():
	config = configparser.ConfigParser()
	config.read('config.ini')

	return config

storage.connectdbcursor()
storage.checktables()

Game = game.Game(SetConfig())

def restart():
	Game.GameOn = False
	Game = game.Game(SetConfig())
