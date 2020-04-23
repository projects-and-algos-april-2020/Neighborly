from flask import render_template, request, redirect, session, flash
from config import app, db, bcrypt
from models import User, Address, Post, Post_comments, Event, Event_location, Event_comments, likes_table
from datetime import date, time
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index():
    print("*"*40)
    return render_template("index.html")

def register():
    return render_template("register.html")

def add_user():
    if len(request.form['fname'])<2:
        flash("First name is required")
    if len(request.form['lname'])<2:
        flash("Last name is required")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Valid email is required")   
    if len(request.form['address'])<2:
        flash("Address is required")
    if len(request.form['city'])<2:
        flash("City must be at least 2 characters")
    if len(request.form['state'])<2:
        flash("State initials required, 2 characters")   
    if len(request.form['password']) < 5:
        flash("password isn't long enough")
    if request.form['password'] != request.form['cpassword']:
        flash("password dont match")
    if '_flashes' not in session:
        new_address = Address(
            address=request.form['address'], 
            city=request.form['city'],
            state = request.form['state']) 
        db.session.add(new_address)
        db.session.commit()
        new_user = User(
            address_id = new_address.id,
            first_name = request.form['fname'],
            last_name = request.form['lname'],
            email = request.form['email'],
            password_hash=bcrypt.generate_password_hash(request.form['password']))   
        db.session.add(new_user)
        db.session.commit()
        flash("Successfull!")
        flash("Please log in")
        return redirect("/")
    return redirect('/register')   
        

def login():
    is_valid = True
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Email is required")
    if len(request.form['password']) < 1:
        is_valid = False
        flash("Password is required")

    if is_valid:
        user = User.query.filter_by(email=request.form['email']).all()
        if user:
            if bcrypt.check_password_hash(user[0].password_hash, request.form['password']):
                session['user_id'] = user[0].id
                return redirect("/user_profile")
            else:
                flash("Email and/or password do not match")
        else:
                flash("Email and/or password do not match")
    return redirect("/")


def user_profile():
    if 'user_id' not in session:
        return redirect("/")
    cur_user = User.query.filter_by(id=session['user_id'])
    post_history = Post.query.filter_by(user_id= session['user_id'])
    event_history = Event.query.filter_by(user_id = session['user_id'])
    return render_template("user_profile.html", all_users = cur_user, all_posts = post_history, all_events = event_history)

def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    posts = Post.query.all()
    return render_template("dashboard.html", all_posts = posts)

def add_post():
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['message']) < 1:
        is_valid = False
        flash("message is required to post")
    if is_valid:
        new_post = Post(
            message = request.form['message'],
            user_id = session['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return redirect("/dashboard")
    return redirect("/dashboard")



def logout():
    session.clear()
    return redirect("/")



