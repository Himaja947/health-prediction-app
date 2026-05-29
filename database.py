import sqlite3

conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()


def insert_patient(data):
    cursor.execute("""
    INSERT INTO patients
    (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
    )
    VALUES(?,?,?,?,?,?,?)
    """, data)

    conn.commit()


def get_patients():
    return cursor.execute(
        "SELECT * FROM patients"
    ).fetchall()


def delete_patient(pid):
    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (pid,)
    )

    conn.commit()


def update_patient(data):
    cursor.execute("""
    UPDATE patients
    SET
        full_name=?,
        dob=?,
        email=?,
        glucose=?,
        haemoglobin=?,
        cholesterol=?,
        remarks=?
    WHERE id=?
    """, data)

    conn.commit()