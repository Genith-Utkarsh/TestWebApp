from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///asep.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"  # Used for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


# Home page
@app.route("/")
def home_page():
   # if "username" in session:
       # return redirect(url_for("index_page"))  # Redirect to index if logged in
    return redirect(url_for("login_page"))


# Login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("index_page"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("login_page"))

    return render_template("login.html")


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register_page"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("register_page"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login_page"))

    return render_template("register.html")


# Logout route
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login_page"))


# Index page
@app.route("/index")
def index_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    username = session["username"]
    return render_template("index.html", username=username)


# Engine page
@app.route("/engine")
def engine_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    return render_template("engine.html")


# Brake page
@app.route("/brake")
def brake_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    return render_template("brake.html")


# Transmission page
@app.route("/trans")
def transmission_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    return render_template("trans.html")


# profile page
@app.route("/profile")
def profile_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    return render_template("profile.html")


@app.route("/success")
def success_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    return render_template("success.html")



# Query page
@app.route("/query")
def query_page():
    if "username" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login_page"))
    return render_template("query.html")


# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)


    from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(_name_)
app.secret_key = 'Asepgroup@03'

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Update if using a different provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'backendrunner2@gmail.com'
app.config['MAIL_PASSWORD'] = 'Asepgroup@03'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('http://127.0.0.1:5000/query')

@app.route('http://127.0.0.1:5000/success', methods=['POST'])
def submit_query():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send the email
        try:
            msg = Message("New Query Received",
                          sender="backendrunner2@gmail.com",
                          recipients=["backendrunner2@gmail.com"])
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash("Query submitted successfully! We'll get back to you soon.", "success")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for('index'))

if _name_ == '_main_':
    app.run(debug=True)




