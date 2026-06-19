import sqlite3
from typing import List, Dict, Any, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "academic.db")


def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert a sqlite3.Row to a dictionary."""
    return {key: row[key] for key in row.keys()}


def get_all_students(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """Get all students with pagination."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students LIMIT ? OFFSET ?",
        (limit, offset)
    )
    results = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
    """Get a single student by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row_to_dict(row) if row else None


def get_student_count() -> int:
    """Get total number of students."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_today_registrations() -> int:
    """Get count of registrations for today."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM registrations WHERE date(registration_date) = date('now')")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_all_courses() -> List[Dict[str, Any]]:
    """Get all courses."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    results = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_stats_overview() -> Dict[str, Any]:
    """Get aggregate statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    stats = {}

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    stats["total_students"] = cursor.fetchone()[0]

    # Active students
    cursor.execute("SELECT COUNT(*) FROM students WHERE status = 'active'")
    stats["active_students"] = cursor.fetchone()[0]

    # Total courses
    cursor.execute("SELECT COUNT(*) FROM courses")
    stats["total_courses"] = cursor.fetchone()[0]

    # Total registrations
    cursor.execute("SELECT COUNT(*) FROM registrations")
    stats["total_registrations"] = cursor.fetchone()[0]

    # Today's registrations
    cursor.execute("SELECT COUNT(*) FROM registrations WHERE date(registration_date) = date('now')")
    stats["today_registrations"] = cursor.fetchone()[0]

    # Average GPA
    cursor.execute("SELECT AVG(gpa) FROM students WHERE gpa IS NOT NULL")
    stats["average_gpa"] = round(cursor.fetchone()[0], 2)

    # Students by major
    cursor.execute("SELECT major, COUNT(*) as count FROM students GROUP BY major")
    stats["students_by_major"] = [row_to_dict(row) for row in cursor.fetchall()]

    # Grade distribution
    cursor.execute("""
        SELECT letter_grade, COUNT(*) as count
        FROM grades
        GROUP BY letter_grade
        ORDER BY CASE letter_grade
            WHEN 'A' THEN 1
            WHEN 'B' THEN 2
            WHEN 'C' THEN 3
            WHEN 'D' THEN 4
            WHEN 'E' THEN 5
        END
    """)
    stats["grade_distribution"] = [row_to_dict(row) for row in cursor.fetchall()]

    conn.close()
    return stats


def search_students(query: str) -> List[Dict[str, Any]]:
    """Search students by name or email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?",
        (f"%{query}%", f"%{query}%", f"%{query}%")
    )
    results = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_students_by_major(major: str) -> List[Dict[str, Any]]:
    """Get students by major."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE major = ?", (major,))
    results = [row_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_average_grade_by_course(course_id: int) -> Optional[float]:
    """Get average grade for a specific course."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT AVG(total_score) FROM grades WHERE course_id = ?",
        (course_id,)
    )
    result = cursor.fetchone()[0]
    conn.close()
    return round(result, 2) if result else None
