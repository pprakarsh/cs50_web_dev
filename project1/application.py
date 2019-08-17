import os

from flask import Flask, session, request, render_template, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        
        username = request.form.get("username")
        create_password = request.form.get("create_password")
        confirm_password = request.form.get("confirm_password")
        email_id = request.form.get("emailid") 
        
        usernames = db.execute("SELECT username FROM users WHERE username= :username", {"username": username}).fetchone()
        if username == "" or create_password == "" or confirm_password == "" or email_id == "": #for checking if any data unfilled
            return render_template("error.html", error="Incomplete form! Please fill all the details.")

        elif usernames != None:   #for checking is username already exists in database
            return render_template("error.html", error="Username already taken. Please fill the form again")
        
        elif create_password != confirm_password:     #for checking if create_password and confirm password match
            return render_template("error.html", error="Passwords do not match! Please fill the form with matching passwords")

        elif '\'' in create_password or '\"' in create_password:    #for sql_injection protection
            return render_template("error.html", error="Apostrophe and quotes not allowed in password")
            
        else:
            db.execute("INSERT INTO users(username, email, password) VALUES (:username, :email, :password)", {"username": username, "email": email_id, "password": create_password})
            db.commit()
            return render_template("index.html")

    if request.method == "GET":
        return render_template("index.html")
    
@app.route("/home", methods =  ["POST"])
def home():
    username = request.form.get("username")
    password = request.form.get("password")
    
    credentials = db.execute("SELECT username, password FROM users WHERE username= :username and password= :password", {"username": username, "password": password }).rowcount!=0

    if credentials==False:
        return render_template("error.html", error="Invalid credentials. Please login again")
    else:
        session[username]="home"
        return render_template("home.html", username=username)

@app.route("/logout", methods = ["POST"])
def logout():
    username=request.form.get("username")
    del session[username]
    return redirect('/')
