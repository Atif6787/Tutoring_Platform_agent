import json
from pathlib import Path

from session_manager import load_session, validate_session


KNOWLEDGE_FILE = Path("knowledge/mathematics.json")


def load_knowledge():

    if not KNOWLEDGE_FILE.exists():
        return {}

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:

        return json.load(file)


def calculate_math(question):

    question = (
        question
        .lower()
        .strip()
        .replace(" ", "")
    )

    operators = ["+", "-", "*", "x", "/"]

    for operator in operators:

        if operator in question:

            try:

                if operator == "x":
                    parts = question.split("x")
                else:
                    parts = question.split(operator)

                if len(parts) != 2:
                    return None

                number1 = float(parts[0])
                number2 = float(parts[1])

                if operator == "+":
                    answer = number1 + number2

                elif operator == "-":
                    answer = number1 - number2

                elif operator == "*" or operator == "x":
                    answer = number1 * number2

                elif operator == "/":

                    if number2 == 0:
                        return "You cannot divide by zero."

                    answer = number1 / number2

                if answer.is_integer():
                    answer = int(answer)

                return f"The answer is {answer}."

            except ValueError:

                return None

    return None


def find_knowledge_answer(question):

    knowledge = load_knowledge()

    question = question.lower().strip()

    for topic, answer in knowledge.items():

        if topic in question:
            return answer

    return None


def get_student_progress(student):

    history = student["quiz_history"]

    if not history:
        return None

    total_score = sum(
        item["score"]
        for item in history
    )

    total_questions = sum(
        item["total"]
        for item in history
    )

    if total_questions == 0:
        return None

    percentage = (
        total_score / total_questions
    ) * 100

    if percentage >= 80:

        level = "Good"

    elif percentage >= 50:

        level = "Needs some practice"

    else:

        level = "Needs more practice"

    return {
        "attempts": len(history),
        "score": total_score,
        "total": total_questions,
        "percentage": percentage,
        "level": level
    }


def get_weak_topics(student):

    history = student.get("quiz_history", [])

    topic_totals = {}

    # Older results still matter, but recent results
    # receive more weight.
    for index, quiz in enumerate(history):

        topic_results = quiz.get(
            "topic_results",
            {}
        )

        if not topic_results:
            continue

        # Recent attempts get larger weights.
        weight = index + 1

        for topic, result in topic_results.items():

            if topic not in topic_totals:

                topic_totals[topic] = {
                    "score": 0,
                    "total": 0,
                    "weighted_score": 0,
                    "weighted_total": 0
                }

            score = result.get("score", 0)
            total = result.get("total", 0)

            topic_totals[topic]["score"] += score
            topic_totals[topic]["total"] += total

            topic_totals[topic][
                "weighted_score"
            ] += score * weight

            topic_totals[topic][
                "weighted_total"
            ] += total * weight

    weak_topics = []

    for topic, result in topic_totals.items():

        if result["total"] == 0:
            continue

        overall_percentage = (
            result["score"] /
            result["total"]
        ) * 100

        recent_percentage = (
            result["weighted_score"] /
            result["weighted_total"]
        ) * 100

        # 60% recent performance
        # 40% overall performance
        current_percentage = (
            recent_percentage * 0.60
            + overall_percentage * 0.40
        )

        weak_topics.append({
            "topic": topic,
            "score": result["score"],
            "total": result["total"],
            "percentage": current_percentage,
            "overall_percentage": overall_percentage,
            "recent_percentage": recent_percentage
        })

    weak_topics.sort(
        key=lambda item: item["percentage"]
    )

    return weak_topics


def get_practice_recommendation(student):

    weak_topics = get_weak_topics(student)

    if not weak_topics:

        return (
            "There is not enough topic-level history yet. "
            "Complete a mathematics quiz first."
        )

    weakest = weak_topics[:2]

    weak_names = [
        item["topic"]
        for item in weakest
        if item["percentage"] < 80
    ]

    if not weak_names:

        return (
            "Your performance is strong across "
            "the recorded topics. "
            "Try more challenging questions."
        )

    details = []

    for item in weakest:

        if item["percentage"] < 80:

            details.append(
                f"{item['topic']} "
                f"{item['percentage']:.1f}%"
            )

    topics = " and ".join(weak_names)

    return (
        f"Your current focus should be {topics}. "
        f"Current weighted performance: "
        f"{', '.join(details)}. "
        f"I recommend adaptive practice for these topics."
    )


def get_improvement_report(student):

    weak_topics = get_weak_topics(student)

    if not weak_topics:

        return (
            "There is not enough topic-level history "
            "to measure improvement yet."
        )

    lines = []

    for item in weak_topics:

        change = (
            item["recent_percentage"]
            - item["overall_percentage"]
        )

        if change > 5:

            status = "improving"

        elif change < -5:

            status = "needs attention"

        else:

            status = "stable"

        lines.append(
            f"{item['topic']}: "
            f"overall {item['overall_percentage']:.1f}%, "
            f"recent {item['recent_percentage']:.1f}% "
            f"({status})"
        )

    return (
        "Here is your topic improvement report:\n"
        + "\n".join(lines)
    )


def tutoring_agent(
    student_id,
    session_id,
    question
):

    if not validate_session(
        student_id,
        session_id
    ):

        return (
            "Session validation failed. "
            "Access denied."
        )

    student = load_session(student_id)

    question_lower = (
        question.lower().strip()
    )

    math_answer = calculate_math(question)

    if math_answer is not None:
        return math_answer

    knowledge_answer = find_knowledge_answer(
        question
    )

    if knowledge_answer is not None:
        return knowledge_answer

    improvement_words = [
        "improvement",
        "improving",
        "getting better",
        "progress",
        "performance"
    ]

    if any(
        word in question_lower
        for word in improvement_words
    ):

        return get_improvement_report(
            student
        )

    recommendation_words = [
        "practice",
        "weak",
        "improve",
        "recommend",
        "study"
    ]

    if any(
        word in question_lower
        for word in recommendation_words
    ):

        return get_practice_recommendation(
            student
        )

    progress_words = [
        "score",
        "result",
        "history",
        "doing",
        "level"
    ]

    if any(
        word in question_lower
        for word in progress_words
    ):

        progress = get_student_progress(
            student
        )

        if progress is None:

            return (
                "You do not have any quiz history yet. "
                "Take a mathematics quiz first."
            )

        return (
            f"You have completed "
            f"{progress['attempts']} quiz attempt(s). "
            f"Your overall score is "
            f"{progress['score']}/"
            f"{progress['total']} "
            f"({progress['percentage']:.1f}%). "
            f"Your current level is: "
            f"{progress['level']}."
        )

    return (
        "I can help you with mathematics, "
        "your progress, weak topics, "
        "improvement, and adaptive practice."
    )


if __name__ == "__main__":

    print(
        "Tutoring agent module loaded successfully."
    )
