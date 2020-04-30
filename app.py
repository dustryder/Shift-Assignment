from flask import Flask
from views import course, student, lookup, search
import utils.config


app = Flask(__name__)
app.config["SECRET_KEY"] = utils.config.SECRET_KEY

app.register_blueprint(course.course_page)
app.register_blueprint(student.student_page)
app.register_blueprint(lookup.lookup_page)
app.register_blueprint(search.search_page)

if __name__ == '__main__':
    app.run(debug=True, port=5000)