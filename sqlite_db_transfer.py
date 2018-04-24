#!/usr/bin/env python
# -*- coding: utf-8 -*

from __future__ import print_function
import sqlite3

def transfer_db(db_from, db_to):
	'''Transfer an SQLite database from one to another.
	
	Args:
		db_from: The database from which to transfer. Can be either an sqlite
			database connection, file or ":memory:".
		db_to: The database to which to transfer. Can be either an sqlite
			database connection, file or ":memory:".
	
	Returns:
		A tuple containing the from and to database connections.
	'''
	if not isinstance(db_from, sqlite3.Connection):
		db_from = sqlite3.connect(db_from)
	if not isinstance(db_to, sqlite3.Connection):
		db_to = sqlite3.connect(db_to)
	isolation_level = db_to.isolation_level
	db_to.isolation_level = None
	cur = db_to.cursor()
	for sql in db_from.iterdump():
		cur.execute(sql);
	cur.close()
	db_to.isolation_level = isolation_level
	return db_from, db_to

def load_db(path):
	'''Load an SQLite database into memory.
	
	Args:
		path: The path to the database file to be loaded into memory.
	
	Returns:
		A connection to the in-memory database.
	'''
	f, m = transfer_db(path, ":memory:")
	f.close()
	return m

def store_db(database, path):
	'''Store an SQLite database.
	
	This is mainly used to store an in-memory database as a file. This file
	may be an existing database.
	
	Args:
		database: The (in-memory) database connection to be stored.
		path: The path to the file in which to store the database.
	
	Return:
		A connection to the file database.
	'''
	_, f = transfer_db(database, path)
	return f

if __name__ == "__main__":
	import sys
	
	help_text = '''Tranfer one SQLite database to another.

sqlite_db_transfer.py <SOURCE> <DEST>

If the destination is an existing database, the source database will be added
to it. Otherwise, the destination will be a copy of the source database.'''
	
	try:
		_, path_db_from, path_db_to = sys.argv
	except:
		print(help_text)
	else:
		db_1, db_2 = transfer_db(path_db_from, path_db_to)
		db_1.close()
		db_2.close()
