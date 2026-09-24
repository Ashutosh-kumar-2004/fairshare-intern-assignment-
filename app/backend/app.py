import os
import sqlite3
import pickle
import base64
import hashlib
import random
import subprocess

import yaml
import requests
from flask import Flask, request, render_template_string, redirect, session, send_file

app = Flask(__name__)
app.secret_key = "supersecret123"

DB_PASSWORD = "admin123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

UPLOAD_DIR = "uploads"


def get_db():
    return sqlite3.connect("users.db")


def init_db():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)")
    conn.execute("INSERT INTO users (username, password, email) VALUES ('admin', '" + hashlib.md5(b"admin").hexdigest() + "', 'admin@example.com')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return "Welcome to the test app"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    hashed = hashlib.md5(password.encode()).hexdigest()
    conn = get_db()
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + hashed + "'"
    user = conn.execute(query).fetchone()
    if user:
        session["user"] = username
        return redirect("/dashboard")
    return "Invalid credentials", 401


@app.route("/search")
def search():
    q = request.args.get("q", "")
    template = "<h1>Results for: " + q + "</h1>"
    return render_template_string(template)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    output = os.popen("ping -c 1 " + host).read()
    return "<pre>" + output + "</pre>"


@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd")
    result = subprocess.check_output(cmd, shell=True)
    return result


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    return str(eval(expr))


@app.route("/read")
def read_file():
    filename = request.args.get("file")
    with open("files/" + filename) as f:
        return f.read()


@app.route("/download")
def download():
    return send_file(request.args.get("path"))


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return "Uploaded " + f.filename


@app.route("/load", methods=["POST"])
def load_session():
    data = request.form["data"]
    obj = pickle.loads(base64.b64decode(data))
    return str(obj)


@app.route("/config", methods=["POST"])
def load_config():
    config = yaml.load(request.data)
    return str(config)


@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    r = requests.get(url, verify=False)
    return r.text


@app.route("/redirect")
def open_redirect():
    return redirect(request.args.get("next"))


@app.route("/user/<user_id>")
def get_user(user_id):
    conn = get_db()
    user = conn.execute(f"SELECT id, username, email FROM users WHERE id = {user_id}").fetchone()
    return str(user)


@app.route("/reset-token")
def reset_token():
    token = str(random.randint(100000, 999999))
    return token


@app.route("/dashboard")
def dashboard():
    try:
        return "Hello " + session["user"]
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
