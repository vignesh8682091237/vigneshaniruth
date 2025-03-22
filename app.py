from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
from datetime import datetime
from sqlalchemy import text


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)

class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), db.ForeignKey('student.reg_no'), nullable=False)
    subject_code = db.Column(db.String(20), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    internal = db.Column(db.Integer, nullable=False)
    external = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), db.ForeignKey('student.reg_no'), nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    days_present = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)

class Fees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.String(20), db.ForeignKey('student.reg_no'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    fee_id = db.Column(db.String(50), nullable=False)
    payment_mode = db.Column(db.String(20), nullable=False)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100), nullable=False)
    reg_no = db.Column(db.String(100), nullable=False)
    emis_no = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    bloodgroup = db.Column(db.String(5), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    caste = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    parent_mobile_no = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    day_hostel = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    current_joining = db.Column(db.String(50), nullable=False)
    batch_start_year = db.Column(db.Integer, nullable=False)
    batch_end_year = db.Column(db.Integer, nullable=False)
    scholarship = db.Column(db.String(3), nullable=False)
    profile_image = db.Column(db.String(255))

# Initialize the database
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('login.html')
#-------------------------stat login function-----------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if email == 'admin@gmail.com' and password == '123':
        session['user'] = 'admin'
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session['user'] = user.username
        return redirect(url_for('user_dashboard'))
    
    return "Invalid credentials! Try again."
#-----------------------start register function-------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        
        new_user = User(username=username, email=email, password=password, mobile=mobile)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('register.html')
#--------------------------start admin dashboard----------------------------------------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session and session['user'] == 'admin':
        return render_template('admin_dashboard.html')
    return redirect(url_for('home'))
#--------------------------start check department details--------------------------------------------
@app.route('/admin/check_department_details')
def check_department_details():
    if 'user' in session and session['user'] == 'admin':
        departments = db.session.query(Student.department).distinct().all()
        return render_template('check_student_details.html', departments=departments)  # Pass the departments to the template
    return redirect(url_for('home'))

#--------------------------start add_student---------------------------------------------------------

@app.route('/admin/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            print("Received POST request to add student")  # Debugging
            
            # Extract form data
            first_name = request.form['first_name']
            middle_name = request.form.get('middle_name', '')
            last_name = request.form['last_name']
            reg_no = request.form['reg_no']
            emis_no = request.form['emis_no']
            mobile_no = request.form['mobile_no']
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
            bloodgroup = request.form['bloodgroup']
            religion = request.form['religion']
            caste = request.form['caste']
            address = request.form['address']
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            parent_mobile_no = request.form['parent_mobile_no']
            department = request.form['department']
            year = request.form['year']
            day_hostel = request.form['day_hostel']
            gender = request.form['gender']
            current_joining = request.form['current_joining']
            batch_start_year = request.form['batch_start_year']
            batch_end_year = request.form['batch_end_year']
            scholarship = request.form['scholarship']

            # Handle profile image upload
            profile_image = None
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file.filename:
                    filename = f"{int(time.time())}_{secure_filename(file.filename)}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    profile_image = filename
            
            # Create new student record
            new_student = Student(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                reg_no=reg_no,
                emis_no=emis_no,
                mobile_no=mobile_no,
                dob=dob,
                bloodgroup=bloodgroup,
                religion=religion,
                caste=caste,
                address=address,
                father_name=father_name,
                mother_name=mother_name,
                parent_mobile_no=parent_mobile_no,
                department=department,
                year=year,
                day_hostel=day_hostel,
                gender=gender,
                current_joining=current_joining,
                batch_start_year=batch_start_year,
                batch_end_year=batch_end_year,
                scholarship=scholarship,
                profile_image=profile_image
            )

            db.session.add(new_student)
            db.session.commit()
            print("Student added successfully!")  # Debugging
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        
        except Exception as e:
            db.session.rollback()
            print(f"Error saving student: {e}")  # Debugging
            return f"Error: {e}"

    return render_template('add_student.html')

#--------------------------start add_student_academic_details-----------------------------------------
@app.route('/admin/student_academic_details', methods=['GET', 'POST'])
def student_academic_details():
    if 'user' in session and session['user'] == 'admin':
        student_data = None
        if request.method == 'POST':
            reg_no = request.form.get('reg_no')
            if reg_no:
                student_data = db.session.execute(
                    text("SELECT * FROM student WHERE reg_no = :reg_no"), {"reg_no": reg_no}
                ).fetchone()

        return render_template('student_academic_details.html', student=student_data)

    return redirect(url_for('home'))


#--------------------------start user dashboard----------------------------------------------------
@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session:
        return render_template('user_dashboard.html', user=session['user'])
    return redirect(url_for('home'))


#------------------------star view_student function------------------------------------------------------
@app.route('/view_students', methods=['GET', 'POST'])
def view_students():
    if request.method == 'POST':
        department = request.form.get('department', '').strip()
        year = request.form.get('year', '').strip()
    else:  # Handle GET requests
        department = request.args.get('department', '').strip()
        year = request.args.get('year', '').strip()

    # Ensure department and year are provided
    if department and year:
        students = Student.query.filter_by(department=department, year=year).all()
    else:
        students = []  # No filter applied

    return render_template('view_students.html', students=students, department=department, year=year)
#------------------------end view_student function------------------------------------------------------
@app.route('/student_details')
def student_details():
    reg_no = request.args.get('reg_no')
    student = Student.query.filter_by(reg_no=reg_no).first()
    marks = Marks.query.filter_by(reg_no=reg_no).all()
    attendance = Attendance.query.filter_by(reg_no=reg_no).first()
    fees = Fees.query.filter_by(reg_no=reg_no).all()

    return render_template("student_details.html", student=student, marks=marks, attendance=attendance, fees=fees)

#------------------------star logout function------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
#--------------------end main function----------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
