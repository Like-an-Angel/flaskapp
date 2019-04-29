from app.auth import auth
from flask import render_template, redirect, url_for, flash, request
from app.auth.forms import (RegistrationForm, LoginForm, UpdateAccount,
                            ResetRequestForm, ResetPasswordForm)
from app import bcrypt, db
from app.auth.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.auth.utils import save_picture, send_reset_email

@auth.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        flash("You have already logged in","warning")
        return redirect(url_for('posts.home'))

    form = RegistrationForm() # instatiating a form
    if form.validate_on_submit():
        username = form.username.data # datafiled from the username attribute
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        print(username, "has registered :3")
        flash("Cool, you're done, {}!".format(username), "success") # success is for color category name
        return redirect(url_for('auth.login')) # here name of the function

    return render_template("register.html", reg_form=form)

@auth.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        flash("You have already logged in","warning")
        return redirect(url_for('posts.home'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        password = login_form.password.data
        email = login_form.email.data
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=login_form.remember.data)
            print("Account", email, "has logged in :3")
            flash("You're logged in, {}!".format(email), "success")
            next_page = request.args.get('next') # .get returns same as ['next'] but .get handles missing key -> returns None
            return redirect(next_page) if next_page else redirect(url_for('posts.home'))
            # if next_page:
            #     # print(next_page)
            #     return redirect(next_page) # here name of the function
            # else:
            #     return redirect(url_for('posts.home'))
    return render_template("login.html", login_form=login_form)

@auth.route("/logout")
def sign_out():
    logout_user()
    flash("Succesfully logged out", "success")
    return redirect(url_for('posts.home'))

@auth.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccount()
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data  = current_user.email
    # print(form.validate_on_submit())
    # flash(form.errors, "warning")
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        pic_data = form.avatar.data
        if pic_data:
            profile_picture = save_picture(pic_data)
            current_user.avatar = profile_picture
        db.session.commit()
        flash("Account has been updated", "success")
        return redirect(url_for("auth.account"))
    # if not current_user.is_authenticated:
    #     flash("You are not logged in","warning")
    #     return redirect(url_for('posts.home'))
    return render_template("account.html", form=form)

@auth.route("/reset-request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("posts.home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email with reset password instructions is sent", "info")
        return redirect(url_for("auth.login"))
    return render_template("reset_request.html", form=form)

@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token): # argument from url is passed to function
    if current_user.is_authenticated:
        return redirect(url_for("posts.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("The link has been expired. Make a new request", "warning")
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Password has been successfully changed", "success")
        return redirect(url_for('auth.login'))
    return render_template("reset_password.html", form=form)
