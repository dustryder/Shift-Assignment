from flask import Blueprint, render_template, request
from utils.validators import validate_course
import utils.dbconfig as db
import utils.strings as string

TEMPLATE = "addCourse.html"
course_page = Blueprint('course_page', __name__, template_folder='templates')

@course_page.route('/course', methods = ['POST', 'GET'])
def add_course():
	"""Handler to add courses to the database"""

	if request.method == 'POST':

		course_code = request.form['course_code'].upper()
		course_title = request.form['course_title']
		delivery_year = request.form['delivery_year']

		#Check if given fields are of the right form
		if not validate_course(course_code, course_title, delivery_year):
			return render_template(TEMPLATE, message=string.DATA_INVALID)

		#Form a successful database connection
		connection = db.get_connection()
		cursor = db.get_cursor(connection)
		if not cursor or not connection:
			return render_template(TEMPLATE, message=string.DATABASE_CHECK)

		#Check for duplication of primary key
		result = db.execute(db.MODE_SELECT, cursor, string.COURSE_QUERY_SELECT, (course_code,))
		if result:
			return render_template(TEMPLATE, message=string.COURSE_REPEAT)

		#Insert data into database
		course_data = (course_code, course_title, delivery_year)
		result = db.execute(db.MODE_INSERT, cursor, string.COURSE_QUERY_INSERT, course_data)
		commit_success = db.commit(connection)
		db.close_connection(connection, cursor)
		if result and commit_success:
			return render_template(TEMPLATE, message=string.COURSE_SUCCESS)

		return render_template(TEMPLATE, message=string.COURSE_FAIL)	

	else:
		return render_template(TEMPLATE)