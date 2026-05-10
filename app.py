from flask import Flask, render_template,request,session
import mysql.connector

app = Flask(__name__)
app.secret_key = "some_random_string"

properties = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = properties.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Class")
cursor.execute("USE Class")

# THIS LINE IS THE MAGIC - It deletes the broken table for you
cursor.execute("DROP TABLE IF EXISTS Class_table")

# This recreates it PERFECTLY with all 7 columns
cursor.execute("""
    CREATE TABLE Class_table(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(200),
        class VARCHAR(200),
        maths INT,
        english INT,
        chemistry INT,
        marks VARCHAR(200)
    )
""")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    name = request.form.get('name')
    clas = request.form.get("class")
    maths = int(request.form.get("maths"))
    english = int(request.form.get("english"))
    chemistry = int(request.form.get("chemistry"))
    if maths and english and chemistry > 75:
        total_marks = "Total marks are 75"
    else:
        total_marks = (int(maths)) + (int(english)) + (int(chemistry))
        session["name"] = name
        session["clas"] = clas
        session["maths"] = maths
        session["english"] = english
        session["chemistry"] = chemistry
        session["total_marks"] = total_marks

    return render_template("result.html",
                           name = name,
                           class_1 = clas,
                           Toatal_number = total_marks,)

@app.route("/history", methods=["POST"])
def history_analyze():
        student_name = session.get('name')
        student_class = session.get('clas')
        maths_1 = session.get('maths')
        english_1 = session.get('english')
        chemistry_1 = session.get('chemistry')
        final_marks = session.get('total_marks')
        student_info = (student_name,student_class, maths_1, english_1, chemistry_1, final_marks)
        sql_command = "INSERT INTO Class_table (name, class, maths, english, chemistry, marks) VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql_command,student_info)
        properties.commit()
        cursor.execute("SELECT * FROM Class_table")
        record = cursor.fetchall()
        return render_template("history.html",
                               record = record)


                                    
if __name__ == '__main__':
    app.run(debug=True)
