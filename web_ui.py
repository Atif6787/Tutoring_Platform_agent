from flask import Flask, request, redirect, url_for, render_template_string, session
from session_manager import (
    create_session,
    load_session,
    validate_session,
    save_quiz_result
)
from agent import (
    tutoring_agent,
    get_student_progress,
    get_weak_topics,
    get_practice_recommendation,
    get_improvement_report
)
from quiz import QUESTIONS, ADAPTIVE_QUESTIONS
import random


app = Flask(__name__)

# Local development only.
app.secret_key = "tutoring-platform-local-key"


HTML = """
<!DOCTYPE html>
<html>
<head>

    <title>Tutoring Platform</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            color: #1f2937;
        }

        .navbar {
            background: #172554;
            color: white;
            padding: 18px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar h1 {
            margin: 0;
            font-size: 22px;
        }

        .student {
            font-size: 14px;
            opacity: 0.9;
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(230px, 1fr));
            gap: 20px;
        }

        .card {
            background: white;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.07);
            margin-bottom: 20px;
        }

        .card h2,
        .card h3 {
            margin-top: 0;
        }

        .stat {
            font-size: 30px;
            font-weight: bold;
            color: #2563eb;
        }

        .small {
            color: #64748b;
            font-size: 14px;
        }

        .btn {
            display: inline-block;
            padding: 11px 18px;
            margin: 5px 5px 5px 0;
            border: none;
            border-radius: 8px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            cursor: pointer;
            font-size: 14px;
        }

        .btn:hover {
            opacity: 0.9;
        }

        .btn.green {
            background: #16a34a;
        }

        .btn.orange {
            background: #ea580c;
        }

        .btn.gray {
            background: #64748b;
        }

        .btn.red {
            background: #dc2626;
        }

        input[type=text],
        input[type=number] {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            margin: 8px 0 15px;
            font-size: 15px;
        }

        .option {
            display: block;
            padding: 12px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin: 8px 0;
            cursor: pointer;
        }

        .option:hover {
            background: #eff6ff;
        }

        .topic {
            display: flex;
            justify-content: space-between;
            padding: 14px 0;
            border-bottom: 1px solid #e5e7eb;
        }

        .progress {
            background: #e5e7eb;
            border-radius: 10px;
            height: 10px;
            margin-top: 7px;
        }

        .progress-bar {
            background: #2563eb;
            height: 10px;
            border-radius: 10px;
        }

        .chat {
            background: #f8fafc;
            border-radius: 10px;
            padding: 15px;
            white-space: pre-wrap;
            margin-bottom: 15px;
        }

        .success {
            background: #dcfce7;
            color: #166534;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .warning {
            background: #fef3c7;
            color: #92400e;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }

        @media(max-width: 600px) {

            .navbar {
                padding: 15px;
            }

            .container {
                padding: 0 12px;
            }
        }

    </style>

</head>

<body>

<div class="navbar">

    <h1>🎓 Tutoring Platform</h1>

    {% if student_id %}
        <div class="student">
            Student: {{ student_id }}
        </div>
    {% endif %}

</div>


<div class="container">

{% if student_id %}

    <div style="margin-bottom:20px">

        <a class="btn"
           href="{{ url_for('dashboard') }}">
           Dashboard
        </a>

        <a class="btn"
           href="{{ url_for('quiz') }}">
           Mathematics Quiz
        </a>

        <a class="btn green"
           href="{{ url_for('adaptive') }}">
           Adaptive Practice
        </a>

        <a class="btn orange"
           href="{{ url_for('agent') }}">
           🤖 Tutor Agent
        </a>

        <a class="btn gray"
           href="{{ url_for('history') }}">
           History
        </a>

        <a class="btn red"
           href="{{ url_for('logout') }}">
           Logout
        </a>

    </div>

{% endif %}

{{ content|safe }}

</div>

</body>
</html>
"""


