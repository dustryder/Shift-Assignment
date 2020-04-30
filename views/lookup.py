from flask import Blueprint, render_template, request
from utils.validators import validate_student, validate_course
import utils.dbconfig as db
import utils.strings as string

TEMPLATE = "lookupStudent.html"
COURSE_MAX = 8
lookup_page = Blueprint('lookup_page', __name__, template_folder='templates')

@lookup_page.route('/', methods = ['POST', 'GET'])
def lookup():
	"""Handler to search for students, display student enrolments and add enrolments"""

	#Form a successful database connection
	#Errors at this stage will only alert users on console
	connection = db.get_connection()
	cursor = db.get_cursor(connection)
	if not cursor or not connection:
		print(string.DATABASE_CHECK)

	#Retrieves all students in database
	result = db.execute(db.MODE_SELECT, cursor, string.LOOKUP_QUERY_SELECT_STUDENTS)
	if not result:
		print(string.LOOKUP_STUDENT_DATA_FAIL)
	students = [{"id":id, 'name':f"{fname} {lname}"} for id, fname, lname, year in result]

	#Retrieves all courses in database
	result = db.execute(db.MODE_SELECT, cursor, string.LOOKUP_QUERY_SELECT_COURSES)
	if not result:
		print(string.LOOKUP_COURSE_DATA_FAIL)
	courses = [{"code":code, "title":title, "year":year} for code, title, year in result]

	if request.method == 'POST':

		student_id = request.form.get('student_id', "")
		course_code = request.form.get('course_code', "")

		student = db.execute(db.MODE_SELECT, cursor, string.LOOKUP_QUERY_SELECT_STUDENT_BYID, (student_id,))
		#Check if given id is of sufficient length and is in database
		if not validate_student(id=student_id) or not student:
			return render_template(TEMPLATE, message=string.LOOKUP_STUDENT_VALIDATE_FAIL, students=students)

		#Check if students has max enrolments. Display courses if at max, but cannot add more
		student_courses = db.execute(db.MODE_SELECT, cursor, string.LOOKUP_QUERY_SELECT_COURSE_BYID, (student_id,))
		if len(student_courses) >= COURSE_MAX:
			return render_template(TEMPLATE, student_courses=student_courses, student=student[0], students=students)

		if course_code:

			#Check if given course is in valid form and is in database
			course = db.execute(db.MODE_SELECT, cursor, string.LOOKUP_QUERY_SELECT_COURSE_BYCODE, (course_code,))
			if not validate_course(code=course_code) or not course:
				return render_template(TEMPLATE, message=string.LOOKUP_COURSE_VALIDATE_FAIL, 
					students=students, courses=courses, student_courses=student_courses, student=student[0])

			#Check if student already has given course
			if course_code in [course[0] for course in student_courses]:
				name = f"{student[0][1]} {student[0][2]}"
				course_title = [course[1] for course in student_courses if course[0] == course_code][0]
				return render_template(TEMPLATE, message=string.LOOKUP_COURSE_REPEAT.format(name, course_title), 
					students=students, courses=courses, student_courses=student_courses, student=student[0])

			#Insert new enrolment
			result = db.execute(db.MODE_INSERT, cursor, string.LOOKUP_QUERY_INSERT_ENROLMENT, (student_id, course_code))
			commit_success = db.commit(connection)

			#Check if student has max enrolments after previous insertion
			student_courses = db.execute(db.MODE_SELECT, cursor, string.LOOKUP_QUERY_SELECT_COURSE_BYID, (student_id,))
			if len(student_courses) >= COURSE_MAX:
				return render_template(TEMPLATE, student_courses=student_courses, student=student[0], students=students)

			db.close_connection(cursor, connection)

			#Successful insertion. Display new course list and ready to add more courses
			if result and commit_success:
				return render_template(TEMPLATE, students=students, courses=courses, 
					student_courses=student_courses, student=student[0])
			
			#Failed insertion
			return render_template(TEMPLATE, message=string.LOOKUP_COURSE_ADD_FAIL, 
				students=students, courses=courses, student_courses=student_courses, student=student[0])

		else:
			#Received valid id, display courses and ready to add more courses
			return render_template(TEMPLATE, students=students, courses=courses, 
				student_courses=student_courses, student=student[0])

	else:
		#Get request, just ask for student id
		return render_template(TEMPLATE, students=students)