from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import database

app = FastAPI(
    title="Academic Data API",
    description="Read-only API for academic data.\n\nCAUTION: This is a teaching tool. Not production-ready.",
    version="0.1.0"
)

# CAUTION: In production, CORS should be restricted to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # CAUTION: Allows any origin. Production: specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Academic Data API",
        "caution": "This is a teaching artifact. No auth, no rate limiting, no production safeguards.",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}


@app.get("/students")
async def get_students(limit: int = 100, offset: int = 0):
    """Get all students with pagination."""
    # CAUTION: No max limit. In production, cap at 100-1000 to prevent abuse.
    students = database.get_all_students(limit=limit, offset=offset)
    return {
        "data": students,
        "count": len(students),
        "limit": limit,
        "offset": offset
    }


@app.get("/students/{student_id}")
async def get_student(student_id: int):
    """Get a single student by ID."""
    student = database.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students/search/{query}")
async def search_students(query: str):
    """Search students by name or email."""
    results = database.search_students(query)
    return {"query": query, "results": results, "count": len(results)}


@app.get("/students/major/{major}")
async def get_students_by_major(major: str):
    """Get students by major."""
    students = database.get_students_by_major(major)
    return {"major": major, "students": students, "count": len(students)}


@app.get("/registrations/today")
async def get_today_registrations():
    """Get count of today's registrations."""
    count = database.get_today_registrations()
    return {"today_registrations": count, "date": "today"}


@app.get("/courses")
async def get_courses():
    """Get all courses."""
    courses = database.get_all_courses()
    return {"courses": courses, "count": len(courses)}


@app.get("/stats/overview")
async def get_stats():
    """Get aggregate statistics."""
    stats = database.get_stats_overview()
    return stats


@app.get("/courses/{course_id}/average-grade")
async def get_course_average(course_id: int):
    """Get average grade for a course."""
    avg = database.get_average_grade_by_course(course_id)
    if avg is None:
        raise HTTPException(status_code=404, detail="No grades found for this course")
    return {"course_id": course_id, "average_grade": avg}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
