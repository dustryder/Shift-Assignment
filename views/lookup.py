from flask import Blueprint, render_template, request
from extra.validators import validate_student
import extra.dbconfig as db

lookup_page = Blueprint('lookup_page', __name__, template_folder='templates')

@lookup_page.route('/', methods = ['POST', 'GET'])
def lookup():

	#Form a successful database connection
	#Errors at this stage will only alert users on console
	connection = db.get_connection()
	cursor = db.get_cursor(connection)
	if not cursor or not connection:
		print("Could not form connection")

	#Retrieves all students in database
	query = "SELECT student_id, first_name, last_name FROM student"
	result = db.execute(db.MODE_SELECT, cursor, query)
	if not result:
		print("Could not retrieve student data")

	students = [{"id":id, 'name':f"{fname} {lname}"} for id, fname, lname in result]

	def render_page(message=""):
		"""Nested function to reduce clutter and repetition"""
		return render_template("lookupStudent.html", message=message, students=students)


	if request.method == 'POST':

		student_id = request.form['student_id']

		#Server side validation
		if not validate_student(id=student_id):
			return render_page("Sorry, that student could not be found")

		#Retrieve a specific student's data by student id
		query = "SELECT * FROM student WHERE student.student_id = %s"
		student = db.execute(db.MODE_SELECT, cursor, query, (student_id,))
		if not student:
			return render_page(f"Could not retrieve data for id {student_id}")

		#Retrieve a student's courses by student id
		query = "SELECT course.course_code, course_title, delivery_year "\
				"FROM student "\
				"JOIN enrolment ON student.student_id = enrolment.student_id "\
				"JOIN course ON course.course_code = enrolment.course_code "\
				"WHERE student.student_id = %s"
		courses = db.execute(db.MODE_SELECT, cursor, query, (student_id,))
		if not courses:
			return render_page(f"No courses could be found for {student[0][1]} {student[0][2]}")

		db.close_connection(connection, cursor)
		
		return render_template("lookupStudent.html", courses=courses, student=student[0], students=students)

	else:
		return render_page()