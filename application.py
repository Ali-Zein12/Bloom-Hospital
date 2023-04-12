import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd



# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

blood_types = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
time_slots = ["time_slot_1", "time_slot_2", "time_slot_3", "time_slot_4", "time_slot_5", "all"]

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hospital.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if 'user_id' not in session:
        # Redirect or handle the case where user is not logged in
        return redirect("/login")
    userid = session["user_id"]
    query = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(query[0]["staff"])
    if staff:
        return redirect("/staff")
    rows = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    description = rows[0]["description"]
    staff_check = bool(rows[0]["staff"])
    if staff_check:
        return redirect("/staff")
    username = rows[0]["username"]
    times_db = db.execute("SELECT * FROM blood_donations WHERE username = ?", username)
    times = len(times_db)
    query1 = db.execute("SELECT * FROM reservations WHERE patient_username = ?", username)
    return render_template("index.html", times=times, reservations=query1, description=description)

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

@app.route("/donor", methods=["GET", "POST"])
@login_required
def donor():
    userid = session["user_id"]
    query = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(query[0]["staff"])
    if staff:
        return redirect("/staff")
    if request.method == "POST":
        blood_type = request.form.get("blood_type")
        if blood_type not in blood_types:
            return render_template("error.html", message="Invalid blood type")
        rows = db.execute("SELECT * FROM blood_donations WHERE blood_type = ?", blood_type)
        if len(rows) <= 0:
            return render_template("error.html", message="No results found")
        return render_template("donored.html", rows=rows)
    else:
        return render_template("donor.html", blood_types=blood_types)

@app.route("/reserve", methods=["GET", "POST"])
@login_required
def reserve():
    userid = session["user_id"]
    query = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(query[0]["staff"])
    if staff:
        return redirect("/staff")
    if request.method == "POST":
        doctor_name = request.form.get("doctor_name")
        time_slot = request.form.get("time_slot")
        query1 = db.execute("SELECT * FROM patients WHERE name LIKE ?", doctor_name)
        doctor_username = query1[0]["username"]
        userid = session["user_id"]
        query2 = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
        patient_name = query2[0]["name"]
        patient_username = query2[0]["username"]
        query3 = db.execute("SELECT * FROM reservations WHERE patient_username = ?", patient_username)
        rows = db.execute("SELECT * FROM time_slots WHERE name LIKE ?", doctor_name)
        if len(rows) <= 0:
            return render_template("error.html", message="Invalid doctor name")
        if time_slot == "time_slot_1":
            availability = bool(rows[0]["time_slot_1"])
            if not availability:
                db.execute("UPDATE time_slots set time_slot_1 = ? WHERE name LIKE ?", True, doctor_name)

            else:
                return render_template("error.html", message="Time slot is already reserved")
        elif time_slot == "time_slot_2":
            availability = bool(rows[0]["time_slot_2"])
            if not availability:
                db.execute("UPDATE time_slots set time_slot_2 = ? WHERE name LIKE ?", True, doctor_name)
            else:
                return render_template("error.html", message="Time slot is already reserved")
        elif time_slot == "time_slot_3":
            availability = bool(rows[0]["time_slot_3"])
            if not availability:
                db.execute("UPDATE time_slots set time_slot_3 = ? WHERE name LIKE ?", True, doctor_name)
            else:
                return render_template("error.html", message="Time slot is already reserved")
        elif time_slot == "time_slot_4":
            availability = bool(rows[0]["time_slot_4"])
            if not availability:
                db.execute("UPDATE time_slots set time_slot_4 = ? WHERE name LIKE ?", True, doctor_name)
            else:
                return render_template("error.html", message="Time slot is already reserved")
        elif time_slot == "time_slot_5":
            availability = bool(rows[0]["time_slot_5"])
            if not availability:
                db.execute("UPDATE time_slots set time_slot_5 = ? WHERE name LIKE ?", True, doctor_name)
            else:
                return render_template("error.html", message="Time slot is already reserved")
        else:
            return render_template("error.html", message="Invalid time slot")
        db.execute("INSERT INTO reservations (patient_name, patient_username, doctor_name, doctor_username, time_slot) VALUES (?, ?, ?, ?, ?)",
        patient_name, patient_username, doctor_name, doctor_username, time_slot)
        return redirect("/")
    else:
        query2 = db.execute("SELECT * FROM patients WHERE staff = ?", True)
        doctor_list = []
        for doctor in query2:
            doctor_list.append(doctor.get("name"))
        return render_template("reserve.html", doctors=doctor_list)


