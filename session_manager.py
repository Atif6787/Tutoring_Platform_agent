import json
import uuid
from pathlib import Path


STUDENTS_DIR = Path("students")
STUDENTS_DIR.mkdir(exist_ok=True)


def create_session(student_id):

    session_id = str(uuid.uuid4())

    file_path = STUDENTS_DIR / f"{student_id}.json"

    student_data = {
        "student_id": student_id,
        "session_id": session_id,
        "quiz_history": []
    }

    with open(file_path, "w", encoding="utf-8-sig") as file:
        json.dump(student_data, file, indent=4)

    return session_id


def load_session(student_id):

    file_path = STUDENTS_DIR / f"{student_id}.json"

    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def validate_session(student_id, session_id):

    student = load_session(student_id)

    if student is None:
        return False

    return student["session_id"] == session_id


def save_quiz_result(
    student_id,
    session_id,
    quiz_name,
    score,
    total,
    topic_results=None
):

    if not validate_session(student_id, session_id):
        return False

    student = load_session(student_id)

    result = {
        "quiz_name": quiz_name,
        "score": score,
        "total": total
    }

    if topic_results is not None:
        result["topic_results"] = topic_results

    student["quiz_history"].append(result)

    file_path = STUDENTS_DIR / f"{student_id}.json"

    with open(file_path, "w", encoding="utf-8-sig") as file:
        json.dump(student, file, indent=4)

    return True
