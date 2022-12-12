from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .database_models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# email küldéshez
import smtplib
import ssl


authentications = Blueprint("authentications", __name__)


# Regisztráció
@authentications.route("/sign-up", methods=["GET", "POST"])
def signup():
    # email küldéshez váltózók
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "bigfourforuminfo@gmail.com"
    sender_password = "mgxtlvvsnqqtgyjm"
    subject = "BigFour forum account"
    #

    if request.method == "POST":
        email_signup = request.form.get("signUpEmailInput")
        username_signup = request.form.get("signUpUsernameInput")
        password_signup = request.form.get("signUpPasswordInput")
        confirm_password_signup = request.form.get(
            "signUpConfirmPasswordInput")
        bio_signup = request.form.get("signUpBioTextArea")
        nfl_signup = request.form.get("signUpNflSelect")
        nba_signup = request.form.get("signUpNbaSelect")
        mlb_signup = request.form.get("signUpMlbSelect")
        nhl_signup = request.form.get("signUpNhlSelect")

        email_exists = User.query.filter_by(email=email_signup).first()
        username_exists = User.query.filter_by(
            username=username_signup).first()
        passwords_match = password_signup == confirm_password_signup
        if email_exists:
            flash("Email is already in use.", category="error")
        elif username_exists:
            flash("Username is already in use.", category="error")
        elif not passwords_match:
            flash("Passwords don't match.", category="error")
        elif len(username_signup) < 4:
            flash("Username is too short.", category="error")
        elif len(password_signup) < 6:
            flash("Password is too short.", category="error")
        elif len(email_signup) < 4:
            flash("Email is invalid.", category="error")
        else:
            new_user = User(
                email=email_signup,
                username=username_signup,
                password=generate_password_hash(
                    password_signup, method="sha256"),
                bio=bio_signup,
                nfl=nfl_signup,
                nba=nba_signup,
                mlb=mlb_signup,
                nhl=nhl_signup)
            db.session.add(new_user)
            db.session.commit()

            # email küldés
            message_body = f"""
                You have successfully registered to the BigFour forum.
                In order to seamlessly use the site in the future, please keep this email.
                
                Your account credentials are below.
                Email: {email_signup}
                Username: {username_signup}
                """
            message_complete = "Subject: {}\n\n{}".format(
                subject, message_body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_signup, message_complete)
            # email küldés vége

            login_user(new_user, remember=True)
            flash("New user created! You got a confirmation email as well (please check spam too).", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user_active=current_user)


# Bejelentkezés
@authentications.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_login = request.form.get("loginEmailInput")
        password_login = request.form.get("loginPasswordInput")

        user_exists = User.query.filter_by(email=email_login).first()
        if user_exists:
            if check_password_hash(user_exists.password, password_login):
                flash("Logged in!", category="success")
                login_user(user_exists, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user_active=current_user)


# Kijelentkezés
@authentications.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("views.home"))
