import mysql.connector
from extra.config import config


def get_connection():

	try:
		mydb = mysql.connector.connect(**config)
		return mydb
	except Exception as e:
		print(e)
		print("Cannot connect to database. Please check your credentials")
		return False


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
		return False


def execute(cursor, query, data):

	try:
		cursor.execute(query, data)
		if "select" in query.lower():
			result = cursor.fetchall()
			return result
		else:
			return True
	except Exception as e:
		print(e)
		print("Could not execute your query. Please try again")
		return False


def commit(connection):

	try:
		connection.commit()
		return True
	except Exception as e:
		print(e)
		print("Could not commit your change. Please try again")
		return False


 