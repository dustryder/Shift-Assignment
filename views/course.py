from flask import Blueprint, render_template, request
from extra.validators import validate_course
import extra.dbconfig as db

course_page = Blueprint('course_page', __name__, template_folder='templates')

@course_page.route('/course', methods = ['POST', 'GET'])
def add_course():
	"""Handler to add courses to the database"""

	def render_page(message = ""):
		"""Nested function to reduce clutter and repetition"""
		return render_template("addCourse.html", message = message)

	if request.method == 'POST':

		course_code = request.form['course_code']
		course_title = request.form['course_title']
		delivery_year = request.form['delivery_year']

		#Server side validation
		if not validate_course(course_code, course_title, delivery_year):
			return render_page("Please check if the entered data is valid")

		#Form a successful database connection
		connection = db.get_connection()
		cursor = db.get_cursor(connection)
		if not cursor or not connection:
			return render_page("Please check your database connection settings")

		#Check for duplication of primary key
		query = "SELECT * FROM course WHERE course_code = %s"
		result = db.execute(db.MODE_SELECT, cursor, query, (course_code,))
		if result:
			return render_page("Sorry, that course code is already in this database. Try another")

		#Insert data into database
		query = "INSERT INTO course VALUE (%s, %s, %s)"
		course_data = (course_code, course_title, delivery_year)
		result = db.execute(db.MODE_INSERT, cursor, query, course_data)
		commit_success = db.commit(connection)
		db.close_connection(connection, cursor)
		if result and commit_success:
			return render_page("Course successfully added")

		return render_page("Failed to add course. Try again later")	

	else:
		return render_page()