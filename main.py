import configparser, storage, game, qbot, os

def SetConfig():
	config = configparser.ConfigParser()
	configdata = config.read('config.ini')

	piecevalues = configdata[0]
	print(piecevalues)
	return configdata

storage.connectdbcursor()
storage.checktables()

Game = game.Game(SetConfig())