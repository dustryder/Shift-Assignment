import re

def validate_course(code, title, year):

	try:
		code_valid = re.match("^[a-zA-Z]{4}[0-9]{3}$", code)
		title_valid = len(title) <= 100 and len(title) >= 1
		year_valid = int(year) <= 2050 and int(year) >= 1950

		if code_valid and title_valid and year_valid:
			return True
	except Exception as e:
		print(e)
		print("Error in validation")
		return False
	return False

