from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


def init_db():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_hash TEXT UNIQUE,
            choice TEXT,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def home():
    return "Backend is running successfully"



@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    choice = data.get("choice")
    device_hash = data.get("device_hash")

    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM votes WHERE device_hash = ?",
        (device_hash,)
    )

    if cursor.fetchone():
        conn.close()
        return jsonify({"message": "You have already voted"}), 403

    cursor.execute(
        "INSERT INTO votes (device_hash, choice) VALUES (?, ?)",
        (device_hash, choice)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Vote saved successfully"})


if __name__ == '__main__':
    app.run(debug=True)
