"""TODO: Handle cases where dropdown is the same
"""



from flask import Blueprint, render_template, request
from extra.validators import validate_student, validate_course
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
	query = "SELECT student_id, first_name, last_name, start_year FROM student"
	result = db.execute(db.MODE_SELECT, cursor, query)
	if not result:
		print("Could not retrieve student data")
	students = [{"id":id, 'name':f"{fname} {lname}"} for id, fname, lname, year in result]

	#Retrieves all courses in database
	query = "SELECT course_code, course_title, delivery_year FROM course"
	result = db.execute(db.MODE_SELECT, cursor, query)
	if not result:
		print("Could not retrieve course data")
	courses = [{"code":code, "title":title, "year":year} for code, title, year in result]

	def render_page(message="", student_courses=[], student=[]):
		"""Nested function to reduce clutter and repetition"""
		return render_template("lookupStudent.html", message=message, students=students, student_courses=student_courses, student=student, courses=courses)


	if request.method == 'POST':

		student_id = request.form.get('student_id', "")
		course_code = request.form.get('course_code', "")

		#Will always return false if a course is not selected from dropdown
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
		student_courses = db.execute(db.MODE_SELECT, cursor, query, (student_id,))

		#Check for max courses. Does not render course form if hit max
		if len(student_courses) >= 8:
			return render_template("lookupStudent.html", student_courses=student_courses, student=student[0], students=students)

		if course_code:

			#Will always return false if a course is not selected from dropdown
			if not validate_course(code=course_code):
				return render_page(message="Sorry, that course could not be found", student_courses=student_courses, student=student[0])

			#Check for course duplication
			if course_code in [course[0] for course in student_courses]:
				first_name = student[0][1]
				last_name = student[0][2]
				course_title = [course[1] for course in student_courses if course[0] == course_code][0]
				return render_page(message=f"{first_name} {last_name} is already enrolled for {course_title}", student_courses=student_courses, student=student[0])

			#Insert course
			query = "INSERT INTO enrolment VALUE (%s, %s)"
			result = db.execute(db.MODE_INSERT, cursor, query, (student_id, course_code))
			commit_success = db.commit(connection)

			#Check for new max courses. Does not render course form if hit max
			query = "SELECT course.course_code, course_title, delivery_year "\
				"FROM student "\
				"JOIN enrolment ON student.student_id = enrolment.student_id "\
				"JOIN course ON course.course_code = enrolment.course_code "\
				"WHERE student.student_id = %s"
			student_courses = db.execute(db.MODE_SELECT, cursor, query, (student_id,))
			if len(student_courses) >= 8:
				return render_template("lookupStudent.html", student_courses=student_courses, student=student[0], students=students)

			db.close_connection(cursor, connection)

			if result and commit_success:
				return render_page(student_courses=student_courses, student=student[0])
			
			return render_page(message="Could not add course. Try again later", student_courses=student_courses, student=student[0])

		else:
			return render_page(student_courses=student_courses, student=student[0])

	else:
		return render_page()