def page(content, **kwargs):

    return render_template_string(
        HTML,
        content=content,
        **kwargs
    )


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        student_id = request.form["student_id"].strip()

        if not student_id:
            return page(
                """
                <div class="card">
                    <div class="warning">
                        Please enter a Student ID.
                    </div>
                    <a class="btn" href="/">Back</a>
                </div>
                """,
                student_id=None
            )

        student = load_session(student_id)

        if student is None:

            session_id = create_session(student_id)

        else:

            session_id = student["session_id"]

        session["student_id"] = student_id
        session["session_id"] = session_id

        return redirect(
            url_for("dashboard")
        )

    return page(
        """
        <div class="card"
             style="max-width:500px;margin:70px auto">

            <h2>Welcome 👋</h2>

            <p class="small">
                Enter your Student ID to access
                your personal tutoring session.
            </p>

            <form method="post">

                <label>Student ID</label>

                <input
                    type="text"
                    name="student_id"
                    placeholder="Example: 12345"
                    required
                >

                <button class="btn" type="submit">
                    Start Learning
                </button>

            </form>

        </div>
        """,
        student_id=None
    )


def get_current_student():

    student_id = session.get("student_id")
    session_id = session.get("session_id")

    if not student_id or not session_id:
        return None, None

    if not validate_session(
        student_id,
        session_id
    ):
        return None, None

    return (
        student_id,
        load_session(student_id)
    )


@app.route("/dashboard")
def dashboard():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    progress = get_student_progress(student)
    weak_topics = get_weak_topics(student)

    if progress:

        score = (
            f"{progress['score']}/"
            f"{progress['total']}"
        )

        percentage = (
            f"{progress['percentage']:.1f}%"
        )

        level = progress["level"]

    else:

        score = "0/0"
        percentage = "0%"
        level = "New Student"

    topic_html = ""

    for item in weak_topics:

        percentage_value = min(
            100,
            max(0, item["percentage"])
        )

        topic_html += f"""
        <div class="topic">

            <div style="width:70%">

                <strong>
                    {item['topic']}
                </strong>

                <div class="progress">

                    <div class="progress-bar"
                         style="width:{percentage_value}%">
                    </div>

                </div>

            </div>

            <strong>
                {item['percentage']:.1f}%
            </strong>

        </div>
        """

    if not topic_html:

        topic_html = """
        <p class="small">
            Complete a mathematics quiz to
            see topic performance.
        </p>
        """

    recommendation = get_practice_recommendation(
        student
    )

    content = f"""

    <h2>Welcome back, {student_id} 👋</h2>

    <div class="grid">

        <div class="card">

            <div class="small">
                Overall Score
            </div>

            <div class="stat">
                {score}
            </div>

        </div>


        <div class="card">

            <div class="small">
                Overall Percentage
            </div>

            <div class="stat">
                {percentage}
            </div>

        </div>


        <div class="card">

            <div class="small">
                Learning Level
            </div>

            <div class="stat"
                 style="font-size:22px">
                {level}
            </div>

        </div>


        <div class="card">

            <div class="small">
                Quiz Attempts
            </div>

            <div class="stat">
                {progress['attempts'] if progress else 0}
            </div>

        </div>

    </div>


    <div class="card">

        <h2>📊 Topic Performance</h2>

        {topic_html}

    </div>


    <div class="card">

        <h2>🎯 Tutor Recommendation</h2>

        <p>
            {recommendation}
        </p>

        <a class="btn green"
           href="{{ url_for('adaptive') }}">
           Start Adaptive Practice
        </a>

    </div>


    <div class="card">

        <h2>🤖 AI Tutor</h2>

        <p class="small">
            Ask about your progress, weak topics,
            mathematics, or what you should practice.
        </p>

        <a class="btn orange"
           href="{{ url_for('agent') }}">
           Open Tutor
        </a>

    </div>
    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/history")
def history():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    rows = ""

    for result in reversed(
        student["quiz_history"]
    ):

        rows += f"""
        <tr>

            <td>
                {result['quiz_name']}
            </td>

            <td>
                {result['score']}/
                {result['total']}
            </td>

            <td>
                {(
                    result['score'] /
                    result['total'] * 100
                ) if result['total'] else 0:.1f}%
            </td>

        </tr>
        """

    if not rows:

        rows = """
        <tr>
            <td colspan="3">
                No practice history yet.
            </td>
        </tr>
        """

    content = f"""

    <div class="card">

        <h2>📚 Practice History</h2>

        <table>

            <tr>
                <th>Activity</th>
                <th>Score</th>
                <th>Percentage</th>
            </tr>

            {rows}

        </table>

    </div>

    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    if request.method == "POST":

        score = 0
        topic_results = {}

        for index, question in enumerate(
            QUESTIONS
        ):

            answer = request.form.get(
                f"q{index}"
            )

            topic = question["topic"]

            if topic not in topic_results:

                topic_results[topic] = {
                    "score": 0,
                    "total": 0
                }

            topic_results[topic]["total"] += 1

            if answer == question["answer"]:

                score += 1

                topic_results[topic][
                    "score"
                ] += 1

        save_quiz_result(
            student_id,
            session["session_id"],
            "Mathematics",
            score,
            len(QUESTIONS),
            topic_results
        )

        return redirect(
            url_for("quiz_result",
                    score=score)
        )

    questions_html = ""

    for index, question in enumerate(
        QUESTIONS
    ):

        options = ""

        for option in question["options"]:

            options += f"""
            <label class="option">

                <input
                    type="radio"
                    name="q{index}"
                    value="{option}"
                    required
                >

                {option}

            </label>
            """

        questions_html += f"""

        <div class="card">

            <div class="small">
                Topic: {question['topic']}
            </div>

            <h3>
                Question {index + 1}
            </h3>

            <p>
                {question['question']}
            </p>

            {options}

        </div>

        """

    content = f"""

    <h2>📝 Mathematics Quiz</h2>

    <form method="post">

        {questions_html}

        <button
            class="btn"
            type="submit">
            Submit Quiz
        </button>

    </form>

    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/quiz-result")
def quiz_result():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    score = int(
        request.args.get("score", 0)
    )

    total = len(QUESTIONS)

    percentage = (
        score / total * 100
    ) if total else 0

    content = f"""

    <div class="card"
         style="text-align:center">

        <h2>🎉 Quiz Complete</h2>

        <div class="stat">
            {score}/{total}
        </div>

        <h3>
            {percentage:.1f}%
        </h3>

        <p>
            Your result has been saved
            to your personal history.
        </p>

        <a class="btn"
           href="{{ url_for('dashboard') }}">
           Dashboard
        </a>

        <a class="btn green"
           href="{{ url_for('adaptive') }}">
           Adaptive Practice
        </a>

    </div>

    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/adaptive")
