"""utilities.py contains functions used in the creation, formating and insertion of data used in this 
web application"""


import requests
import re
from random import randint, choice
from bs4 import BeautifulSoup
from dbconfig import get_connection, get_cursor, close_connection


URL = "https://www.canterbury.ac.nz/courseinfo/GetCourses.aspx?coursecodeprefixes=COSC%7CSENG%7CENCE"
MIN_COURSE = 0
MAX_COURSE = 8
STUDENT_DATA = "studentData.csv"
COURSE_DATA = "courseData.csv"
ENROLMENT_DATA = "enrolmentData.csv"

def course_scrape(url):

	"""Pulls course codes and course titles from the UCs website"""

	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	seen = []

	course_codes = soup.find_all(id=re.compile("CourseDefinitionCodeLabel"))
	course_titles = soup.find_all(id=re.compile("CourseDefinitionTitleLabel"))

	with open(COURSE_DATA, "w+") as file:
		
		for code, title in zip(course_codes, course_titles):

			code = code.text.strip()
			title = title.text.strip()

			if code not in seen:
				seen.append(code)
				year = "2020" if title != "Special Topic" else str(randint(2012,2019))

				string = f"{code},{title},{year}\n"
				file.write(string)

#course_scrape(URL)

def generate_enrolments(student_file, course_file):

	"""Generates student-course pairs as enrolments from student and course csv datafiles"""

	enrolments = []

	with open(course_file, "r") as file:
		data = file.read().replace('\n', ',').split(',')
		course_codes = data[::3]

	with open(student_file, "r") as file:
		data = file.read().replace('\n', ',').split(',')
		student_ids = data[0::4]

	for id in student_ids:

		for _ in range(randint(MIN_COURSE, MAX_COURSE)):

			course_choice = choice(course_codes)
			pair = [id, course_choice]
			if pair not in enrolments:
				enrolments.append(pair)

	with open(ENROLMENT_DATA, "w+") as file:

		for student_id, course_code in enrolments:

			string = f"{student_id},{course_code}\n"
			file.write(string)

#generate_enrolments(STUDENT_DATA, COURSE_DATA)

def insert_into_db(datafile, table_name):

	"""Inserts data into the corresponding table name"""

	connection = get_connection()
	cursor = get_cursor(connection)

	with open(datafile, "r") as file:

		data = []
		for i in file.readlines():
			data.append(i.strip().split(','))


		column_count = len(data[0])
		parameters = ','.join(['%s' for x in range(column_count)])
		query_string = f"INSERT INTO {table_name} VALUES ({parameters})"

		cursor.executemany(query_string, data)
		connection.commit()
		close_connection(connection, cursor)


#insert_into_db(STUDENT_DATA, "student")
#insert_into_db(COURSE_DATA, "course")
#insert_into_db(ENROLMENT_DATA, "enrolment")









