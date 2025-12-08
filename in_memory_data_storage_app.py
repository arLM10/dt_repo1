from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In‑memory storage
tasks  = []
categories = []

def valid_date(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except:
        return False


# Category Endpoints

@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.get("/api/categories")
def list_categories():
    return jsonify(categories)

@app.post("/api/categories")
def create_category():
    name = request.json.get("name")
    if not name:
        return {"error": "Name required"}, 400
    if any(c["name"] == name for c in categories):
        return {"error": "Category exists"}, 400

    category = {"id": len(categories)+1, "name": name}
    categories.append(category)
    return category, 201

# Tasks CRUD

@app.get("/api/tasks")
def list_tasks():
    cat = request.args.get("category")
    return jsonify([t for t in tasks if t["category"] == cat]) if cat else jsonify(tasks)

@app.post("/api/tasks")
def add_task():
    data = request.json
    title = data.get("title")
    category = data.get("category")
    due = data.get("due_date")
    priority = data.get("priority", "medium")

    if not title:
        return {"error": "Title required"}, 400
    if category and category not in [c["name"] for c in categories]:
        return {"error": "Invalid category"}, 400
    if due and not valid_date(due):
        return {"error": "Invalid date"}, 400
    if priority not in ["low", "medium", "high"]:
        return {"error": "Invalid priority"}, 400

    task = {
        "id": len(tasks)+1,
        "title": title,
        "completed": False,
        "category": category,
        "due_date": due,
        "priority": priority
    }
    tasks.append(task)
    return task, 201

@app.patch("/api/tasks/<int:id>")
def update_task(id):
    task = next((t for t in tasks if t["id"] == id), None)
    if not task:
        return {"error": "Not found"}, 404

    data = request.json
    if "title" in data: task["title"] = data["title"]
    if "completed" in data: task["completed"] = bool(data["completed"])

    if "category" in data:
        if data["category"] not in [c["name"] for c in categories]:
            return {"error": "Invalid category"}, 400
        task["category"] = data["category"]

    if "due_date" in data:
        if data["due_date"] and not valid_date(data["due_date"]):
            return {"error": "Invalid date"}, 400
        task["due_date"] = data["due_date"]

    if "priority" in data:
        if data["priority"] not in ["low", "medium", "high"]:
            return {"error": "Bad priority"}, 400
        task["priority"] = data["priority"]

    return task


# Overdue Tasks

@app.get("/api/tasks/overdue")
def overdue():
    today = datetime.today().date()
    return jsonify([
        t for t in tasks
        if t.get("due_date") and datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today and not t["completed"]
    ])


# Statistics

@app.get("/api/tasks/stats")
def stats():
    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    pending = total - completed

    today = datetime.today().date()
    overdue = len([
        t for t in tasks
        if t.get("due_date") and datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today and not t["completed"]
    ])

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)
