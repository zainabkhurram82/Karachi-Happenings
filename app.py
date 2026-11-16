from flask import Flask, render_template, request, redirect, session

app = Flask(__name__, template_folder='.', static_folder='.')
app.secret_key = "karachi123"
# Simple users storage - no database needed
users = {"admin": {"name": "Admin", "password": "1234"}}
events = [
    {"id": 1, "title": "Coke Fest Karachi", "category": "Music", "area": "Clifton", "date": "2026-11-20", "venue": "Beach Park", "price": "500", "description": "Live music and food festival."},
    {"id": 2, "title": "Tech Meetup", "category": "Tech", "area": "Gulshan", "date": "2026-11-22", "venue": "IBA City Campus", "price": "Free", "description": "Meet developers and startups."},
    {"id": 3, "title": "Food Street Night", "category": "Food", "area": "Burns Road", "date": "2026-11-25", "venue": "Burns Road", "price": "Free", "description": "Best street food in Karachi."},
]
next_id = 4

@app.route("/")
def home():
    return render_template("index.html", events=events)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["name"] = users[username]["name"]
            return redirect("/")
        return render_template("login.html", error="Wrong username or password")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            return render_template("signup.html", error="Username already taken, try another one")
        users[username] = {"name": name, "password": password}
        session["user"] = username
        session["name"] = name
        return redirect("/")
    return render_template("signup.html")
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
def add():
    global next_id
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        events.append({"id": next_id, "title": request.form["title"], "category": request.form["category"], "area": request.form["area"], "date": request.form["date"], "venue": request.form["venue"], "price": request.form["price"], "description": request.form["description"]})
        next_id += 1
        return redirect("/")
    return render_template("add_event.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user" not in session:
        return redirect("/login")
    event = next(e for e in events if e["id"] == id)
    if request.method == "POST":
        event.update({"title": request.form["title"], "category": request.form["category"], "area": request.form["area"], "date": request.form["date"], "venue": request.form["venue"], "price": request.form["price"], "description": request.form["description"]})
        return redirect("/")
    return render_template("edit_event.html", event=event)

if __name__ == "__main__":
    app.run(debug=True)
