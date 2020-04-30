from flask import Blueprint, render_template, request
import extra.dbconfig as db

search_page = Blueprint('search_page', __name__, template_folder='templates')

@search_page.route('/search', methods = ['POST', 'GET'])
def search():

	def render_page(message=""):

		return render_template("searchStudent.html", message=message)

	if request.method == 'POST':
		
		student_string = request.form['name']
		if not student_string:
			return render_page("Please enter a string")

		connection = db.get_connection()
		cursor = db.get_cursor(connection)
		if not cursor or not connection:
			return render_page("Please check your database connection settings")

		query = "SELECT CONCAT(first_name, ' ',last_name), start_year, student_id "\
				"FROM student WHERE first_name LIKE %s OR last_name LIKE %s"
		param = "%"+student_string+"%"

		students = db.execute(db.MODE_SELECT, cursor, query, (param,param))
		db.close_connection(connection, cursor)

		if not students:
			return render_page(f"No students could be found for the string {student_string}")

		return render_template("searchStudent.html", students=students)

	else:
		return render_page()