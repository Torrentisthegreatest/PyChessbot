import sqlite3
import pickle

def connectdbcursor():
	global db, c
	db = sqlite3.connect("tables.db")
	c = db.cursor()

def checktables():
	try:
		c.execute("SELECT * FROM InitPieces")
	except:

		c.execute("""CREATE TABLE InitPieces (
			ActionTable BLOB
		)""")
		db.commit()
		initpiecetable()

def initpiecetable():
	try:
		c.execute("SELECT * FROM InitPieces")
	except sqlite3.Error as err:
		raise sqlite3.Error(err)
	else:
		pickledtable = pickle.dumps(initpieces)
		c.execute("UPDATE BotActions SET ActionTable="+pickledtable)
	finally:
		db.commit()

def getpiecetable():
	try:
		c.execute("SELECT * FROM BotActions")
	except sqlite3Error as err:
		raise sqlite3.Error(err)
	else:
		pieces = c.fetchall()
		piecetable = pickle.loads(pieces)
		return piecetable

initpieces = {
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