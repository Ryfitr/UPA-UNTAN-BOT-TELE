import sqlite3
from rapidfuzz import fuzz
from config.config import DB_PATH

def suggest_faq(user_question, threshold=75):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT keyword, response FROM faq")
        faq_entries = c.fetchall()
    finally:
        conn.close()

    suggestions = []
    for keyword, response in faq_entries:
        score = fuzz.token_sort_ratio(user_question.lower(), keyword.lower())
        if score >= threshold:
            suggestions.append((keyword, response, score))

    suggestions.sort(key=lambda x: x[2], reverse=True)
    return suggestions


def find_similar_faq(user_question, threshold=75):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT keyword, response FROM faq")
        faq_entries = c.fetchall()
    finally:
        conn.close()

    best_match = None
    highest_score = 0

    for keyword, response in faq_entries:
        score = fuzz.token_set_ratio(user_question.lower(), keyword.lower())
        if score > highest_score and score >= threshold:
            highest_score = score
            best_match = response

    return best_match  # langsung return response string atau None


def group_unanswered_questions(threshold=70):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT question FROM unanswered")
        questions = [q[0] for q in c.fetchall()]
    finally:
        conn.close()

    groups = []
    visited = set()

    for i, q1 in enumerate(questions):
        if i in visited:
            continue
        group = [q1]
        visited.add(i)
        for j, q2 in enumerate(questions):
            if j != i and j not in visited:
                score = fuzz.token_set_ratio(q1.lower(), q2.lower())
                if score >= threshold:
                    group.append(q2)
                    visited.add(j)
        if len(group) > 1:
            groups.append(group)

    return groups
