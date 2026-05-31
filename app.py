import sqlite3

from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "some_random_string"


def get_db():
    conn = sqlite3.connect("student_class.db")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Class_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            school_class TEXT,
            maths INTEGER,
            english INTEGER,
            chemistry INTEGER,
            marks TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    name = request.form.get("name")
    clas = request.form.get("class")
    maths = int(request.form.get("maths"))
    english = int(request.form.get("english"))
    chemistry = int(request.form.get("chemistry"))

    if maths > 75 and english > 75 and chemistry > 75:
        total_marks = "Total marks are 75"
    else:
        total_marks = str(maths + english + chemistry)
        session["name"] = name
        session["clas"] = clas
        session["maths"] = maths
        session["english"] = english
        session["chemistry"] = chemistry
        session["total_marks"] = total_marks

    return render_template(
        "result.html",
        name=name,
        class_1=clas,
        Toatal_number=total_marks,
    )


@app.route("/history", methods=["POST"])
def history_analyze():
    student_name = session.get("name")
    student_class = session.get("clas")
    maths_1 = session.get("maths")
    english_1 = session.get("english")
    chemistry_1 = session.get("chemistry")
    final_marks = session.get("total_marks")

    conn = get_db()
    cursor = conn.cursor()

    sql_commands = "INSERT INTO Class_table (name,school_class,maths,english,chemistry,marks) VALUES (?,?,?,?,?,?)"
    values = (student_name, student_class, maths_1, english_1, chemistry_1, final_marks)

    cursor.execute(sql_commands, values)
    conn.commit()

    cursor.execute("SELECT * FROM Class_table")
    records = cursor.fetchall()
    conn.close()

    return render_template("history.html", record=records)


@app.route("/delete", methods=["POST"])
def delete_history():
    delete_message = request.form.get("which_to_delete")

    conn = get_db()
    cursor = conn.cursor()

    sql = "DELETE FROM Class_table where id = ?"
    cursor.execute(sql, (delete_message,))
    conn.commit()

    cursor.execute("SELECT * FROM Class_table")
    new_record = cursor.fetchall()
    conn.close()

    return render_template("delete.html", record=new_record)


@app.route("/share_data", methods=["GET"])
def share_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Class_table")
    records = cursor.fetchall()
    conn.close()

    all_students = []
    for row in records:
        all_students.append({"NAME": row[1], "CLASS": row[2], "TOTAL_MARKS": row[6]})

        return jsonify(all_students)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
