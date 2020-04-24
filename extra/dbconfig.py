import mysql.connector
import config

def get_connection():

	mydb = mysql.connector.connect(**config.config)
	return mydb

def close_db(connection, cursor):

	cursor.close()
	connection.close()

def get_cursor(connection):

	return connection.cursor()
 