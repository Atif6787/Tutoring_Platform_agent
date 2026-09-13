from session_manager import (
    load_session,
    validate_session
)


def test_student_sessions():

    students = ["12345", "18822", "54321"]

    print("\n================================")
    print("   SESSION ISOLATION TEST")
    print("================================")

    sessions = {}

    # Load each student's own session
    for student_id in students:

        student = load_session(student_id)

        if student is None:
            print(f"❌ Student {student_id}: NOT FOUND")
            continue

        sessions[student_id] = student["session_id"]

        print(
            f"✅ Student {student_id} "
            f"→ Session {student['session_id']}"
        )

    print("\n---------- OWN SESSION TEST ----------")

    for student_id in students:

        session_id = sessions.get(student_id)

        if session_id and validate_session(student_id, session_id):

            print(
                f"✅ Student {student_id}: "
                f"own session accepted"
            )

        else:

            print(
                f"❌ Student {student_id}: "
                f"own session rejected"
            )

    print("\n---------- CROSS SESSION TEST ----------")

    for student_id in students:

        for other_student in students:

            if student_id == other_student:
                continue

            other_session = sessions.get(other_student)

            if validate_session(student_id, other_session):

                print(
                    f"❌ SECURITY PROBLEM: "
                    f"{student_id} accepted {other_student}'s session"
                )

            else:

                print(
                    f"✅ Secure: "
                    f"{student_id} rejected {other_student}'s session"
                )


if __name__ == "__main__":
    test_student_sessions()