@app.route("/donate", methods=["GET", "POST"])
@login_required
def donate():
    userid = session["user_id"]
    query = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(query[0]["staff"])
    if staff:
        return redirect("/staff")
    if request.method == "POST":
        userid = session["user_id"]
        rows = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
        name = rows[0]["name"]
        username = rows[0]["username"]
        phone = rows[0]["phone"]
        gender = rows[0]["gender"]
        blood_type = rows[0]["blood_type"]

        db.execute("INSERT INTO blood_donations (name, username, phone, gender, blood_type) VALUES (?, ?, ?, ?, ?)",
        name, username, phone, gender, blood_type)
        return redirect("/thanks")
    else:
        return render_template("donate.html", blood_types=blood_types)

@app.route("/upload" , methods=["GET", "POST"])
@login_required
def upload():
    userid = session["user_id"]
    rows = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(rows[0]["staff"])
    if not staff:
        return render_template("error.html", message="You don't have access to this page")
    if request.method == "POST":
        patient_name = request.form.get("patient_name")
        description = request.form.get("description")
        rows = db.execute("SELECT * FROM patients WHERE name = ?", patient_name)
        if len(rows) == 0:
            return render_template("staff_error.html", message="Invalid patient name")
        if not description:
            return render_template("staff_error.html", message="Description field missing")
        username = rows[0]["username"]
        db.execute("UPDATE patients SET description = ? WHERE username = ?" , description, username)
        return redirect("/staff")
    else:
        patients = db.execute("SELECT name FROM patients WHERE staff = ?", False)
        patient_list = []
        for patient in patients:
            patient_list.append(patient.get("name"))
        return render_template("upload.html", patients=patient_list)

@app.route("/free" , methods=["GET", "POST"])
def free():
    userid = session["user_id"]
    rows = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(rows[0]["staff"])
    if not staff:
        return render_template("error.html", message="You don't have access to this page")
    doctor_username = rows[0]["username"]
    if request.method == "GET":
        return render_template("free.html")
    else:
        time_slot = request.form.get("time_slot")
        if time_slot not in time_slots:
            return render_template("staff_error.html", message="invalid time slot")
        if time_slot == "all":
            db.execute("DELETE FROM reservations WHERE doctor_username = ?", doctor_username)
            db.execute("UPDATE time_slots SET time_slot_1 = ?, time_slot_2 = ?, time_slot_3 = ?, time_slot_4 = ?, time_slot_5 = ? WHERE username = ?",
            False, False, False, False, False, doctor_username)
        elif time_slot == "time_slot_1":
            db.execute("DELETE FROM reservations WHERE doctor_username = ? AND time_slot = ?", doctor_username, "time_slot_1")
            db.execute("UPDATE time_slots SET time_slot_1 = ? WHERE username = ?", False, doctor_username)
        elif time_slot == "time_slot_2":
            db.execute("DELETE FROM reservations WHERE doctor_username = ? AND time_slot = ?", doctor_username, "time_slot_2")
            db.execute("UPDATE time_slots SET time_slot_2 = ? WHERE username = ?", False, doctor_username)
        elif time_slot == "time_slot_3":
            db.execute("DELETE FROM reservations WHERE doctor_username = ? AND time_slot = ?", doctor_username, "time_slot_3")
            db.execute("UPDATE time_slots SET time_slot_3 = ? WHERE username = ?", False, doctor_username)
        elif time_slot == "time_slot_4":
            db.execute("DELETE FROM reservations WHERE doctor_username = ? AND time_slot = ?", doctor_username, "time_slot_4")
            db.execute("UPDATE time_slots SET time_slot_4 = ? WHERE username = ?", False, doctor_username)
        elif time_slot == "time_slot_5":
            db.execute("DELETE FROM reservations WHERE doctor_username = ? AND time_slot = ?", doctor_username, "time_slot_5")
            db.execute("UPDATE time_slots SET time_slot_5 = ? WHERE username = ?", False, doctor_username)
        return redirect("/staff")



