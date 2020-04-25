from flask import Blueprint, render_template, request
from extra.validators import validate_course
import extra.dbconfig as db

student_page = Blueprint('student_page', __name__, template_folder='templates')

@student_page.route('/student', methods = ['POST', 'GET'])

def student():

	if request.method == 'POST':
		pass
	else:
		return render_template("addStudent.html")