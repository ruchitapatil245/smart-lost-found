from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = "items.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """)


@app.route("/")
def home():
    search = request.args.get("q", "").strip()

    with get_db() as conn:
        if search:
            items = conn.execute("""
                SELECT * FROM items
                WHERE name LIKE ? OR description LIKE ? OR location LIKE ?
                ORDER BY id DESC
            """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
        else:
            items = conn.execute(
                "SELECT * FROM items ORDER BY id DESC"
            ).fetchall()

    return render_template("index.html", items=items, search=search)


@app.route("/report", methods=["POST"])
def report():
    item_type = request.form.get("type", "")
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()

    if item_type not in ("Lost", "Found") or not all(
        [name, description, location]
    ):
        return "Please enter valid item details.", 400

    with get_db() as conn:
        conn.execute("""
            INSERT INTO items (type, name, description, location)
            VALUES (?, ?, ?, ?)
        """, (item_type, name, description, location))

    return redirect(url_for("home", _anchor="items"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
