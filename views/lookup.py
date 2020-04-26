from flask import Blueprint, render_template, request
from extra.validators import validate_course
import extra.dbconfig as db

lookup_page = Blueprint('lookup_page', __name__, template_folder='templates')

@lookup_page.route('/', methods = ['POST', 'GET'])
def lookup():

	if request.method == 'POST':
		pass
	else:
		return render_template("lookupStudent.html")