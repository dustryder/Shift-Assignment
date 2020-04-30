#Data strings
DATABASE_CHECK = "Please check your database connection settings"
DATA_INVALID = "Please check that you've entered valid data"

#search.py strings
SEARCH_NONE = "No students could be found for the string {}"

SEARCH_QUERY_SELECT = "SELECT CONCAT(first_name, ' ',last_name), start_year, student_id "\
				       "FROM student WHERE first_name LIKE %s OR last_name LIKE %s"

#student.py strings
STUDENT_REPEAT = "Sorry, that student id is already in this database. Try another"
STUDENT_SUCCESS = "Student successfully added"
STUDENT_FAIL = "Failed to add student. Try again later"

STUDENT_QUERY_SELECT = "SELECT * FROM student WHERE student_id = %s"
STUDENT_QUERY_INSERT = "INSERT INTO student VALUE (%s, %s, %s, %s)"

#course.py strings
COURSE_REPEAT = "Sorry, that course is already in this database. Try another"
COURSE_SUCCESS = "Course successfully added"
COURSE_FAIL = "Failed to add course. Try again later"

COURSE_QUERY_SELECT = "SELECT * FROM course WHERE course_code = %s"
COURSE_QUERY_INSERT = "INSERT INTO course VALUE (%s, %s, %s)"

#lookup.py strings
LOOKUP_STUDENT_DATA_FAIL = "Could not retrieve student data"
LOOKUP_COURSE_DATA_FAIL = "Could not retrieve course data"
LOOKUP_STUDENT_VALIDATE_FAIL = "Sorry, that student could not be found"
LOOKUP_COURSE_VALIDATE_FAIL = "Sorry, that course could not be found"
LOOKUP_COURSE_REPEAT = "{} is already enrolled for {}"
LOOKUP_COURSE_ADD_FAIL = "Could not add course. Try again later"

LOOKUP_QUERY_SELECT_STUDENTS = "SELECT student_id, first_name, last_name, start_year FROM student"
LOOKUP_QUERY_SELECT_COURSES = "SELECT course_code, course_title, delivery_year FROM course"
LOOKUP_QUERY_SELECT_STUDENT_BYID = "SELECT * FROM student WHERE student.student_id = %s"
LOOKUP_QUERY_SELECT_COURSE_BYID	= "SELECT course.course_code, course_title, delivery_year "\
								  "FROM student "\
								  "JOIN enrolment ON student.student_id = enrolment.student_id "\
								  "JOIN course ON course.course_code = enrolment.course_code "\
								  "WHERE student.student_id = %s"
LOOKUP_QUERY_SELECT_COURSE_BYCODE = "SELECT * FROM course WHERE course_code = %s"
LOOKUP_QUERY_INSERT_ENROLMENT = "INSERT INTO enrolment VALUE (%s, %s)"