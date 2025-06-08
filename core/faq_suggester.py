import sqlite3
from rapidfuzz import fuzz
from config.config import DB_PATH

def suggest_faq(question):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT question, answer FROM faq")
    faq_entries = c.fetchall()
    conn.close()
    suggestions = []
    for q, a in faq_entries:
        score = fuzz.token_sort_ratio(question.lower(), q.lower())
        if score > 75:
            suggestions.append((q, a, score))
    suggestions.sort(key=lambda x: x[2], reverse=True)
    return suggestions

def find_similar_faq(user_question, threshold=75):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT question, answer FROM faq")
    faq_entries = c.fetchall()
    conn.close()
    best_match = None
    highest_score = 0
    for question, answer in faq_entries:
        score = fuzz.token_set_ratio(user_question.lower(), question.lower())
        if score > highest_score and score >= threshold:
            highest_score = score
            best_match = (question, answer)
    return best_match

def group_unanswered_questions(threshold=70):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT question FROM unanswered")
    questions = [q[0] for q in c.fetchall()]
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
