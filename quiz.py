QUESTIONS = [
    {
        "topic": "Addition",
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    },
    {
        "topic": "Subtraction",
        "question": "What is 5 - 3?",
        "options": ["1", "2", "3", "4"],
        "answer": "2"
    },
    {
        "topic": "Multiplication",
        "question": "What is 5 * 3?",
        "options": ["10", "15", "20", "25"],
        "answer": "15"
    },
    {
        "topic": "Division",
        "question": "What is 12 / 3?",
        "options": ["2", "3", "4", "6"],
        "answer": "4"
    }
]


ADAPTIVE_QUESTIONS = {

    "Addition": {
        "easy": [
            {
                "question": "What is 5 + 3?",
                "options": ["6", "7", "8", "9"],
                "answer": "8"
            },
            {
                "question": "What is 7 + 2?",
                "options": ["8", "9", "10", "11"],
                "answer": "9"
            },
            {
                "question": "What is 9 + 4?",
                "options": ["12", "13", "14", "15"],
                "answer": "13"
            }
        ],

        "medium": [
            {
                "question": "What is 17 + 8?",
                "options": ["23", "24", "25", "26"],
                "answer": "25"
            },
            {
                "question": "What is 25 + 16?",
                "options": ["39", "40", "41", "42"],
                "answer": "41"
            },
            {
                "question": "What is 38 + 27?",
                "options": ["55", "65", "75", "85"],
                "answer": "65"
            }
        ],

        "hard": [
            {
                "question": "What is 125 + 78?",
                "options": ["193", "203", "213", "223"],
                "answer": "203"
            },
            {
                "question": "What is 246 + 189?",
                "options": ["425", "435", "445", "455"],
                "answer": "435"
            },
            {
                "question": "What is 375 + 248?",
                "options": ["613", "623", "633", "643"],
                "answer": "623"
            }
        ]
    },


    "Subtraction": {
        "easy": [
            {
                "question": "What is 8 - 3?",
                "options": ["4", "5", "6", "7"],
                "answer": "5"
            },
            {
                "question": "What is 10 - 4?",
                "options": ["5", "6", "7", "8"],
                "answer": "6"
            },
            {
                "question": "What is 12 - 5?",
                "options": ["5", "6", "7", "8"],
                "answer": "7"
            }
        ],

        "medium": [
            {
                "question": "What is 15 - 7?",
                "options": ["6", "7", "8", "9"],
                "answer": "8"
            },
            {
                "question": "What is 20 - 9?",
                "options": ["9", "10", "11", "12"],
                "answer": "11"
            },
            {
                "question": "What is 35 - 17?",
                "options": ["16", "17", "18", "19"],
                "answer": "18"
            }
        ],

        "hard": [
            {
                "question": "What is 125 - 78?",
                "options": ["37", "47", "57", "67"],
                "answer": "47"
            },
            {
                "question": "What is 250 - 137?",
                "options": ["103", "113", "123", "133"],
                "answer": "113"
            },
            {
                "question": "What is 425 - 186?",
                "options": ["229", "239", "249", "259"],
                "answer": "239"
            }
        ]
    },


    "Multiplication": {
        "easy": [
            {
                "question": "What is 3 * 4?",
                "options": ["7", "12", "14", "16"],
                "answer": "12"
            },
            {
                "question": "What is 5 * 2?",
                "options": ["8", "10", "12", "15"],
                "answer": "10"
            },
            {
                "question": "What is 4 * 3?",
                "options": ["7", "12", "14", "16"],
                "answer": "12"
            }
        ],

        "medium": [
            {
                "question": "What is 7 * 5?",
                "options": ["30", "35", "40", "45"],
                "answer": "35"
            },
            {
                "question": "What is 8 * 6?",
                "options": ["42", "48", "54", "56"],
                "answer": "48"
            },
            {
                "question": "What is 9 * 7?",
                "options": ["56", "63", "72", "81"],
                "answer": "63"
            }
        ],

        "hard": [
            {
                "question": "What is 12 * 8?",
                "options": ["86", "96", "108", "112"],
                "answer": "96"
            },
            {
                "question": "What is 15 * 7?",
                "options": ["95", "100", "105", "110"],
                "answer": "105"
            },
            {
                "question": "What is 18 * 9?",
                "options": ["152", "162", "172", "182"],
                "answer": "162"
            }
        ]
    },


    "Division": {
        "easy": [
            {
                "question": "What is 10 / 2?",
                "options": ["3", "4", "5", "6"],
                "answer": "5"
            },
            {
                "question": "What is 12 / 3?",
                "options": ["2", "3", "4", "6"],
                "answer": "4"
            },
            {
                "question": "What is 16 / 4?",
                "options": ["2", "3", "4", "5"],
                "answer": "4"
            }
        ],

        "medium": [
            {
                "question": "What is 20 / 5?",
                "options": ["2", "4", "5", "6"],
                "answer": "4"
            },
            {
                "question": "What is 24 / 6?",
                "options": ["3", "4", "5", "6"],
                "answer": "4"
            },
            {
                "question": "What is 30 / 5?",
                "options": ["4", "5", "6", "7"],
                "answer": "6"
            }
        ],

        "hard": [
            {
                "question": "What is 72 / 8?",
                "options": ["7", "8", "9", "10"],
                "answer": "9"
            },
            {
                "question": "What is 96 / 12?",
                "options": ["6", "8", "9", "12"],
                "answer": "8"
            },
            {
                "question": "What is 144 / 12?",
                "options": ["10", "11", "12", "14"],
                "answer": "12"
            }
        ]
    }
}


