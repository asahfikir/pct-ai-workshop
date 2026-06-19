#!/usr/bin/env python3
"""
Mock Academic Database Generator
================================
Creates a realistic SQLite database for the workshop.

CAUTION: This is a teaching tool. Real production databases would:
- Use MySQL/PostgreSQL with proper indexing
- Have foreign key constraints enforced
- Include audit trails and soft deletes
- Be normalized to 3NF (this is intentionally simplified)

"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "academic.db"

# Indonesian academic context
FIRST_NAMES = [
    "Ahmad", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hadi",
    "Indah", "Joko", "Kartika", "Lestari", "Mulyadi", "Nadia", "Putra",
    "Rina", "Sari", "Teguh", "Umar", "Vina", "Wahyu", "Yanti", "Zainal",
    "Adi", "Bayu", "Cici", "Dian", "Eka", "Fira", "Guntur", "Hana"
]

LAST_NAMES = [
    "Santoso", "Wijaya", "Kusuma", "Pratama", "Sari", "Nugroho",
    "Hidayat", "Susanto", "Putri", "Rahmawati", "Saputra", "Lestari",
    "Wahyudi", "Purnama", "Handoko", "Siregar", "Mulyani", "Tanjung",
    "Iskandar", "Mahendra", "Suryadi", "Kuswanto", "Ramadhan", "Febrianto"
]

MAJORS = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Elektro",
    "Manajemen",
    "Akuntansi",
    "Hukum",
    "Psikologi",
    "Kedokteran",
    "Farmasi",
    "Ilmu Komunikasi"
]

COURSE_NAMES = [
    ("Algoritma dan Pemrograman", "TI"),
    ("Basis Data", "TI"),
    ("Jaringan Komputer", "TI"),
    ("Pemrograman Web", "TI"),
    ("Sistem Operasi", "TI"),
    ("Kalkulus I", "MT"),
    ("Fisika Dasar", "MT"),
    ("Kimia Dasar", "MT"),
    ("Biologi Umum", "MT"),
    ("Pengantar Akuntansi", "AK"),
    ("Ekonomi Mikro", "MN"),
    ("Manajemen Pemasaran", "MN"),
    ("Hukum Bisnis", "HK"),
    ("Psikologi Kognitif", "PS"),
    ("Farmakologi", "FR"),
    ("Anatomi", "KD"),
    ("Komunikasi Massa", "IK"),
    ("Statistika", "MT"),
    ("Etika Profesi", "UM"),
    ("Bahasa Inggris Akademik", "UM"),
]


def create_database():
    """Create the SQLite database with schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.executescript("""
        DROP TABLE IF EXISTS registrations;
        DROP TABLE IF EXISTS grades;
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS courses;
    """)

    # Students table
    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            major TEXT NOT NULL,
            enrollment_year INTEGER NOT NULL,
            gpa REAL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Courses table
    cursor.execute("""
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            credits INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            enrolled INTEGER DEFAULT 0
        )
    """)

    # Registrations table (student-course enrollment)
    cursor.execute("""
        CREATE TABLE registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            registration_date DATE NOT NULL,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    # Grades table
    cursor.execute("""
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            assignment_score REAL,
            midterm_score REAL,
            final_score REAL,
            total_score REAL,
            letter_grade TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    conn.commit()
    return conn


def generate_students(conn, count=200):
    """Generate realistic student records."""
    cursor = conn.cursor()
    current_year = datetime.now().year

    for i in range(count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        major = random.choice(MAJORS)
        year = random.randint(current_year - 4, current_year)
        student_id = f"{year}{str(i+1).zfill(4)}"
        email = f"{first.lower()}.{last.lower()}{i}@student.ac.id"
        gpa = round(random.uniform(2.0, 3.9), 2)
        status = random.choices(
            ['active', 'active', 'active', 'graduated', 'on_leave'],
            weights=[70, 10, 10, 5, 5]
        )[0]

        cursor.execute("""
            INSERT INTO students (student_id, first_name, last_name, email, major, enrollment_year, gpa, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, first, last, email, major, year, gpa, status))

    conn.commit()
    print(f"Generated {count} students")


def generate_courses(conn):
    """Generate course records."""
    cursor = conn.cursor()

    for i, (name, dept) in enumerate(COURSE_NAMES):
        course_code = f"{dept}{100 + i}"
        credits = random.choice([2, 3, 4])
        semester = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
        capacity = random.choice([30, 40, 50, 60])

        cursor.execute("""
            INSERT INTO courses (course_code, name, department, credits, semester, capacity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (course_code, name, dept, credits, semester, capacity))

    conn.commit()
    print(f"Generated {len(COURSE_NAMES)} courses")


def generate_registrations(conn):
    """Generate student course registrations."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE status = 'active'")
    student_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM courses")
    course_ids = [row[0] for row in cursor.fetchall()]

    today = datetime.now().date()
    registration_count = 0

    for student_id in student_ids:
        # Each active student takes 3-6 courses
        num_courses = random.randint(3, 6)
        selected_courses = random.sample(course_ids, min(num_courses, len(course_ids)))

        for course_id in selected_courses:
            # Registration date within last 30 days or upcoming semester
            days_offset = random.randint(-30, 7)
            reg_date = today + timedelta(days=days_offset)

            status = 'active' if days_offset <= 0 else 'pending'

            cursor.execute("""
                INSERT INTO registrations (student_id, course_id, registration_date, status)
                VALUES (?, ?, ?, ?)
            """, (student_id, course_id, reg_date, status))
            registration_count += 1

    conn.commit()
    print(f"Generated {registration_count} registrations")


def generate_grades(conn):
    """Generate grade records for completed courses."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, enrollment_year FROM students WHERE status IN ('active', 'graduated')")
    students = cursor.fetchall()

    cursor.execute("SELECT id FROM courses")
    courses = [row[0] for row in cursor.fetchall()]

    current_year = datetime.now().year
    grade_count = 0

    for student_id, enroll_year in students:
        # Generate grades for past semesters
        years_enrolled = current_year - enroll_year + 1
        semesters_completed = min(years_enrolled * 2, 8)

        for semester in range(1, semesters_completed + 1):
            # 4-6 courses per semester
            num_courses = random.randint(4, 6)
            selected_courses = random.sample(courses, min(num_courses, len(courses)))

            for course_id in selected_courses:
                assignment = round(random.uniform(60, 95), 1)
                midterm = round(random.uniform(50, 95), 1)
                final = round(random.uniform(55, 95), 1)
                total = round((assignment * 0.3) + (midterm * 0.3) + (final * 0.4), 1)

                if total >= 85:
                    letter = 'A'
                elif total >= 75:
                    letter = 'B'
                elif total >= 60:
                    letter = 'C'
                elif total >= 50:
                    letter = 'D'
                else:
                    letter = 'E'

                academic_year = f"{enroll_year + (semester - 1) // 2}-{enroll_year + (semester - 1) // 2 + 1}"

                cursor.execute("""
                    INSERT INTO grades (student_id, course_id, semester, academic_year, assignment_score, midterm_score, final_score, total_score, letter_grade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (student_id, course_id, semester, academic_year, assignment, midterm, final, total, letter))
                grade_count += 1

    conn.commit()
    print(f"Generated {grade_count} grade records")


def verify_database(conn):
    """Print summary statistics."""
    cursor = conn.cursor()

    print("\n" + "="*50)
    print("DATABASE SUMMARY")
    print("="*50)

    cursor.execute("SELECT COUNT(*) FROM students")
    print(f"Students: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM courses")
    print(f"Courses: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM registrations")
    print(f"Registrations: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM grades")
    print(f"Grades: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM registrations WHERE registration_date = DATE('now')")
    print(f"Today's registrations: {cursor.fetchone()[0]}")

    cursor.execute("SELECT major, COUNT(*) FROM students GROUP BY major")
    print("\nStudents by major:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")

    print("="*50)


if __name__ == "__main__":
    print("Creating mock academic database...")
    conn = create_database()
    generate_students(conn, count=200)
    generate_courses(conn)
    generate_registrations(conn)
    generate_grades(conn)
    verify_database(conn)
    conn.close()
    print(f"\nDatabase created: {DB_PATH}")
