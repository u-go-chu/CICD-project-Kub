import os, time
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "appdb"),
        user=os.environ.get("DB_USER", "appuser"),
        password=os.environ["DB_PASSWORD"],    )

def init_db():
    for _ in range(10):
        try:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name TEXT, colour TEXT, quantity INT)""")
            return
        except psycopg2.OperationalError:
            time.sleep(2)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO items (name, colour, quantity) VALUES (%s, %s, %s)",
                (request.form["name"], request.form["colour"], request.form["quantity"]),
            )
        return redirect("/")
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT name, colour, quantity FROM items ORDER BY id")
        items = [{"name": n, "colour": c, "quantity": q} for n, c, q in cur.fetchall()]
    return render_template("index.html", items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)