def start_quiz():

    score = 0
    topic_results = {}

    print("\n========== MATHEMATICS QUIZ ==========")

    for number, question in enumerate(QUESTIONS, 1):

        print(f"\nQuestion {number}: {question['question']}")
        print("Topic:", question["topic"])

        for i, option in enumerate(question["options"], 1):
            print(f"{i}. {option}")

        while True:

            answer = input("Answer (1-4): ")

            if answer in ["1", "2", "3", "4"]:
                break

            print("Please enter 1, 2, 3, or 4.")

        selected = question["options"][int(answer) - 1]

        topic = question["topic"]

        if topic not in topic_results:

            topic_results[topic] = {
                "score": 0,
                "total": 0
            }

        topic_results[topic]["total"] += 1

        if selected == question["answer"]:

            print("Correct!")

            score += 1
            topic_results[topic]["score"] += 1

        else:

            print("Wrong!")
            print("Correct answer:", question["answer"])

    print(f"\nYour score: {score}/{len(QUESTIONS)}")

    return score, len(QUESTIONS), topic_results


def start_adaptive_practice(weak_topics):

    if not weak_topics:

        print("\nNo weak topics found.")

        return 0, 0, {}

    print("\n================================")
    print("    ADAPTIVE PERSONAL PRACTICE")
    print("================================")

    print("\nThe system identified these weak topics:")

    for topic in weak_topics:
        print("-", topic)

    print("\nDifficulty will automatically change")
    print("based on your answers.")

    topic_results = {}

    total_score = 0
    total_questions = 0

    for topic in weak_topics:

        if topic not in ADAPTIVE_QUESTIONS:
            continue

        difficulty = "easy"

        topic_score = 0
        topic_total = 0

        asked_questions = set()

        print("\n--------------------------------")
        print("Topic:", topic)
        print("Starting difficulty:", difficulty.upper())
        print("--------------------------------")

        for question_number in range(1, 4):

            available = [
                q
                for q in ADAPTIVE_QUESTIONS[topic][difficulty]
                if q["question"] not in asked_questions
            ]

            if not available:

                all_available = []

                for level in ["easy", "medium", "hard"]:

                    for q in ADAPTIVE_QUESTIONS[topic][level]:

                        if q["question"] not in asked_questions:
                            all_available.append(q)

                available = all_available

            if not available:
                break

            question = available[0]

            asked_questions.add(question["question"])

            print(
                f"\n{topic} - Question {question_number}"
            )

            print("Difficulty:", difficulty.upper())
            print("Question:", question["question"])

            for i, option in enumerate(question["options"], 1):

                print(f"{i}. {option}")

            while True:

                answer = input("Answer (1-4): ")

                if answer in ["1", "2", "3", "4"]:
                    break

                print("Please enter 1, 2, 3, or 4.")

            selected = question["options"][int(answer) - 1]

            topic_total += 1
            total_questions += 1

            if selected == question["answer"]:

                print("Correct!")

                topic_score += 1
                total_score += 1

                if difficulty == "easy":
                    difficulty = "medium"

                elif difficulty == "medium":
                    difficulty = "hard"

                else:
                    difficulty = "hard"

                print(
                    "Next difficulty:",
                    difficulty.upper()
                )

            else:

                print("Wrong!")
                print(
                    "Correct answer:",
                    question["answer"]
                )

                if difficulty == "hard":
                    difficulty = "medium"

                elif difficulty == "medium":
                    difficulty = "easy"

                else:
                    difficulty = "easy"

                print(
                    "Next difficulty:",
                    difficulty.upper()
                )

        topic_results[topic] = {
            "score": topic_score,
            "total": topic_total
        }

        percentage = (
            topic_score / topic_total
        ) * 100 if topic_total else 0

        print(
            f"\n{topic} adaptive result: "
            f"{topic_score}/{topic_total} "
            f"({percentage:.1f}%)"
        )

        if percentage >= 80:

            print(
                f"Good work in {topic}. "
                f"You are improving."
            )

        elif percentage >= 50:

            print(
                f"You are making progress in {topic}. "
                f"More practice will help."
            )

        else:

            print(
                f"{topic} still needs attention. "
                f"We will keep practicing this topic."
            )

    print("\n================================")
    print("     ADAPTIVE PRACTICE RESULT")
    print("================================")

    print(
        f"\nOverall score: "
        f"{total_score}/{total_questions}"
    )

    if total_questions > 0:

        percentage = (
            total_score / total_questions
        ) * 100

        print(
            f"Overall percentage: "
            f"{percentage:.1f}%"
        )

    return total_score, total_questions, topic_results
