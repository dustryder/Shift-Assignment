from flask import Blueprint, render_template, request
from utils.validators import validate_student
import utils.dbconfig as db
import utils.strings as string

TEMPLATE = "addStudent.html"
student_page = Blueprint('student_page', __name__, template_folder='templates')

@student_page.route('/student', methods = ['POST', 'GET'])
def student():
	"""Handler to add students to the database"""

	if request.method == 'POST':

		student_firstname = request.form['first_name']
		student_lastname = request.form['last_name']
		student_id = request.form['student_id']
		start_year = request.form['start_year']

		#Check if given values are of valid form
		if not validate_student(student_id, student_firstname, student_lastname, start_year):
			return render_template(TEMPLATE, message=string.DATA_INVALID)

		#Form a successful database connection
		connection = db.get_connection()
		cursor = db.get_cursor(connection)
		if not cursor or not connection:
			return render_template(TEMPLATE, message=string.DATABASE_CHECK)

		#Check for duplication of primary key
		result = db.execute(db.MODE_SELECT, cursor, string.STUDENT_QUERY_SELECT, (student_id,))
		if result:
			return render_template(TEMPLATE, message=string.STUDENT_REPEAT)

		#Insert data into database
		student_data = (student_id, student_firstname, student_lastname, start_year)
		result = db.execute(db.MODE_INSERT, cursor, string.STUDENT_QUERY_INSERT, student_data)
		commit_success = db.commit(connection)
		db.close_connection(connection, cursor)
		if result and commit_success:
			return render_template(TEMPLATE, message=string.STUDENT_SUCCESS)

		return render_template(TEMPLATE, message=string.STUDENT_FAIL)	

	else:
		return render_template(TEMPLATE)