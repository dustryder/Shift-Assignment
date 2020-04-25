import mysql.connector
from extra.config import config

def get_connection():

	mydb = mysql.connector.connect(**config)
	return mydb

def close_db(connection, cursor):

	cursor.close()
	connection.close()

def get_cursor(connection):

	return connection.cursor()

def execute(cursor, query, data):

	cursor.execute(query, data)


 