CREATE DATABASE IF NOT EXISTS enrolments;
USE enrolments;

CREATE TABLE IF NOT EXISTS course (
	course_code CHAR(7) PRIMARY KEY,
    course_title VARCHAR(100),
    delivery_year INT
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS student (
	student_id INT PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    start_date INT
) engine = InnoDB;

CREATE TABLE IF NOT EXISTS enrolment (
	student_id INT,
    course_code CHAR(7),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_code) REFERENCES course(course_code),
    PRIMARY KEY (student_id, course_code)
) engine = InnoDB;