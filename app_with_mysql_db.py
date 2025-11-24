from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --------------------------
# DATABASE CONFIG
# --------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------
# PART 1: USER MODEL
# --------------------------

class User ( db . Model ):
    id = db . Column ( db . Integer , primary_key = True )
    username = db . Column ( db . String (50) , unique = True )
    email = db . Column ( db . String (100) , unique = True )
    created_at = db . Column ( db . DateTime )

    # Relationship (one user -> many tasks)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# --------------------------
# TASK MODEL
# --------------------------
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FOREIGN KEY
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id
        }

# --------------------------
# CREATE TABLES AUTOMATICALLY
# --------------------------
with app.app_context () :
    db.create_all ()
    print (" Database tables created !")


# ---------------------------------------------------
# PART 2: USER CRUD ENDPOINTS
# ---------------------------------------------------
@app.route('/')
def home():
    return "Backend is running!", 200

# CREATE USER
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# GET ALL USERS
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify ({
            'tasks': [ u.to_dict() for u in users],
            'count ': len ( users )
            }) , 200


# GET ONE USER
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404 (user_id)
    return jsonify(user.to_dict()), 200


# UPDATE USER
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404 (user_id)

    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify(user.to_dict()), 200


# DELETE USER
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404 (user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


# ---------------------------------------------------
# PART 3: LINK TASK TO USER
# ---------------------------------------------------

# CREATE TASK FOR USER
@app.route('/api/users/<int:user_id>/tasks', methods=['POST'])
def create_task_for_user(user_id):
    user = User.query.get_or_404 (user_id)

    data = request.json
    new_task = Task(
        title=data["title"],
        is_done=data.get("is_done", False),
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


# GET ALL TASKS FOR USER
@app.route('/api/users/<int:user_id>/tasks', methods=['GET'])
def get_tasks_for_user(user_id):
    user = User.query.get_or_404 (user_id)

    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([t.to_dict() for t in tasks]), 200


if __name__ == "__main__":
    app.run(debug=True , port = 5000)
