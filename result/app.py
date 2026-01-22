import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

db_host = os.getenv("POSTGRES_HOST", "db")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "postgres")
db_name = os.getenv("POSTGRES_DB", "votes")

def get_results():
    conn = psycopg2.connect(
        host=db_host, port=db_port,
        user=db_user, password=db_password,
        dbname=db_name
    )
    cur = conn.cursor()
    cur.execute("SELECT yes_count, no_count FROM vote_totals WHERE id = TRUE;")
    yes_count, no_count = cur.fetchone()
    conn.close()

    total = yes_count + no_count
    yes_pct = (yes_count / total * 100) if total > 0 else 0
    no_pct = (no_count / total * 100) if total > 0 else 0
    return yes_pct, no_pct

@app.route("/")
def index():
    yes_pct, no_pct = get_results()
    return render_template("result.html", yes=yes_pct, no=no_pct)