def adaptive():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    weak_topics = get_weak_topics(student)

    topics = [
        item["topic"]
        for item in weak_topics[:2]
        if item["percentage"] < 80
    ]

    if not topics:

        content = """

        <div class="card">

            <h2>🎯 Adaptive Practice</h2>

            <div class="success">
                Your recorded performance is strong.
                Complete another quiz to update
                your learning profile.
            </div>

            <a class="btn"
               href="/quiz">
               Take Quiz
            </a>

        </div>

        """

        return page(
            content,
            student_id=student_id
        )

    return adaptive_questions(
        student_id,
        topics
    )


def adaptive_questions(
    student_id,
    topics
):

    if request.args.get("done") == "1":

        return redirect(
            url_for("dashboard")
        )

    questions = []

    for topic in topics:

        topic_questions = []

        for difficulty in [
            "easy",
            "medium",
            "hard"
        ]:

            topic_questions.extend(
                ADAPTIVE_QUESTIONS[
                    topic
                ][difficulty]
            )

        random.shuffle(topic_questions)

        topic_questions = topic_questions[:3]

        for question in topic_questions:

            questions.append(
                {
                    "topic": topic,
                    "question": question
                }
            )

    session["adaptive_questions"] = [
        {
            "topic": item["topic"],
            "question": item["question"]["question"],
            "options": item["question"]["options"],
            "answer": item["question"]["answer"]
        }
        for item in questions
    ]

    return render_adaptive_form(
        student_id,
        questions
    )


