from flask import Flask, render_template, request, redirect, url_for, session, flash
import extra.config


app = Flask(__name__)
app.config["SECRET_KEY"] = extra.config.SECRET_KEY

@app.route('/')
@app.route('/index')
def home():

	return render_template("lookupStudent.html", title = 'Student Lookup')


@app.route('/course')
def course():

	return render_template("addCourse.html", title = 'Course Admin')


@app.route('/student')
def student():

	return render_template("addStudent.html", title = 'Student Admin')


@app.route('/enrolment')
def enrol():

	return render_template("enrolStudent.html", title = 'Enrolment Admin')





if __name__ == '__main__':
    app.run(debug=True, port=5000)