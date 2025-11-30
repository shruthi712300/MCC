from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Membership(db.Model):
    __tablename__ = 'memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    # Personal Particulars
    full_name = db.Column(db.String(200), nullable=False)
    mykad_no = db.Column(db.String(20), nullable=False, unique=True)
    home_address = db.Column(db.Text, nullable=False)
    office_address = db.Column(db.Text)
    phone_home = db.Column(db.String(20))
    phone_office = db.Column(db.String(20))
    hp_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    political_party = db.Column(db.String(200))
    
    # Membership Details
    membership_type = db.Column(db.String(50), nullable=False)
    years = db.Column(db.Integer, nullable=False, default=1)
    amount_paid = db.Column(db.Float, nullable=False)
    
    # Proposer & Seconder
    proposer_name = db.Column(db.String(200), nullable=False)
    proposer_mykad = db.Column(db.String(20), nullable=False)
    seconder_name = db.Column(db.String(200), nullable=False)
    seconder_mykad = db.Column(db.String(20), nullable=False)
    
    # Declaration
    application_date = db.Column(db.Date, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'mykad_no': self.mykad_no,
            'home_address': self.home_address,
            'office_address': self.office_address,
            'phone_home': self.phone_home,
            'phone_office': self.phone_office,
            'hp_no': self.hp_no,
            'email': self.email,
            'political_party': self.political_party,
            'membership_type': self.membership_type,
            'years': self.years,
            'amount_paid': self.amount_paid,
            'proposer_name': self.proposer_name,
            'proposer_mykad': self.proposer_mykad,
            'seconder_name': self.seconder_name,
            'seconder_mykad': self.seconder_mykad,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'status': self.status
        }

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'is_read': self.is_read
        }

class NewsletterSubscriber(db.Model):
    __tablename__ = 'newsletter_subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(100), nullable=False, unique=True)
    subscription_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subscription_date': self.subscription_date.isoformat() if self.submission_date else None,
            'is_active': self.is_active
        }

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string of skills/interests
    availability = db.Column(db.String(100))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'skills': json.loads(self.skills) if self.skills else [],
            'availability': self.availability,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'status': self.status
        }

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'department': self.department,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'bio': self.bio,
            'image_url': self.image_url,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }