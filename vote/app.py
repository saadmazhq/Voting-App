import os
from flask import Flask, render_template, request, redirect
import redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=redis_host, port=redis_port, db=0)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/vote", methods=["POST"])
def vote():
    choice = request.form.get("vote")
    if choice not in ("YES", "NO"):
        return redirect("/")
    # Push vote to Redis list/queue
    r.lpush("votes", choice)
    # Redirect back with a simple confirmation via query param (optional)
    return redirect("/?voted=" + choice)