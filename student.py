#%%
from flask import Flask, jsonify, request

app = Flask(__name__)

students_data = [
    {"id": 12345, "name": "John Doe", "course": "Computer Science", "year": 2, "gpa": 3.8},
    {"id": 12346, "name": "Jane Smith", "course": "Biology", "year": 3, "gpa": 3.6},
    {"id": 12347, "name": "Alice Brown", "course": "Engineering", "year": 1, "gpa": 3.9}
]


# Get student info by ID
@app.route('/api/student', methods=['GET'])
def get_student_info():
    student_id = request.args.get('id', type=int)

    student = next((s for s in students_data if s["id"] == student_id), None)
    if student:
        return jsonify(student), 200
    else:
        return jsonify({"error": "Student not found"}), 404


# Get the total number of students
@app.route('/api/students/count', methods=['GET'])
def get_student_count():
    return jsonify({"total_students": len(students_data)}), 200


if __name__ == '__main__':
    app.run(debug=True , port=5000)