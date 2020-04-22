from config import db
from sqlalchemy.sql import func
from datetime import date, time



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(255))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete='cascade'))
    address = db.relationship('Address', foreign_keys=[address_id])
    password_hash=db.Column(db.String(255))
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
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())
    
    def full_address(self):
        return self.address + ' ' + self.city



