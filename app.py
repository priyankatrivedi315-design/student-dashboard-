from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ─────────────────────────────
# STUDENT DATA
# ─────────────────────────────
STUDENT = {
    "name": "Alex Johnson",
    "id": "STU-2024-0042",
    "major": "Computer Science",
    "year": "Sophomore",
    "gpa": 3.72,
    "email": "alex.johnson@university.edu",
    "advisor": "Dr. Sarah Mitchell",
    "credits_completed": 45,
    "credits_required": 120,
    "semester": "Spring 2026",
}

# ─────────────────────────────
# COURSES
# ─────────────────────────────
COURSES = [
    {
        "id": 1,
        "code": "CS101",
        "title": "Intro to CS",
        "instructor": "Dr. Sarah Mitchell",
        "credits": 4,
        "grade": "A",
        "progress": 75,
        "color": "#6C63FF",
        "icon": "💻"
    },
    {
        "id": 2,
        "code": "MATH201",
        "title": "Calculus II",
        "instructor": "Prof. James Chen",
        "credits": 3,
        "grade": "B+",
        "progress": 60,
        "color": "#FF6584",
        "icon": "📐"
    },
]

# ─────────────────────────────
# ASSIGNMENTS
# ─────────────────────────────
ASSIGNMENTS = [
    {
        "title": "AI Project",
        "course": "CS101",
        "description": "Build a basic AI chatbot using Python.",
        "due": "2026-06-10",
        "points": 100,
        "status": "pending"
    },
    {
        "title": "Math Homework",
        "course": "MATH201",
        "description": "Complete calculus integration worksheet.",
        "due": "2026-06-05",
        "points": 50,
        "status": "submitted"
    },
    {
        "title": "Research Paper",
        "course": "CS101",
        "description": "Submit final research paper on machine learning.",
        "due": "2026-06-01",
        "points": 80,
        "status": "overdue"
    },
    {
        "title": "Programming Quiz",
        "course": "CS101",
        "description": "Online graded quiz for Python basics.",
        "due": "2026-05-30",
        "points": 25,
        "status": "graded"
    }
]

# ─────────────────────────────
# EVENTS
# ─────────────────────────────
EVENTS = [
    {
        "title": "Campus Culture Fair",
        "date": "2026-05-28",
        "time": "11:00 AM",
        "location": "Quad",
        "category": "Social",
        "image": "🌎",
        "color": "#FF6584"
    },
    {
        "title": "Tech Symposium",
        "date": "2026-06-05",
        "time": "10:00 AM",
        "location": "Auditorium",
        "category": "Academic",
        "image": "🎓",
        "color": "#6C63FF"
    },
]

# ─────────────────────────────
# FEES
# ─────────────────────────────
FEES = [
    {"label": "Tuition", "amount": 8500, "status": "paid"},
    {"label": "Library Fee", "amount": 150, "status": "pending"},
]

# ─────────────────────────────
# EXAM DATA
# ─────────────────────────────
SEMESTERS = [
    {
        "semester": 1,
        "label": "Sem 1",
        "overall_gpa": 3.6,
        "overall_grade": "A",
        "overall_percentage": 88,
        "result": "PASS",
        "period": "2025 Spring",
        "rank": 5,
        "total_students": 60,
        "subjects": [
            {
                "code": "CS101",
                "name": "Programming Basics",
                "credits": 4,
                "internal": 45,
                "external": 60,
                "total": 105,
                "max": 125,
                "grade": "A",
                "grade_point": 4.0,
                "status": "Pass"
            }
        ]
    }
]

# ─────────────────────────────
# ROUTES
# ─────────────────────────────

@app.route("/")
def index():
    return render_template(
        "index.html",
        student=STUDENT,
        courses=COURSES,
        events=EVENTS
    )

# OVERVIEW
@app.route("/overview")
def overview():

    pending_tasks = len(
        [a for a in ASSIGNMENTS if a["status"] == "pending"]
    )

    overdue_tasks = len(
        [a for a in ASSIGNMENTS if a["status"] == "overdue"]
    )

    return render_template(
        "overview.html",
        student=STUDENT,
        courses=COURSES,
        assignments=ASSIGNMENTS,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks
    )

# ASSIGNMENTS PAGE
@app.route("/assignments")
def assignments():
    return render_template(
        "assignments.html",
        student=STUDENT,
        assignments=ASSIGNMENTS
    )

# COURSES
@app.route("/courses")
def courses():
    return render_template(
        "courses.html",
        student=STUDENT,
        courses=COURSES
    )

# EVENTS
@app.route("/events")
def events():
    return render_template(
        "events.html",
        student=STUDENT,
        events=EVENTS
    )

# FEES
@app.route("/fees")
def fees():

    total = sum(f["amount"] for f in FEES)
    paid = sum(f["amount"] for f in FEES if f["status"] == "paid")
    pending = sum(f["amount"] for f in FEES if f["status"] != "paid")

    return render_template(
        "fees.html",
        student=STUDENT,
        fees=FEES,
        total=total,
        paid=paid,
        pending=pending
    )

# EXAMINATIONS
@app.route("/examinations")
def examinations():

    avg_gpa = round(
        sum(s["overall_gpa"] for s in SEMESTERS) / len(SEMESTERS),
        2
    )

    return render_template(
        "examinations.html",
        student=STUDENT,
        semesters=SEMESTERS,
        avg_gpa=avg_gpa
    )

# PROFILE
@app.route("/profile")
def profile():
    return render_template(
        "profile.html",
        student=STUDENT
    )

# LIBRARY
@app.route("/library")
def library():
    return render_template(
        "library.html",
        student=STUDENT
    )

# SUPPORT
@app.route("/support")
def support():
    return render_template(
        "support.html",
        student=STUDENT
    )

# ─────────────────────────────
# CHAT API
# ─────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()
    msg = data.get("message", "").lower()

    reply = "Hi! Ask me about fees, assignments, courses, or exams."

    if "gpa" in msg:
        reply = f"Your GPA is {STUDENT['gpa']}"

    elif "assignment" in msg:
        reply = "Check the Assignments page for deadlines."

    elif "exam" in msg:
        reply = "Check Examinations page for results."

    elif "fee" in msg:
        reply = "You have pending fees in the Fees section."

    return jsonify({
        "reply": reply,
        "time": datetime.now().strftime("%H:%M")
    })

# ─────────────────────────────
# RUN APP
# ─────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)