from flask import Blueprint, render_template, request
import utils.dbconfig as db
import utils.strings as string

TEMPLATE = "searchStudent.html"
search_page = Blueprint('search_page', __name__, template_folder='templates')


@search_page.route('/search', methods = ['POST', 'GET'])
def search():

	if request.method == 'POST':
		
		#Are we sent an empty string?
		student_string = request.form['name']
		if not student_string:
			return render_template(TEMPLATE, message=string.DATA_INVALID)

		#Form a successful database connection
		connection = db.get_connection()
		cursor = db.get_cursor(connection)
		if not cursor or not connection:
			return render_template(TEMPLATE, message=string.DATABASE_CHECK)

		param = f"%{student_string}%"
		students = db.execute(db.MODE_SELECT, cursor, string.SEARCH_QUERY_SELECT, (param,param))
		db.close_connection(connection, cursor)

		#Given string didn't return any results
		if not students:
			return render_template(TEMPLATE, message=string.SEARCH_NONE.format(student_string))

		#Display table of results where string LIKE %first% or %last% names
		return render_template(TEMPLATE, students=students)

	else:
		return render_template(TEMPLATE)