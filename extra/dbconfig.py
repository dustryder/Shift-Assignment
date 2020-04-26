import mysql.connector
from extra.config import config

MODE_INSERT = "insert"
MODE_SELECT = "select"


def get_connection():

	try:
		mydb = mysql.connector.connect(**config)
		return mydb
	except Exception as e:
		print(e)
		print("Cannot connect to database. Please check your credentials")
		return None


def close_connection(connection, cursor):

	try:
		cursor.close()
		connection.close()
		return True
	except Exception as e:
		print(e)
		print("Could not close database. Please try again")
		return False


def get_cursor(connection):

	try:
		cursor = connection.cursor()
		return cursor
	except Exception as e:
		print(e)
		print("Cannot create cursor instance to connection. Please try again")
		return None


def execute(mode, cursor, query, data=()):

	if mode == MODE_INSERT:

		try:

			if isinstance(data[0], list):
				cursor.executemany(query, data)
			else:
				cursor.execute(query, data)
			return True
		except Exception as e:
			print(e)
			print("Could not perform data insertion")
			return False

	elif mode == MODE_SELECT:

		try:
			cursor.execute(query, data)
			result = cursor.fetchall()
			return result
		except Exception as e:
			print(e)
			print("Could not perform data lookup")
			return None

	else:
		print("Could not determine correct data operation")
		return None



def commit(connection):

	try:
		connection.commit()
		return True
	except Exception as e:
		print(e)
		print("Could not commit your change. Please try again")
		return False


 