def render_adaptive_form(
    student_id,
    questions
):

    html = ""

    for index, item in enumerate(
        questions
    ):

        question = item["question"]

        options = ""

        for option in question["options"]:

            options += f"""
            <label class="option">

                <input
                    type="radio"
                    name="q{index}"
                    value="{option}"
                    required
                >

                {option}

            </label>
            """

        html += f"""

        <div class="card">

            <div class="small">
                Topic: {item['topic']}
            </div>

            <h3>
                Question {index + 1}
            </h3>

            <p>
                {question['question']}
            </p>

            {options}

        </div>

        """

    content = f"""

    <h2>🎯 Adaptive Personalized Practice</h2>

    <div class="card">

        <p>
            Your tutor selected these weak topics:
        </p>

        <strong>
            {' • '.join(
                item['topic']
                for item in questions
            )}
        </strong>

        <p class="small">
            Answer the questions and the system
            will save your personalized result.
        </p>

    </div>

    <form method="post"
          action="/adaptive-submit">

        {html}

        <button class="btn green"
                type="submit">
            Submit Practice
        </button>

    </form>

    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/adaptive-submit", methods=["POST"])
def adaptive_submit():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    questions = session.get(
        "adaptive_questions",
        []
    )

    if not questions:

        return redirect(
            url_for("adaptive")
        )

    score = 0
    topic_results = {}

    for index, question in enumerate(
        questions
    ):

        topic = question["topic"]

        if topic not in topic_results:

            topic_results[topic] = {
                "score": 0,
                "total": 0
            }

        topic_results[topic]["total"] += 1

        answer = request.form.get(
            f"q{index}"
        )

        if answer == question["answer"]:

            score += 1

            topic_results[topic][
                "score"
            ] += 1

    save_quiz_result(
        student_id,
        session["session_id"],
        "Adaptive Personalized Practice",
        score,
        len(questions),
        topic_results
    )

    session.pop(
        "adaptive_questions",
        None
    )

    percentage = (
        score / len(questions) * 100
    ) if questions else 0

    content = f"""

    <div class="card"
         style="text-align:center">

        <h2>🎯 Adaptive Practice Complete</h2>

        <div class="stat">
            {score}/{len(questions)}
        </div>

        <h3>
            {percentage:.1f}%
        </h3>

        <p>
            Your personalized practice result
            has been saved.
        </p>

        <a class="btn"
           href="/dashboard">
           Dashboard
        </a>

    </div>

    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/agent", methods=["GET", "POST"])
def agent():

    student_id, student = get_current_student()

    if student is None:
        return redirect(url_for("login"))

    answer = None
    question = None

    if request.method == "POST":

        question = request.form[
            "question"
        ]

        answer = tutoring_agent(
            student_id,
            session["session_id"],
            question
        )

    chat = ""

    if question:

        chat = f"""

        <div class="chat">

            <strong>You:</strong>

            {question}

        </div>

        <div class="chat">

            <strong>🤖 Tutor:</strong>

            {answer}

        </div>

        """

    content = f"""

    <div class="card">

        <h2>🤖 Tutoring Agent</h2>

        <p class="small">
            Ask your personal tutor anything
            about mathematics, progress,
            weak topics, or practice.
        </p>

        {chat}

        <form method="post">

            <input
                type="text"
                name="question"
                placeholder="Example: What should I practice?"
                required
            >

            <button class="btn orange"
                    type="submit">
                Ask Tutor
            </button>

        </form>

    </div>

    <div class="card">

        <h3>Try asking:</h3>

        <p>• What should I practice?</p>
        <p>• What am I weak at?</p>
        <p>• How am I improving?</p>
        <p>• What is multiplication?</p>
        <p>• What is 25 + 17?</p>

    </div>

    """

    return page(
        content,
        student_id=student_id
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":

    print("")
    print("========================================")
    print("       TUTORING PLATFORM WEB UI")
    print("========================================")
    print("")
    print("Open in your browser:")
    print("http://127.0.0.1:5000")
    print("")
    print("Press CTRL+C to stop the server.")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
