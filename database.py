
import sqlite3

DB_NAME = "career_agent.db"


def create_database():
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS solved_questions (
                question_id TEXT PRIMARY KEY,
                question_title TEXT NOT NULL,
                topic TEXT NOT NULL,
                solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS study_plans (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                target_date TEXT NOT NULL,
                daily_hours REAL NOT NULL,
                topics TEXT NOT NULL
            )
        """)


def save_solved_question(question_id, title, topic):
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            INSERT OR IGNORE INTO solved_questions
            (question_id, question_title, topic)
            VALUES (?, ?, ?)
        """, (question_id, title, topic))


def get_solved_questions():
    with sqlite3.connect(DB_NAME) as connection:
        return connection.execute("""
            SELECT question_id, question_title, topic, solved_at
            FROM solved_questions
            ORDER BY solved_at DESC
        """).fetchall()


def save_study_plan(target_date, daily_hours, topics):
    with sqlite3.connect(DB_NAME) as connection:
        connection.execute("""
            INSERT OR REPLACE INTO study_plans
            (id, target_date, daily_hours, topics)
            VALUES (1, ?, ?, ?)
        """, (target_date, daily_hours, "|".join(topics)))


def get_study_plan():
    with sqlite3.connect(DB_NAME) as connection:
        return connection.execute("""
            SELECT target_date, daily_hours, topics
            FROM study_plans
            WHERE id = 1
        """).fetchone()
