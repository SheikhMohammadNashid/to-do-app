from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# Database Configuration
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://todo:todo@todo-db:5432/tododb"
)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Model
# -----------------------------
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# -----------------------------
# Create Tables (Docker-safe)
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# Routes
# -----------------------------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "title": t.title, "completed": t.completed}
        for t in tasks
    ])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task added"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()

    return jsonify({"message": "Task updated"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})

# -----------------------------
# App Runner
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
