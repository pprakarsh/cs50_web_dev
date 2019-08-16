import os

from flask import Flask, session, request, render_template
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
        
        usernames = db.execute("SELECT username FROM users").fetchall()
        temp_username = "('"+ username +"',)"
        if username == None or create_password == None or confirm_password == None or email_id == None: #for checking if any data unfilled
            return render_template("error.html", error="Incomplete form! Please fill all the details.")

        elif temp_username in usernames:  #for checking is username already exists in database
            return render_template("temp_error.html", error=usernames) 
            return render_template("error.html", error="Username already taken please enter a different username")
        
        elif create_password != confirm_password:     #for checking if create_password and confirm password match
            return render_template("error.html", error="Passwords do not match! Please fill the form with matching passwords")

        elif '\'' in create_password or '\"' in create_password:    #for sql_injection protection
            return render_template("error.html", error="Apostrophe and quotes not allowed in password")
            
        else:
#            db.execute("INSERT INTO users(username, email, password) VALUES (:username, :password, :email)", {"username": username, "password": create_password, "email": email_id})
#            db.commit()
#            return render_template("index.html")
            return render_template("temp_error.html", error=usernames) 
    if request.method == "GET":
        return render_template("index.html")
    
@app.route("/home", methods =  ["POST"])
def home():
    return "Hello, welcome to home"
