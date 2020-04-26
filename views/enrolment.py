from flask import Blueprint, render_template, request
from extra.validators import validate_course
import extra.dbconfig as db

enrolment_page = Blueprint('enrolment_page', __name__, template_folder='templates')

@enrolment_page.route('/enrolment', methods = ['POST', 'GET'])
def enrolment():

	if request.method == 'POST':
		pass
	else:
		return render_template("enrolStudent.html")