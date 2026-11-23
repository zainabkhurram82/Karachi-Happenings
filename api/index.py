from flask import Flask, render_template, request, redirect, session
import os
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "karachi123"

events = [
    {"id":1, "title":"Karachi Food Festival", "area":"Clifton", "category":"Food", "date":"2026-11-29", "desc":"Best food stalls of Karachi"},
    {"id":2, "title":"Tech Meetup Karachi", "area":"Gulshan", "category":"Tech", "date":"2026-12-05", "desc":"Meet developers & startups"},
    {"id":3, "title":"Coke Fest Music Night", "area":"DHA", "category":"Music", "date":"2026-12-12", "desc":"Live music night"},
]

@app.route("/")
def home():
    search = request.args.get("search","").lower()
    area = request.args.get("area","")
    cat = request.args.get("category","")
    filtered = events
    if search:
        filtered = [e for e in filtered if search in e["title"].lower()]
    if area:
        filtered = [e for e in filtered if e["area"]==area]
    if cat:
        filtered = [e for e in filtered if e["category"]==cat]
    return render_template("index.html", events=filtered)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        session["user"]=request.form["email"]
        return redirect("/")
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method=="POST":
        session["user"]=request.form["email"]
        return redirect("/")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

@app.route("/add", methods=["GET","POST"])
def add():
    if "user" not in session:
        return redirect("/login")
    if request.method=="POST":
        new_id = len(events)+1
        events.append({"id":new_id, "title":request.form["title"], "area":request.form["area"], "category":request.form["category"], "date":request.form["date"], "desc":request.form["desc"]})
        return redirect("/")
    return render_template("add_event.html")
