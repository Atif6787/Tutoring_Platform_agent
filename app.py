from session_manager import (
    create_session,
    load_session,
    validate_session,
    save_quiz_result
)

from quiz import (
    start_quiz,
    start_adaptive_practice
)

from agent import (
    tutoring_agent,
    get_weak_topics
)


def main():

    print("================================")
    print("       TUTORING PLATFORM")
    print("================================")

    student_id = input(
        "\nEnter Student ID: "
    )

    student = load_session(
        student_id
    )

    if student is None:

        session_id = create_session(
            student_id
        )

        print(
            "\nNew student session created."
        )

    else:

        session_id = student["session_id"]

        print(
            "\nExisting student session loaded."
        )

    print(
        "Student ID:",
        student_id
    )

    print(
        "Session ID:",
        session_id
    )

    while True:

        print("\n========== MENU ==========")
        print("1. Start Quiz")
        print("2. View My Practice History")
        print("3. Ask Tutoring Agent")
        print("4. Adaptive Personalized Practice")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":

            score, total, topic_results = (
                start_quiz()
            )

            saved = save_quiz_result(
                student_id,
                session_id,
                "Mathematics",
                score,
                total,
                topic_results
            )

            if saved:

                print(
                    "\nPractice history saved."
                )

            else:

                print(
                    "\nSession validation failed."
                )

        elif choice == "2":

            if not validate_session(
                student_id,
                session_id
            ):

                print(
                    "\nSession validation failed."
                )

                continue

            student = load_session(
                student_id
            )

            print(
                "\n====== MY PRACTICE HISTORY ======"
            )

            if not student["quiz_history"]:

                print(
                    "No practice history."
                )

            else:

                for result in student[
                    "quiz_history"
                ]:

                    print(
                        f"{result['quiz_name']} - "
                        f"{result['score']}/"
                        f"{result['total']}"
                    )

                    if "topic_results" in result:

                        for topic, data in result[
                            "topic_results"
                        ].items():

                            print(
                                f"   {topic}: "
                                f"{data['score']}/"
                                f"{data['total']}"
                            )

        elif choice == "3":

            question = input(
                "\nAsk the tutoring agent: "
            )

            response = tutoring_agent(
                student_id,
                session_id,
                question
            )

            print(
                "\nAgent:",
                response
            )

        elif choice == "4":

            if not validate_session(
                student_id,
                session_id
            ):

                print(
                    "\nSession validation failed."
                )

                continue

            student = load_session(
                student_id
            )

            weak_topics = get_weak_topics(
                student
            )

            if not weak_topics:

                print(
                    "\nNot enough topic-level "
                    "history yet."
                )

                print(
                    "Complete a mathematics quiz first."
                )

                continue

            # Select up to two weakest topics.
            weakest_topics = [
                item["topic"]
                for item in weak_topics[:2]
                if item["percentage"] < 80
            ]

            if not weakest_topics:

                print(
                    "\nYour performance is strong "
                    "across all recorded topics."
                )

                print(
                    "Try a normal quiz or "
                    "more challenging questions."
                )

                continue

            print(
                "\n====== ADAPTIVE PERSONALIZED "
                "PRACTICE ======"
            )

            print(
                "\nCurrent focus topics:"
            )

            for topic in weakest_topics:

                print(
                    "-",
                    topic
                )

            score, total, topic_results = (
                start_adaptive_practice(
                    weakest_topics
                )
            )

            if total > 0:

                saved = save_quiz_result(
                    student_id,
                    session_id,
                    "Adaptive Personalized Practice",
                    score,
                    total,
                    topic_results
                )

                if saved:

                    print(
                        "\nAdaptive practice "
                        "history saved."
                    )

                else:

                    print(
                        "\nSession validation failed."
                    )

        elif choice == "5":

            print(
                "\nSession ended."
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


if __name__ == "__main__":

    main()
