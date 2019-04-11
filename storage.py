import sqlite3
import pickle

def connectdbcursor():
	global db = sqlite3.connect("tables.db")
	global c = db.cursor()

def checktables():
	try:
		c.execute("SELECT * FROM QTables")
	except:

		CreateQTable = [] #{state: dict, qvalue: int}
		c.execute("""CREATE TABLE QTables (
			GameID int,
			QTable BLOB
		)""")
		db.commit()

	try:
		c.execute("SELECT * FROM BotActions")
	except:

		# CreateBotActions = {
		# 	p1: { actions:[], alive:True },
		# 	p2: { actions:[], alive:True },
		# 	p3: { actions:[], alive:True },
		# 	p4: { actions:[], alive:True },
		# 	p5: { actions:[], alive:True },
		# 	p6: { actions:[], alive:True },
		# 	p7: { actions:[], alive:True },
		# 	p8: { actions:[], alive:True },
		# 	k1: { actions:[], alive:True },
		# 	k2: { actions:[], alive:True },
		# 	b1: { actions:[], alive:True },
		# 	b2: { actions:[], alive:True },
		# 	r1: { actions:[], alive:True },
		# 	r2: { actions:[], alive:True },
		# 	K: { actions:[], alive:True },
		# 	Q: { actions:[], alive:True },
		# }
		c.execute("""CREATE TABLE BotActions (
			GameID int,
			ActionTable BLOB
		)""")
		db.commit()

def updateactiontable(table, gameid):
	try:
		c.execute("SELECT * FROM BotActions WHERE gameid="+gameid)
	except sqlite3.Error as err:
		raise sqlite3.Error(er)
	else:
		pickledtable = pickle.dumps(table)
		c.execute("UPDATE BotActions SET ActionTable="+pickledtable+" WHERE gameid="+gameid)
	finally:
		db.commit()

def getactiontable(gameid):
	try:
		c.execute("SELECT * FROM BotActions WHERE gameid="+gameid)
	except sqlite3Error as err:
		raise sqlite3.Error(er)
	else:
		table = c.fetchall()
		actiontable = pickle.loads(table)
		return actiontable

def updateQtable(table, gameid):
	try:
		c.execute("SELECT * FROM QTables WHERE gameid="+gameid)
	except sqlite3.Error as err:
		raise sqlite3.Error(er)
	else:
		pickledtable = pickle.dumps(table)
		c.execute("UPDATE QTables SET QTable")
	finally:
		db.commit()

def getQtable(gameid):
	try:
		c.execute("SELECT * FROM QTables WHERE gameid="+gameid)
	except sqlite.Error as err:
		raise sqlite3.Error(er)
	else:
		table = c.fetchall()
		qtable = pickle.loads(table)
		return qtable
