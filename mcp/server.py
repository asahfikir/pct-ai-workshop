from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import requests
import sys
import os

# Add parent directory to path so we can import database
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))
import database

app = FastAPI(
    title="Academic MCP Server",
    description="Simple HTTP-based MCP server for academic data.\n\nCAUTION: This is a teaching implementation. Production would use the official MCP SDK with stdio/SSE transport.",
    version="0.1.0"
)

# CAUTION: In production, CORS should be restricted
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # CAUTION: Allows any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# The API that this MCP server wraps
API_BASE_URL = "http://localhost:8000"


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}


# Define the tools that this MCP server exposes
TOOLS = [
    {
        "name": "get_student_count",
        "description": "Get the total number of students in the database",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_today_registrations",
        "description": "Get the number of student registrations for today",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_stats_overview",
        "description": "Get aggregate statistics about the academic data including total students, courses, average GPA, and grade distribution",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "search_students",
        "description": "Search for students by name or email",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for student name or email"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_students_by_major",
        "description": "Get all students in a specific major/department",
        "parameters": {
            "type": "object",
            "properties": {
                "major": {
                    "type": "string",
                    "description": "The major/department name (e.g., 'Teknik Informatika', 'Manajemen')"
                }
            },
            "required": ["major"]
        }
    },
    {
        "name": "get_courses",
        "description": "Get the list of all available courses",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


@app.get("/")
async def root():
    return {
        "name": "Academic MCP Server",
        "version": "0.1.0",
        "caution": "HTTP-based MCP for teaching. Production: use official MCP SDK.",
        "endpoints": {
            "tools_list": "GET /tools/list",
            "tools_call": "POST /tools/call"
        }
    }


@app.get("/tools/list")
async def list_tools():
    """List all available tools."""
    return {"tools": TOOLS}


@app.post("/tools/call")
async def call_tool(tool_call: ToolCall):
    """Execute a tool and return the result."""

    # CAUTION: No input validation beyond Pydantic. Production: strict schema validation.
    # CAUTION: No rate limiting. Production: implement per-user rate limits.
    # CAUTION: No authentication. Production: verify API keys/JWT.

    try:
        if tool_call.name == "get_student_count":
            count = database.get_student_count()
            return {
                "content": [{"type": "text", "text": f"There are {count} students in the database."}],
                "data": {"count": count}
            }

        elif tool_call.name == "get_today_registrations":
            count = database.get_today_registrations()
            return {
                "content": [{"type": "text", "text": f"There are {count} registrations today."}],
                "data": {"today_registrations": count}
            }

        elif tool_call.name == "get_stats_overview":
            stats = database.get_stats_overview()
            summary = (
                f"Academic Statistics:\n"
                f"- Total Students: {stats['total_students']}\n"
                f"- Active Students: {stats['active_students']}\n"
                f"- Total Courses: {stats['total_courses']}\n"
                f"- Total Registrations: {stats['total_registrations']}\n"
                f"- Today's Registrations: {stats['today_registrations']}\n"
                f"- Average GPA: {stats['average_gpa']}\n"
            )
            return {
                "content": [{"type": "text", "text": summary}],
                "data": stats
            }

        elif tool_call.name == "search_students":
            query = tool_call.arguments.get("query", "")
            if not query:
                raise HTTPException(status_code=400, detail="Query parameter is required")
            results = database.search_students(query)
            if not results:
                return {
                    "content": [{"type": "text", "text": f"No students found matching '{query}'."}],
                    "data": {"query": query, "results": []}
                }
            summary = f"Found {len(results)} student(s) matching '{query}':\n"
            for s in results[:5]:  # Limit to 5 for readability
                summary += f"- {s['first_name']} {s['last_name']} ({s['email']}), {s['major']}, GPA: {s['gpa']}\n"
            if len(results) > 5:
                summary += f"... and {len(results) - 5} more."
            return {
                "content": [{"type": "text", "text": summary}],
                "data": {"query": query, "results": results}
            }

        elif tool_call.name == "get_students_by_major":
            major = tool_call.arguments.get("major", "")
            if not major:
                raise HTTPException(status_code=400, detail="Major parameter is required")
            students = database.get_students_by_major(major)
            if not students:
                return {
                    "content": [{"type": "text", "text": f"No students found in {major}."}],
                    "data": {"major": major, "students": []}
                }
            summary = f"Found {len(students)} student(s) in {major}:\n"
            for s in students[:5]:
                summary += f"- {s['first_name']} {s['last_name']}, GPA: {s['gpa']}, Status: {s['status']}\n"
            if len(students) > 5:
                summary += f"... and {len(students) - 5} more."
            return {
                "content": [{"type": "text", "text": summary}],
                "data": {"major": major, "students": students}
            }

        elif tool_call.name == "get_courses":
            courses = database.get_all_courses()
            summary = f"There are {len(courses)} courses available:\n"
            for c in courses[:10]:
                summary += f"- {c['course_code']}: {c['name']} ({c['credits']} credits, Semester {c['semester']})\n"
            if len(courses) > 10:
                summary += f"... and {len(courses) - 10} more."
            return {
                "content": [{"type": "text", "text": summary}],
                "data": {"courses": courses}
            }

        else:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_call.name}' not found")

    except HTTPException:
        raise
    except Exception as e:
        # CAUTION: In production, don't expose internal error details to clients
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
