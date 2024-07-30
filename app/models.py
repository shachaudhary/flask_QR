from app import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def get_id(self):
        return self.id
    

class QRLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(2048), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tracking = db.Column(db.String(3), default='no')

    # visits = db.relationship('QRLinkVisit', backref='qr_link', lazy=True)
     # Relationship with QRLinkVisit
    visits = db.relationship('QRLinkVisit', backref='qr_link', cascade="all, delete-orphan")
    user = db.relationship('User', backref=db.backref('qr_links', lazy=True))

    def __repr__(self):
        return f'<QRLink {self.link}>'
    

class QRLinkVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qr_link_id = db.Column(db.Integer, db.ForeignKey('qr_link.id'), nullable=False)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # To store IP address if needed

