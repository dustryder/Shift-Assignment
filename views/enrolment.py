from flask import Blueprint, render_template, request
from extra.validators import validate_course, validate_student
import extra.dbconfig as db

enrolment_page = Blueprint('enrolment_page', __name__, template_folder='templates')

@enrolment_page.route('/enrolment', methods = ['POST', 'GET'])
def enrolment():

	#Form a successful database connection
	#Errors at this stage will only alert users on console
	connection = db.get_connection()
	cursor = db.get_cursor(connection)
	if not cursor or not connection:
		print("Could not connection")

	#Retrieves all students in database
	query = "SELECT student_id, first_name, last_name FROM student"
	result = db.execute(db.MODE_SELECT, cursor, query)
	if not result:
		print("Could not retrieve student data")
	students = [{"id":id, 'name':f"{fname} {lname}"} for id, fname, lname in result]

	query = "SELECT course_code, course_title, delivery_year FROM course"
	result = db.execute(db.MODE_SELECT, cursor, query)
	if not result:
		print("Could not retrieve course data")
	courses = [{"code":code, "title":title, "year":year} for code, title, year in result]

	def render_page(message=""):
		"""Nested function to reduce clutter and repetition"""
		return render_template("enrolStudent.html", message=message, students=students, courses=courses)



	if request.method == 'POST':

		student_id = request.form['student_id']
		course_code = request.form['course_code']

		#Server side validation
		if not validate_student(id=student_id):
			return render_page("Sorry, that student id is not valid")

		if not validate_course(code=course_code):
			return render_page("Sorry, that course is not valid")

		query = "SELECT first_name, last_name FROM student WHERE student_id = %s"
		student = db.execute(db.MODE_SELECT, cursor, query, (student_id,))
		if not student:
			return render_page("Sorry, that student does not exist")

		query = "SELECT course_title FROM course WHERE course_code = %s"
		course = db.execute(db.MODE_SELECT, cursor, query, (course_code,))
		if not course:
			return render_page("Sorry, that course does not exist")


		query = "SELECT course_code FROM enrolment WHERE student_id = %s"
		student_courses = db.execute(db.MODE_SELECT, cursor, query, (student_id,))
		if len(student_courses) >= 8:
			return render_page(f"{student[0][0]} {student[0][1]} is already enrolled in the maximum of eight courses. ")

		if (course_code,) in student_courses:
			return render_page(f"{student[0][0]} {student[0][1]} is already enrolled for {course[0][0]}")
			
		query = "INSERT INTO enrolment VALUE (%s, %s)"
		result = db.execute(db.MODE_INSERT, cursor, query, (student_id, course_code))
		commit_success = db.commit(connection)
		db.close_connection(cursor, connection)
		if result and commit_success:
			return render_page(f'{student[0][0]} {student[0][1]} has been enrolled for {course[0][0]}')

		return render_page("Failed to register course. Try again later")

	else:
		return render_page()