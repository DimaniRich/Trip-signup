import hmac
import os
import sqlite3

from flask import Flask, Response, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["DATABASE"] = "signups.db"
app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD")


def get_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute(
        "CREATE TABLE IF NOT EXISTS signups ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, email TEXT NOT NULL, major TEXT NOT NULL)"
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        major = request.form.get("major", "").strip()
        if not (name and email and major):
            return render_template("signup.html", error="All fields are required."), 400
        conn = get_db()
        with conn:  # commits the transaction
            conn.execute(
                "INSERT INTO signups (name, email, major) VALUES (?, ?, ?)",
                (name, email, major),
            )
        conn.close()
        return redirect(url_for("thanks", name=name))
    return render_template("signup.html")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html", name=request.args.get("name", ""))


@app.route("/admin")
def admin():
    expected = app.config["ADMIN_PASSWORD"]
    given = request.authorization.password if request.authorization else None
    # No password configured means the page stays locked.
    if not expected or not given or not hmac.compare_digest(given, expected):
        return Response(
            "Login required.", 401, {"WWW-Authenticate": 'Basic realm="Admin"'}
        )
    conn = get_db()
    signups = conn.execute("SELECT name, email, major FROM signups ORDER BY id").fetchall()
    conn.close()
    return render_template("admin.html", signups=signups)


if __name__ == "__main__":
    app.run(debug=True)
