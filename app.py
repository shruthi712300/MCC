from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import json
import os

from models import db, Membership, ContactMessage, NewsletterSubscriber, Volunteer, TeamMember

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mcc_website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Routes
@app.route('/api/membership/submit', methods=['POST', 'OPTIONS'])
def submit_membership():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'mykad_no', 'home_address', 'hp_no', 
                          'membership_type', 'proposer_name', 'proposer_mykad',
                          'seconder_name', 'seconder_mykad', 'application_date']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Check if MyKad already exists
        existing_member = Membership.query.filter_by(mykad_no=data['mykad_no']).first()
        if existing_member:
            return jsonify({
                'success': False,
                'message': 'A membership application with this MyKad number already exists.'
            }), 400
        
        # Create new membership application
        membership = Membership(
            full_name=data['full_name'],
            mykad_no=data['mykad_no'],
            home_address=data['home_address'],
            office_address=data.get('office_address', ''),
            phone_home=data.get('phone_home', ''),
            phone_office=data.get('phone_office', ''),
            hp_no=data['hp_no'],
            email=data.get('email', ''),
            political_party=data.get('political_party', ''),
            membership_type=data['membership_type'],
            years=data.get('years', 1),
            amount_paid=data.get('amount_paid', 0),
            proposer_name=data['proposer_name'],
            proposer_mykad=data['proposer_mykad'],
            seconder_name=data['seconder_name'],
            seconder_mykad=data['seconder_mykad'],
            application_date=datetime.strptime(data['application_date'], '%Y-%m-%d').date()
        )
        
        db.session.add(membership)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Membership application submitted successfully!',
            'application_id': membership.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting application: {str(e)}'
        }), 500

# Team Management Routes
@app.route('/api/team/members', methods=['GET'])
def get_team_members():
    try:
        members = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.display_order).all()
        return jsonify({
            'success': True,
            'team_members': [member.to_dict() for member in members]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching team members: {str(e)}'
        }), 500

@app.route('/api/team/members', methods=['POST'])
def create_team_member():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'position']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new team member
        team_member = TeamMember(
            name=data['name'],
            position=data['position'],
            department=data.get('department', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            bio=data.get('bio', ''),
            image_url=data.get('image_url', ''),
            display_order=data.get('display_order', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(team_member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Team member created successfully!',
            'team_member': team_member.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating team member: {str(e)}'
        }), 500

@app.route('/api/team/members/<int:member_id>', methods=['GET'])
def get_team_member(member_id):
    try:
        member = TeamMember.query.get_or_404(member_id)
        return jsonify({
            'success': True,
            'team_member': member.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching team member: {str(e)}'
        }), 500

@app.route('/api/team/members/<int:member_id>', methods=['PUT'])
def update_team_member(member_id):
    try:
        data = request.get_json()
        member = TeamMember.query.get_or_404(member_id)
        
        # Update fields
        updatable_fields = ['name', 'position', 'department', 'email', 'phone', 
                           'address', 'bio', 'image_url', 'display_order', 'is_active']
        
        for field in updatable_fields:
            if field in data:
                setattr(member, field, data[field])
        
        member.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Team member updated successfully!',
            'team_member': member.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating team member: {str(e)}'
        }), 500

@app.route('/api/team/members/<int:member_id>', methods=['DELETE'])
def delete_team_member(member_id):
    try:
        member = TeamMember.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Team member deleted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting team member: {str(e)}'
        }), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new contact message
        contact = ContactMessage(
            full_name=data['full_name'],
            email=data['email'],
            subject=data.get('subject', ''),
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Your message has been sent successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error sending message: {str(e)}'
        }), 500

@app.route('/api/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email'):
            return jsonify({
                'success': False,
                'message': 'Email address is required'
            }), 400
        
        # Check if already subscribed
        existing_subscriber = NewsletterSubscriber.query.filter_by(
            email=data['email']).first()
        if existing_subscriber:
            if existing_subscriber.is_active:
                return jsonify({
                    'success': False,
                    'message': 'This email is already subscribed to our newsletter.'
                }), 400
            else:
                # Reactivate existing subscriber
                existing_subscriber.is_active = True
                existing_subscriber.name = data.get('name', existing_subscriber.name)
        else:
            # Create new subscriber
            subscriber = NewsletterSubscriber(
                name=data.get('name', ''),
                email=data['email']
            )
            db.session.add(subscriber)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Successfully subscribed to our newsletter!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error subscribing to newsletter: {str(e)}'
        }), 500

@app.route('/api/volunteer/register', methods=['POST'])
def register_volunteer():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Create new volunteer registration
        volunteer = Volunteer(
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            address=data.get('address', ''),
            skills=json.dumps(data.get('skills', [])),
            availability=data.get('availability', '')
        )
        
        db.session.add(volunteer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Volunteer registration submitted successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting volunteer registration: {str(e)}'
        }), 500

# Admin routes
@app.route('/api/admin/memberships', methods=['GET'])
def get_memberships():
    try:
        memberships = Membership.query.order_by(Membership.submission_date.desc()).all()
        return jsonify({
            'success': True,
            'memberships': [m.to_dict() for m in memberships]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching memberships: {str(e)}'
        }), 500

@app.route('/api/admin/memberships/<int:membership_id>/status', methods=['PUT'])
def update_membership_status(membership_id):
    try:
        data = request.get_json()
        membership = Membership.query.get_or_404(membership_id)
        
        if 'status' in data:
            membership.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Membership status updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating membership status: {str(e)}'
        }), 500

# Membership form endpoint that matches your HTML form
@app.route('/api/membership_submit.php', methods=['POST', 'OPTIONS'])
def membership_submit_php():
    """This endpoint handles the PHP-style endpoint that your HTML form is trying to call"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'mykad_no', 'home_address', 'hp_no', 
                          'membership_type', 'proposer_name', 'proposer_mykad',
                          'seconder_name', 'seconder_mykad', 'application_date']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Check if MyKad already exists
        existing_member = Membership.query.filter_by(mykad_no=data['mykad_no']).first()
        if existing_member:
            return jsonify({
                'success': False,
                'message': 'A membership application with this MyKad number already exists.'
            }), 400
        
        # Create new membership application
        membership = Membership(
            full_name=data['full_name'],
            mykad_no=data['mykad_no'],
            home_address=data['home_address'],
            office_address=data.get('office_address', ''),
            phone_home=data.get('phone_home', ''),
            phone_office=data.get('phone_office', ''),
            hp_no=data['hp_no'],
            email=data.get('email', ''),
            political_party=data.get('political_party', ''),
            membership_type=data['membership_type'],
            years=data.get('years', 1),
            amount_paid=data.get('amount_paid', 0),
            proposer_name=data['proposer_name'],
            proposer_mykad=data['proposer_mykad'],
            seconder_name=data['seconder_name'],
            seconder_mykad=data['seconder_mykad'],
            application_date=datetime.strptime(data['application_date'], '%Y-%m-%d').date()
        )
        
        db.session.add(membership)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Membership application submitted successfully!',
            'application_id': membership.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting application: {str(e)}'
        }), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)