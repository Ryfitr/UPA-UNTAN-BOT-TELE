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