import configparser, storage, game, qbot

def SetConfig():
	config = configparser.ConfigParser()
	configdata = config.read('config.ini')

	piecevalues = configdata["PIECEVALUES"]["PAWN"]
	print(piecevalues)

storage.connectdbcursor()
storage.checktables()

Game = game.Game(SetConfig.configdata)