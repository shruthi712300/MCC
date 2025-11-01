from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    # All users are admins in this project
    is_branch_admin = db.Column(db.Boolean, default=True)  # Changed to True
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_branch_admin': self.is_branch_admin,
            'branch_id': self.branch_id
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(500))  # Store tags as comma-separated string
    
    # UPDATED: Add all media fields
    image_filename = db.Column(db.String(255))
    video_filename = db.Column(db.String(255))
    audio_filename = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'username': self.author.username,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'tags': self.tags.split(',') if self.tags else [],
            # UPDATED: Include all media filenames in post data
            'image_filename': self.image_filename,
            'video_filename': self.video_filename,
            'audio_filename': self.audio_filename
        }

class MembershipApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    mykad_no = db.Column(db.String(20), nullable=False)
    home_address = db.Column(db.Text, nullable=False)
    office_address = db.Column(db.Text)
    phone_home = db.Column(db.String(20))
    phone_office = db.Column(db.String(20))
    hp_no = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255))
    political_party = db.Column(db.String(255))
    membership_type = db.Column(db.String(50), nullable=False)
    years = db.Column(db.Integer, nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    proposer_name = db.Column(db.String(255), nullable=False)
    proposer_mykad = db.Column(db.String(20), nullable=False)
    seconder_name = db.Column(db.String(255), nullable=False)
    seconder_mykad = db.Column(db.String(20), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

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
            'amount_paid': float(self.amount_paid) if self.amount_paid else 0,
            'proposer_name': self.proposer_name,
            'proposer_mykad': self.proposer_mykad,
            'seconder_name': self.seconder_name,
            'seconder_mykad': self.seconder_mykad,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'status': self.status,
            'branch_id': self.branch_id
        }

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    members = db.relationship('User', backref='branch', lazy=True)
    applications = db.relationship('MembershipApplication', backref='branch', lazy=True)
    activities = db.relationship('BranchActivity', backref='branch', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'address': self.address,
            'contact_number': self.contact_number,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'member_count': len(self.members),
            'admin_count': len([user for user in self.members if getattr(user, 'is_branch_admin', True)])
        }

class BranchActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    activity_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_archived = db.Column(db.Boolean, default=False)
    
    # Relationship
    creator = db.relationship('User', backref='activities_created')

    def to_dict(self):
        return {
            'id': self.id,
            'branch_id': self.branch_id,
            'branch_name': self.branch.name if self.branch else 'Unknown',
            'title': self.title,
            'description': self.description,
            'activity_date': self.activity_date.isoformat() if self.activity_date else None,
            'location': self.location,
            'is_archived': self.is_archived,
            'created_by': self.created_by,
            'created_by_name': self.creator.username if self.creator else 'Unknown',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# NEW: Logo Model
class Logo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    
    # Relationship
    uploader = db.relationship('User', backref='logos_uploaded')

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.username if self.uploader else 'Unknown',
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'is_active': self.is_active,
            'file_url': f"/static/uploads/{self.filename}" if self.filename else None
        }

# NEW: News Model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'image_filename': self.image_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

# NEW: Documents Model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    document_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'document_filename': self.document_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

# NEW: Gallery Image Model
class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship
    uploader = db.relationship('User', backref='gallery_images')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_filename': self.image_filename,
            'uploaded_by': self.uploaded_by,
            'uploader_name': self.uploader.username if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }