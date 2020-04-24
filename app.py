from flask import Flask, render_template, request, redirect, url_for, session, flash
import extra.config


app = Flask(__name__)
app.config["SECRET_KEY"] = extra.config.SECRET_KEY

@app.route('/', methods = ['POST', 'GET'])
def home():

	if request.method == 'POST':
		pass
	else:
		return render_template("lookupStudent.html", title = 'Student Lookup')


@app.route('/course', methods = ['POST', 'GET'])
def course():

	if request.method == 'POST':
		pass
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