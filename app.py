from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ==========================
# Database Configuration
# ==========================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# Student Model
# ==========================

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    roll_no = db.Column(db.String(20), unique=True, nullable=False)

    maths = db.Column(db.Integer)

    science = db.Column(db.Integer)

    english = db.Column(db.Integer)

    attendance = db.Column(db.Float)

    percentage = db.Column(db.Float)

    grade = db.Column(db.String(10))

    performance = db.Column(db.String(30))


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("home.html")


# ==========================
# Add Student
# ==========================

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        roll_no = request.form["roll_no"]

        maths = int(request.form["maths"])
        science = int(request.form["science"])
        english = int(request.form["english"])

        attendance = float(request.form["attendance"])

        # Percentage Calculation
        percentage = (maths + science + english) / 3

        # Grade Calculation
        if percentage >= 90:
            grade = "A"
        elif percentage >= 75:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        else:
            grade = "D"

        # Performance Calculation
        if percentage >= 90 and attendance >= 90:
            performance = "Outstanding"

        elif percentage >= 80 and attendance >= 80:
            performance = "Excellent"

        elif percentage >= 70 and attendance >= 75:
            performance = "Good"

        elif percentage >= 60 and attendance >= 70:
            performance = "Average"

        else:
            performance = "Needs Improvement"

        student = Student(
            name=name,
            roll_no=roll_no,
            maths=maths,
            science=science,
            english=english,
            attendance=attendance,
            percentage=percentage,
            grade=grade,
            performance=performance
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/students")

    return render_template("add_student.html")


# ==========================
# View Students
# ==========================

@app.route("/students")
def students():

    all_students = Student.query.all()

    return render_template(
        "students.html",
        students=all_students
    )


# ==========================
# Edit Student
# ==========================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.name = request.form["name"]

        student.maths = int(request.form["maths"])
        student.science = int(request.form["science"])
        student.english = int(request.form["english"])

        student.attendance = float(
            request.form["attendance"]
        )

        # Recalculate Percentage
        student.percentage = (
            student.maths +
            student.science +
            student.english
        ) / 3

        # Recalculate Grade
        if student.percentage >= 90:
            student.grade = "A"

        elif student.percentage >= 75:
            student.grade = "B"

        elif student.percentage >= 60:
            student.grade = "C"

        else:
            student.grade = "D"

        # Recalculate Performance
        if student.percentage >= 90 and student.attendance >= 90:
            student.performance = "Outstanding"

        elif student.percentage >= 80 and student.attendance >= 80:
            student.performance = "Excellent"

        elif student.percentage >= 70 and student.attendance >= 75:
            student.performance = "Good"

        elif student.percentage >= 60 and student.attendance >= 70:
            student.performance = "Average"

        else:
            student.performance = "Needs Improvement"

        db.session.commit()

        return redirect("/students")

    return render_template(
        "edit_student.html",
        student=student
    )


# ==========================
# Delete Student
# ==========================

@app.route("/delete/<int:id>")
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return redirect("/students")


# ==========================
# Run Application
# ==========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=False)