@app.route("/staff")
def staff():
    userid = session["user_id"]
    rows = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    username = rows[0]["username"]
    if rows[0]["staff"]:
        query1 = db.execute("SELECT * FROM reservations WHERE doctor_username = ?", username)
        return render_template("staff_index.html", rows=query1)
    else:
        return render_template("staff_error.html", message="Only staff members can access")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
             return render_template("error.html", message="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM patients WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
             return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

        # Redirect user to home page

        if rows[0]["staff"]:
            return redirect("/staff")
        else:
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/staff_lookup", methods=["GET", "POST"])
def laklook():
    userid = session["user_id"]
    query = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(query[0]["staff"])
    if staff:
        return redirect("/staff")
    rows = db.execute("SELECT * FROM patients WHERE staff = ?", True)
    if len(rows) <= 0:
        return render_template("error.html", message="Cannot find what you are looking for")
    return render_template("lookedup.html", results=rows)

@app.route("/register", methods=["GET", "POST"])
def regsister():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_check = request.form.get("password_confirm")
        name = request.form.get("name")
        email = request.form.get("email")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        address = request.form.get("address")
        birth = request.form.get("date_of_birth")
        blood_type = request.form.get("blood_type")
        if not (username and password and password_check and name
        and gender and phone and address and birth and blood_type):
            return render_template("error.html", message="missing field(s)")
        if password != password_check:
            return render_template("error.html", message="passwords do not match")
        if blood_type == "Blood type":
            return render_template("error.html", message="Please choose a blood type")
        check_db = db.execute("SELECT * FROM patients WHERE username = ?", username)
        if(len(check_db) > 0):
            return render_template("error.html", message="username already chosen")
        if blood_type not in blood_types:
            return render_template("error.html", message="Invalid blood type")
        hashed = generate_password_hash(password)
        db.execute("INSERT INTO patients (username, password, staff, name, DOB, gender, phone, email, address, blood_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
        username, hashed, False, name, birth, gender, phone, email, address, blood_type)
        return redirect("/login")
    else:
        return render_template("register.html", blood_types=blood_types)


@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    userid = session["user_id"]
    query = db.execute("SELECT * FROM patients WHERE ID = ?", userid)
    staff = bool(query[0]["staff"])
    if staff:
        return redirect("/staff")
    if request.method == "POST":
        name = request.form.get("name")
        rows = db.execute("SELECT * FROM time_slots WHERE name LIKE ?", name)
        if len(rows) <= 0:
            return render_template("error.html", message="Cannot find what you are looking for")
        else:
            return render_template("lookedup2.html", results=rows)
    else:
        query2 = db.execute("SELECT * FROM patients WHERE staff = ?", True)
        doctor_list = []
        for doctor in query2:
            doctor_list.append(doctor.get("name"))
        return render_template("lookup.html", doctors=doctor_list)



@app.route("/secret", methods=["GET", "POST"])
def secret():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_check = request.form.get("password_confirm")
        name = request.form.get("name")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")
        birth = request.form.get("date_of_birth")
        specialization = request.form.get("specialization")
        staff = True
        blood_type = request.form.get("blood_type")
        if not (username and password and password_check and name
        and gender and phone and address and birth and specialization and blood_type):
            return render_template("error.html", message="missing field(s)")
        if password != password_check:
            return render_template("error.html", message="passwords do not match")
        check_db = db.execute("SELECT * FROM patients WHERE username = ?", username)
        if(len(check_db) > 0):
            return render_template("error.html", message="username already chosen")
        if blood_type not in blood_types:
            return render_template("error.html", message="Invalid blood type")
        hashed = generate_password_hash(password)
        db.execute("INSERT INTO patients (username, password, name, DOB, gender, phone, email, address, staff, specialization, blood_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
        username, hashed, name, birth, gender, phone, email, address, staff, specialization, blood_type)
        db.execute("INSERT INTO time_slots (name, username, time_slot_1, time_slot_2, time_slot_3, time_slot_4, time_slot_5) VALUES (?, ?, ?, ?, ?, ?, ?)",  name, username, False, False, False, False, False)
        return redirect("/login")
    else:
        # Forget any user_id
        session.clear()
        return render_template("staff_register.html", blood_types=blood_types)



