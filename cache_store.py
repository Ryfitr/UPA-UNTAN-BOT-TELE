import sqlite3

def cache_user_question_answer(user_id, question, answer):
    conn = sqlite3.connect("database/bot_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO conversations (user_id, question, answer) VALUES (?, ?, ?)", 
              (str(user_id), question, answer))
    conn.commit()
    conn.close()
