import sqlite3


DATABASE_NAME = "worksync.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            wpm REAL,
            correction_rate REAL,
            mouse_clicks INTEGER,
            mouse_movements INTEGER,
            work_minutes REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS baseline (
            id INTEGER PRIMARY KEY,
            wpm REAL,
            correction_rate REAL,
            mouse_movements REAL
        )
    """)

    connection.commit()
    connection.close()


def save_activity(
    timestamp,
    wpm,
    correction_rate,
    mouse_clicks,
    mouse_movements,
    work_minutes
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO activity
        (timestamp, wpm, correction_rate, mouse_clicks, mouse_movements, work_minutes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        wpm,
        correction_rate,
        mouse_clicks,
        mouse_movements,
        work_minutes
    ))

    connection.commit()
    connection.close()


def get_activity_count():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM activity
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


def create_baseline():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT AVG(wpm), AVG(correction_rate), AVG(mouse_movements)
        FROM activity
        WHERE wpm > 0
    """)

    result = cursor.fetchone()

    if result[0] is None:
        connection.close()
        return None

    baseline = {
        "wpm": result[0],
        "correction_rate": result[1],
        "mouse_movements": result[2]
    }

    cursor.execute("""
        INSERT OR REPLACE INTO baseline
        (id, wpm, correction_rate, mouse_movements)
        VALUES (1, ?, ?, ?)
    """, (
        baseline["wpm"],
        baseline["correction_rate"],
        baseline["mouse_movements"]
    ))

    connection.commit()
    connection.close()

    return baseline


def get_baseline():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT wpm, correction_rate, mouse_movements
        FROM baseline
        WHERE id = 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return {
        "wpm": result[0],
        "correction_rate": result[1],
        "mouse_movements": result[2]
    }
def get_recent_activity(limit=3):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT wpm, correction_rate, mouse_movements, work_minutes
        FROM activity
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "wpm": row[0],
            "correction_rate": row[1],
            "mouse_movements": row[2],
            "work_minutes": row[3]
        }
        for row in rows
    ]
def get_activity_history(limit=50):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp, wpm, correction_rate,
               mouse_clicks, mouse_movements, work_minutes
        FROM activity
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "timestamp": row[0],
            "wpm": row[1],
            "correction_rate": row[2],
            "mouse_clicks": row[3],
            "mouse_movements": row[4],
            "work_minutes": row[5]
        }
        for row in rows
    ]

if __name__ == "__main__":

    create_database()

    print("WorkSync database created successfully.")