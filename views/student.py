from flask import Blueprint, render_template, request
from extra.validators import validate_student
import extra.dbconfig as db

student_page = Blueprint('student_page', __name__, template_folder='templates')

@student_page.route('/student', methods = ['POST', 'GET'])
def student():
	"""Handler to add students to the database"""

	def render_page(message = ""):
		"""Nested function to reduce clutter and repetition"""
		return render_template("addStudent.html", message=message)

	if request.method == 'POST':

		student_firstname = request.form['first_name']
		student_lastname = request.form['last_name']
		student_id = request.form['student_id']
		start_year = request.form['start_year']

		#Server side validation
		if not validate_student(student_id, student_firstname, student_lastname, start_year):
			return render_page("Please check if the entered data is valid")

		#Form a successful database connection
		connection = db.get_connection()
		cursor = db.get_cursor(connection)
		if not cursor or not connection:
			return render_page("Please check your database connection settings")

		#Check for duplication of primary key
		query = "SELECT * FROM student WHERE student_id = %s"
		result = db.execute(db.MODE_SELECT, cursor, query, (student_id,))
		if result:
			return render_page("Sorry, that student id is already in this database. Try another")

		#Insert data into database
		query = "INSERT INTO student VALUE (%s, %s, %s, %s)"
		student_data = (student_id, student_firstname, student_lastname, start_year)
		result = db.execute(db.MODE_INSERT, cursor, query, student_data)
		commit_success = db.commit(connection)
		db.close_connection(connection, cursor)
		if result and commit_success:
			return render_page("Student successfully added")

		return render_page("Failed to add student. Try again later")	

	else:
		return render_page()