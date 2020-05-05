from flask import render_template, request, redirect, session, flash
from config import app, db, bcrypt
from models import User, Address, Post, Post_comment, Event, Event_location, Event_comment, likes_table
from datetime import date, time
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index():
    print("*"*40)
    return render_template("index2.html")

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
    if len(request.form['zipcode'])<5:
        flash("Zipcode required, 5 numbers")     
    if len(request.form['password']) < 5:
        flash("password isn't long enough")
    if request.form['password'] != request.form['cpassword']:
        flash("password dont match")
    if '_flashes' not in session:
        new_address = Address(
            address=request.form['address'], 
            city=request.form['city'],
            state = request.form['state'],
            zipcode = request.form['zipcode']) 
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
                return redirect("/dashboard")
            else:
                flash("Email and/or password do not match")
        else:
                flash("Email and/or password do not match")
    return redirect("/")

def my_profile():
    if 'user_id' not in session:
        return redirect("/")
    user = User.query.filter_by(id=session['user_id'])
    post_history = Post.query.filter_by(user_id= session['user_id'])
    event_history = Event.query.filter_by(user_id = session['user_id'])
    return render_template("my_profile.html", all_users = user, all_posts = post_history, all_events = event_history)

def delete_user(user_id):
    if 'user_id' not in session:
        return redirect("/")
    this_user = User.query.filter_by(id = int(user_id)).first()
    if this_user is not None:
        print("delete")
        db.session.delete(this_user)
        db.session.commit()
        flash("User successfully deleted")
        return redirect("/register")
    return redirect("/my_profile")


def neighbors_profile(user_id):
    if 'user_id' not in session:
        return redirect("/")
    user = User.query.filter_by(id = int(user_id)).all()
    post_history = Post.query.filter_by(user_id = int(user_id))
    event_history = Event.query.filter_by(user_id = int(user_id))
    return render_template("neighbors_profile.html", all_users = user, all_posts = post_history, all_events = event_history)

    

def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    posts = Post.query.all()
    events = Event.query.all()
    cur_user = User.query.filter_by(id=session['user_id'])
    return render_template("dashboard.html", all_posts = posts, all_events = events,all_users = cur_user )

def add_post():
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['message']) < 2:
        is_valid = False
        flash("A message is required to post")
    if is_valid:
        new_post = Post(
            message = request.form['message'],
            user_id = session['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return redirect("/dashboard")
    return redirect("/dashboard")

def add_like(post_id):
    if 'user_id' not in session:
        return redirect("/")
    post = Post.query.get(post_id)
    user = User.query.get(session['user_id'])
    post.likes_rec.append(user)
    db.session.commit()
    return redirect("/dashboard")


def post_details(post_id):
    if 'user_id' not in session:
        return redirect("/")
    post = Post.query.get(post_id)
    user = User.query.filter_by(id = post.user_id).all()
    comment = Post_comment.query.filter_by(post_id = int(post_id)).all()
    return render_template("post_details.html", post = post, all_users = user, all_comments = comment)
  
def update_post(post_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['message']) < 2:
        is_valid = False
        flash("A message is required to edit post")
    if is_valid:
        this_post = Post.query.get(post_id)
        if this_post is not None:
            this_post.message = request.form['message']
            db.session.commit()
            
        return redirect ("/post/details/{}".format(post_id))
    return redirect ("/post/details/{}".format(post_id))
       

def delete_post(post_id):
    if 'user_id' not in session:
        return redirect("/")
    print("hello?")
    this_post = Post.query.filter_by(id = int(post_id)).first()
    if this_post is not None:
        print("delete")
        db.session.delete(this_post)
        db.session.commit()
        flash("Post successfully deleted")
        return redirect("/dashboard")

def add_post_comments(post_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['message']) < 2:
        is_valid = False
        flash("A message is required to post")
    if is_valid:
        new_message = Post_comment(
            message = request.form['message'],
            user_id = session['user_id'],
            post_id = int(post_id))
        db.session.add(new_message)
        db.session.commit() 
        return redirect ("/post/details/{}".format(post_id))
    return redirect("/dashboard")          


def events():
    if 'user_id' not in session:
        return redirect("/")
    events = Event.query.all()
    return render_template("add_event.html", all_events = events)

def add_event():
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['title']) < 1:
        is_valid = False
        flash("Event title is required")
    if len(request.form['description']) < 1:
        is_valid = False
        flash("Description is required")
    if len(request.form['date']) < 1:
        is_valid = False
        flash("Date is required")
    if len(request.form['time']) < 1:
        is_valid = False
        flash("Time is required")
    if len(request.form['address']) < 1:
        is_valid = False
        flash("Location address is required")
    if len(request.form['city']) < 1:
        is_valid = False
        flash("city is required")
    if len(request.form['state']) < 1:
        is_valid = False
        flash("State initials are required")
    if len(request.form['zipcode']) < 1:
        is_valid = False
        flash("Zipcode is required")
    if is_valid:
        new_location = Event_location(
            address = request.form['address'],
            city = request.form['city'],
            zipcode = request.form['zipcode'])
        db.session.add(new_location)
        db.session.commit()               
        new_event = Event(
            title = request.form['title'],
            description = request.form['description'],
            date = request.form['date'],
            time = request.form['time'],
            user_id = session['user_id'],
            location_id = new_location.id)
        db.session.add(new_event)
        db.session.commit()
        flash("Successfully added Event!")
        return redirect("/events")
    return redirect("/events")


def delete_event(event_id):
    if 'user_id' not in session:
        return redirect("/")
    this_event = Event.query.filter_by(id = int(event_id)).first()
    if this_event is not None:
        db.session.delete(this_event)
        db.session.commit()
        flash("Event successfully deleted")
        return redirect("/dashboard")
    return redirect("/dashboard")


# def edit_event(event_id):
#     if 'user_id' not in session:
#         return redirect("/")
#     this_event = Event.query.filter_by(id = int(event_id)).all()
#     return render_template("edit_event.html", all_events = this_event)

def update_event(event_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['title']) < 1:
        is_valid = False
        flash("Event title is required")
    if len(request.form['description']) < 1:
        is_valid = False
        flash("Description is required")
    if len(request.form['date']) < 1:
        is_valid = False
        flash("Date is required")
    if len(request.form['time']) < 1:
        is_valid = False
        flash("Time is required")
    if is_valid:
        this_event = Event.query.filter_by(id = int(event_id)).first()
        if this_event is not None:
            this_event.title = request.form['title']
            this_event.description = request.form['description']
            this_event.date = request.form['date']
            this_event.time = request.form['time']
            db.session.commit()
            return redirect("/dashboard")
        return redirect("/edit/event/{}".format(event_id))
    return redirect ("/edit/event/{}".format(event_id))

def event_details(event_id):
    if 'user_id' not in session:
        return redirect("/")
    this_event = Event.query.filter_by(id = int(event_id)).all()
    comment = Event_comment.query.filter_by(event_id = int(event_id)).all()
    return render_template("event_details.html", all_events = this_event, all_comments = comment)

def add_event_comments(event_id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    if len(request.form['message']) < 2:
        is_valid = False
        flash("A message is required to post")
    if is_valid:
        new_message = Event_comment(
            message = request.form['message'],
            user_id = session['user_id'],
            event_id = int(event_id))
        db.session.add(new_message)
        db.session.commit() 
        return redirect("/event/details/{}".format(event_id))
    return redirect("/event/details/{}".format(event_id))          



def logout():
    session.clear()
    return redirect("/")



