import re

YEAR_MAX = 2050
YEAR_MIN = 1950
STUDENTID_MAX = 999999999
STUDENTID_MIN = 100000000
STRING_MAX = 100
STRING_MIN = 1


def validate_course(code, title, year):


	try:
		code_valid = re.match("^[a-zA-Z]{4}[0-9]{3}$", code)
		title_valid = len(title) <= STRING_MAX and len(title) >= STRING_MIN
		year_valid = int(year) <= YEAR_MAX and int(year) >= YEAR_MIN

		if code_valid and title_valid and year_valid:
			return True
	except Exception as e:
		print(e)
		print("Error in validation")

	return False
	

def validate_student(first, last, id, year):


	try:
		first_valid = len(first) <= STRING_MAX and len(first) >= STRING_MIN
		last_valid = len(last) <= STRING_MAX and len(last) >= STRING_MIN
		id_valid = int(id) <= STUDENTID_MAX and int(id) >= STUDENTID_MIN
		year_valid = int(year) <= YEAR_MAX and int(year) >= YEAR_MIN

		if first_valid and last_valid and id_valid and year_valid:
			return True

	except Exception as e:
		print(e)
		print("Error in validation")

	return False

