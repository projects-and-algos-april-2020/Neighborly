from config import db
from sqlalchemy.sql import func
from datetime import date, time

likes_table = db.Table('likes', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True), 
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='cascade'), primary_key=True))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(255))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete='cascade'))
    address = db.relationship('Address', foreign_keys=[address_id])
    password_hash=db.Column(db.String(255))
    likes_sent = db.relationship('Post', secondary=likes_table, passive_deletes=True)
    all_post = db.relationship('Post', back_populates="user", cascade="all, delete, delete-orphan")
    all_event = db.relationship('Event', back_populates="user", cascade="all, delete, delete-orphan")
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Address(db.Model):
    __tablename__ = "addresses" 
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())
    
    def full_address(self):
        return self.address + ' ' + self.city

class Post(db.Model):
    __tablename__ = "posts" 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', foreign_keys=[user_id])
    likes_rec = db.relationship('User', secondary=likes_table, passive_deletes=True)
    all_post = db.relationship('Post_comment', back_populates="post", cascade="all, delete, delete-orphan")
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

    @property
    def num_likes(self):
        return len(self.likes_rec)

class Post_comment(db.Model):
    __tablename__ = "post_comments" 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'))
    post = db.relationship('Post', foreign_keys=[post_id])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', foreign_keys=[user_id])
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())


class Event(db.Model):
    __tablename__ = "events" 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    date = db.Column(db.String(45))
    time = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', foreign_keys=[user_id])
    location_id = db.Column(db.Integer, db.ForeignKey('event_locations.id', ondelete='cascade'))
    location = db.relationship('Event_location', foreign_keys=[location_id])
    all_comment = db.relationship('Event_comment', back_populates="event", cascade="all, delete, delete-orphan")
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

class Event_location(db.Model):
    __tablename__ = "event_locations" 
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    zipcode = db.Column(db.String(30))
    state = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

class Event_comment(db.Model):
    __tablename__ = "event_comments" 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='cascade'))
    event = db.relationship('Event', foreign_keys=[event_id])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    user = db.relationship('User', foreign_keys=[user_id])
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

