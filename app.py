from flask import Flask, render_template, request, redirect, url_for, session, flash
import extra.config
from extra.dbconfig import get_connection, close_db, get_cursor, execute


app = Flask(__name__)
app.config["SECRET_KEY"] = extra.config.SECRET_KEY

@app.route('/', methods = ['POST', 'GET'])
def home():

	if request.method == 'POST':
		pass
	else:
		return render_template("lookupStudent.html", title = 'Student Lookup')


@app.route('/course', methods = ['POST', 'GET'])
def add_course():

	if request.method == 'POST':
		course_code = request.form['course_code']
		course_title = request.form['course_title']
		delivery_year = request.form['delivery_year']

		connection = get_connection()
		cursor = get_cursor(connection)

		query = "INSERT INTO course VALUE (%s, %s, %s)"
		course_data = (course_code, course_title, delivery_year)

		execute(cursor, query, course_data)
		connection.commit()
		close_db(connection, cursor)
		return redirect(request.url)
	else:
		return render_template("addCourse.html", title = 'Course Admin')


@app.route('/student', methods = ['POST', 'GET'])
def student():

	if request.method == 'POST':
		pass
	else:
		return render_template("addStudent.html", title = 'Student Admin')


@app.route('/enrolment', methods = ['POST', 'GET'])
def enrol():

	if request.method == 'POST':
		pass
	else:
		return render_template("enrolStudent.html", title = 'Enrolment Admin')





if __name__ == '__main__':
    app.run(debug=True, port=5000)