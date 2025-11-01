from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from models import db, User, Post, MembershipApplication, Branch, BranchActivity, GalleryImage, Logo
from datetime import datetime
import os
from flask_migrate import Migrate
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-12345-change-in-production'

# WAMP Server MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/community_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Shows SQL queries in console (optional)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'image': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    'video': ['mp4', 'mov', 'avi', 'mkv', 'webm'],
    'audio': ['mp3', 'wav', 'ogg', 'm4a']
}

def allowed_file(filename, file_type):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, [])

def save_uploaded_file(file, file_type):
    """Save uploaded file with unique filename"""
    if file and file.filename:
        if allowed_file(file.filename, file_type):
            # Generate unique filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{file_type}_{uuid.uuid4().hex}.{ext}"
            
            # Create uploads directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return filename
    return None

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Create tables
with app.app_context():
    try:
        db.create_all()
        
        # Create default test user if doesn't exist
        if not User.query.filter_by(email='test@example.com').first():
            default_user = User(
                username='testuser',
                email='test@example.com'
            )
            default_user.set_password('password123')
            default_user.is_branch_admin = True
            db.session.add(default_user)
            db.session.commit()
            print("Default admin user created: test@example.com / password123")
    except Exception as e:
        print(f"Database initialization note: {e}")
        print("If you're getting column errors, run flask db upgrade")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/membership')
def membership_form():
    return render_template('membership.html')

@app.route('/membership-status')
def membership_status():
    return render_template('membership_status.html')

# Serve uploaded files
@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Authentication Routes
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'})

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['loggedin'] = True
            session['is_branch_admin'] = True
            session['branch_id'] = getattr(user, 'branch_id', None)
            
            return jsonify({
                'success': True, 
                'message': 'Login successful!',
                'username': user.username,
                'is_branch_admin': True
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'})

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during login'})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        # Validation
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'})

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'})

        if len(username) < 3:
            return jsonify({'success': False, 'message': 'Username must be at least 3 characters'})

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'})

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already taken'})

        # Create new user
        new_user = User(username=username, email=email, is_branch_admin=True)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        # Auto-login after registration
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['email'] = new_user.email
        session['loggedin'] = True
        session['is_branch_admin'] = True
        session['branch_id'] = None

        return jsonify({
            'success': True, 
            'message': 'Registration successful!',
            'username': new_user.username
        })

    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during registration'})

@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/check-auth')
def check_auth():
    if 'loggedin' in session and session['loggedin']:
        return jsonify({
            'loggedin': True,
            'username': session.get('username'),
            'email': session.get('email'),
            'is_branch_admin': True,
            'branch_id': session.get('branch_id')
        })
    return jsonify({'loggedin': False})

# Posts Routes
@app.route('/api/posts')
def get_posts():
    try:
        posts = Post.query.join(User).order_by(Post.created_at.desc()).all()
        posts_data = [post.to_dict() for post in posts]
        return jsonify(posts_data)
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return jsonify([])

@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        print("=== CREATE POST START ===")
        
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in to create posts'})

        # Handle form data for file uploads
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        tags = request.form.get('tags', '')
        
        print(f"Received - Title: '{title}', Content: '{content}', Tags: '{tags}'")

        if not content:
            return jsonify({'success': False, 'message': 'Post content is required'})

        # Handle file uploads
        image_file = request.files.get('image')
        video_file = request.files.get('video')
        audio_file = request.files.get('audio')

        print(f"Files received - Image: {image_file.filename if image_file else 'None'}, "
              f"Video: {video_file.filename if video_file else 'None'}, "
              f"Audio: {audio_file.filename if audio_file else 'None'}")

        # Save files and get filenames
        image_filename = None
        video_filename = None
        audio_filename = None

        if image_file and image_file.filename:
            image_filename = save_uploaded_file(image_file, 'image')
            print(f"Image saved as: {image_filename}")

        if video_file and video_file.filename:
            video_filename = save_uploaded_file(video_file, 'video')
            print(f"Video saved as: {video_filename}")

        if audio_file and audio_file.filename:
            audio_filename = save_uploaded_file(audio_file, 'audio')
            print(f"Audio saved as: {audio_filename}")

        # Process tags
        tag_list = [tag.strip() for tag in tags.split(',')] if tags else []

        # Create new post
        new_post = Post(
            title=title,
            content=content,
            user_id=session['user_id'],
            tags=','.join(tag_list) if tag_list else None,
            image_filename=image_filename,
            video_filename=video_filename,
            audio_filename=audio_filename
        )
        
        db.session.add(new_post)
        db.session.commit()

        print("=== CREATE POST SUCCESS ===")
        return jsonify({
            'success': True, 
            'message': 'Post created successfully!',
            'post': new_post.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error creating post: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': f'An error occurred while creating post: {str(e)}'})

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})

        post = Post.query.get_or_404(post_id)

        # Check if user owns the post
        if post.user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Unauthorized'})

        # Delete associated files
        if post.image_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.image_filename))
            except:
                pass
        if post.video_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.video_filename))
            except:
                pass
        if post.audio_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.audio_filename))
            except:
                pass

        db.session.delete(post)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Post deleted successfully'})

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting post: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while deleting post'})

# Membership Form Routes
@app.route('/api/membership/submit', methods=['POST'])
def submit_membership():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'mykad_no', 'home_address', 'hp_no', 
                          'membership_type', 'years', 'amount_paid',
                          'proposer_name', 'proposer_mykad', 
                          'seconder_name', 'seconder_mykad', 'application_date']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'})
        
        # Create new membership application
        new_application = MembershipApplication(
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
            years=data['years'],
            amount_paid=data['amount_paid'],
            proposer_name=data['proposer_name'],
            proposer_mykad=data['proposer_mykad'],
            seconder_name=data['seconder_name'],
            seconder_mykad=data['seconder_mykad'],
            application_date=datetime.strptime(data['application_date'], '%Y-%m-%d').date(),
            status='Pending'
        )
        
        db.session.add(new_application)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Membership application submitted successfully! Your application is now pending review.',
            'application_id': new_application.id,
            'status': new_application.status
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Membership submission error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while submitting the application'})

@app.route('/api/membership/applications')
def get_membership_applications():
    try:
        applications = MembershipApplication.query.order_by(MembershipApplication.submitted_at.desc()).all()
        applications_data = [app.to_dict() for app in applications]
        
        return jsonify({
            'success': True,
            'applications': applications_data
        })
        
    except Exception as e:
        print(f"Error fetching membership applications: {e}")
        return jsonify({'success': False, 'message': 'Error fetching applications'})

@app.route('/api/membership/check-status', methods=['POST'])
def check_membership_status():
    try:
        data = request.get_json()
        mykad_no = data.get('mykad_no', '').strip()
        
        if not mykad_no:
            return jsonify({'success': False, 'message': 'MyKad number is required'})
        
        # Find application by MyKad number
        application = MembershipApplication.query.filter_by(mykad_no=mykad_no).order_by(MembershipApplication.submitted_at.desc()).first()
        
        if application:
            return jsonify({
                'success': True,
                'application': application.to_dict(),
                'message': f'Application found. Status: {application.status}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No application found with this MyKad number'
            })
            
    except Exception as e:
        print(f"Error checking membership status: {e}")
        return jsonify({'success': False, 'message': 'Error checking application status'})

@app.route('/api/membership/update-status', methods=['POST'])
def update_membership_status():
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})
            
        data = request.get_json()
        application_id = data.get('application_id')
        new_status = data.get('status')
        
        if not application_id or not new_status:
            return jsonify({'success': False, 'message': 'Application ID and status are required'})
        
        if new_status not in ['Pending', 'Approved', 'Rejected', 'Cancelled']:
            return jsonify({'success': False, 'message': 'Invalid status'})
        
        application = MembershipApplication.query.get(application_id)
        
        if not application:
            return jsonify({'success': False, 'message': 'Application not found'})
        
        application.status = new_status
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Application status updated to {new_status}',
            'application': application.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating membership status: {e}")
        return jsonify({'success': False, 'message': 'Error updating application status'})

# Dashboard Stats Route
@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})

        # Get total posts count
        total_posts = Post.query.count()
        
        # Get user's posts count
        user_posts = Post.query.filter_by(user_id=session['user_id']).count()
        
        # Get total users count
        total_users = User.query.count()
        
        # Get membership stats
        total_applications = MembershipApplication.query.count()
        pending_applications = MembershipApplication.query.filter_by(status='Pending').count()
        approved_applications = MembershipApplication.query.filter_by(status='Approved').count()

        # Get gallery stats
        total_gallery_images = GalleryImage.query.filter_by(is_active=True).count()

        return jsonify({
            'success': True,
            'stats': {
                'total_posts': total_posts,
                'user_posts': user_posts,
                'total_users': total_users,
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'approved_applications': approved_applications,
                'total_gallery_images': total_gallery_images
            }
        })

    except Exception as e:
        print(f"Error fetching dashboard stats: {e}")
        return jsonify({'success': False, 'message': 'Error fetching dashboard stats'})

# User Profile Routes
@app.route('/api/profile')
def get_profile():
    if 'loggedin' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'posts': [post.to_dict() for post in user_posts]
    })

# Branch Management Routes
@app.route('/api/branches')
def get_branches():
    try:
        branches = Branch.query.filter_by(is_active=True).all()
        branches_data = [branch.to_dict() for branch in branches]
        
        return jsonify({
            'success': True,
            'branches': branches_data
        })
        
    except Exception as e:
        print(f"Error fetching branches: {e}")
        return jsonify({'success': False, 'message': 'Error fetching branches'})

@app.route('/api/branches', methods=['POST'])
def create_branch():
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'code', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'})
        
        # Check if branch code already exists
        if Branch.query.filter_by(code=data['code']).first():
            return jsonify({'success': False, 'message': 'Branch code already exists'})
        
        # Create new branch
        new_branch = Branch(
            name=data['name'],
            code=data['code'],
            address=data['address'],
            contact_number=data.get('contact_number', ''),
            email=data.get('email', '')
        )
        
        db.session.add(new_branch)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Branch created successfully',
            'branch': new_branch.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating branch: {e}")
        return jsonify({'success': False, 'message': 'Error creating branch'})

@app.route('/api/branches/<int:branch_id>', methods=['PUT'])
def update_branch(branch_id):
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})
            
        data = request.get_json()
        branch = Branch.query.get(branch_id)
        
        if not branch:
            return jsonify({'success': False, 'message': 'Branch not found'})
        
        # Update branch fields
        if 'name' in data:
            branch.name = data['name']
        if 'address' in data:
            branch.address = data['address']
        if 'contact_number' in data:
            branch.contact_number = data['contact_number']
        if 'email' in data:
            branch.email = data['email']
        if 'is_active' in data:
            branch.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Branch updated successfully',
            'branch': branch.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating branch: {e}")
        return jsonify({'success': False, 'message': 'Error updating branch'})

@app.route('/api/branches/<int:branch_id>/activities')
def get_branch_activities(branch_id):
    try:
        activities = BranchActivity.query.filter_by(branch_id=branch_id).order_by(BranchActivity.activity_date.desc()).all()
        activities_data = [activity.to_dict() for activity in activities]
        
        return jsonify({
            'success': True,
            'activities': activities_data
        })
        
    except Exception as e:
        print(f"Error fetching branch activities: {e}")
        return jsonify({'success': False, 'message': 'Error fetching activities'})

@app.route('/api/branches/activities', methods=['POST'])
def create_branch_activity():
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})
            
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['branch_id', 'title', 'activity_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'})
        
        # Parse activity date
        activity_date_str = data['activity_date']
        try:
            activity_date = datetime.strptime(activity_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            try:
                activity_date = datetime.strptime(activity_date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM'})
        
        # Create new activity
        new_activity = BranchActivity(
            branch_id=data['branch_id'],
            title=data['title'],
            description=data.get('description', ''),
            activity_date=activity_date,
            location=data.get('location', ''),
            created_by=session['user_id']
        )
        
        db.session.add(new_activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Activity created successfully',
            'activity': new_activity.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating activity: {e}")
        return jsonify({'success': False, 'message': f'Error creating activity: {str(e)}'})

@app.route('/api/branches/activities/<int:activity_id>', methods=['PUT'])
def update_branch_activity(activity_id):
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})
            
        data = request.get_json()
        activity = BranchActivity.query.get(activity_id)
        
        if not activity:
            return jsonify({'success': False, 'message': 'Activity not found'})
        
        # Update activity fields
        if 'title' in data:
            activity.title = data['title']
        if 'description' in data:
            activity.description = data['description']
        if 'activity_date' in data:
            try:
                activity.activity_date = datetime.strptime(data['activity_date'], '%Y-%m-%dT%H:%M')
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format'})
        if 'location' in data:
            activity.location = data['location']
        if 'is_archived' in data:
            activity.is_archived = data['is_archived']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Activity updated successfully',
            'activity': activity.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating activity: {e}")
        return jsonify({'success': False, 'message': 'Error updating activity'})

@app.route('/api/branches/<int:branch_id>/stats')
def get_branch_stats(branch_id):
    try:
        branch = Branch.query.get(branch_id)
        
        if not branch:
            return jsonify({'success': False, 'message': 'Branch not found'})
        
        # Calculate branch statistics
        total_members = len(branch.members)
        branch_admins = len([user for user in branch.members if getattr(user, 'is_branch_admin', True)])
        pending_applications = len([app for app in branch.applications if app.status == 'Pending'])
        approved_applications = len([app for app in branch.applications if app.status == 'Approved'])
        active_activities = len([activity for activity in branch.activities if not activity.is_archived])
        
        return jsonify({
            'success': True,
            'stats': {
                'total_members': total_members,
                'branch_admins': branch_admins,
                'pending_applications': pending_applications,
                'approved_applications': approved_applications,
                'active_activities': active_activities
            }
        })
        
    except Exception as e:
        print(f"Error fetching branch stats: {e}")
        return jsonify({'success': False, 'message': 'Error fetching branch statistics'})

# Gallery Routes
@app.route('/api/gallery')
def get_gallery_images():
    try:
        images = GalleryImage.query.filter_by(is_active=True)\
            .join(User)\
            .order_by(GalleryImage.created_at.desc()).all()
        images_data = [image.to_dict() for image in images]
        return jsonify({
            'success': True,
            'images': images_data
        })
    except Exception as e:
        print(f"Error fetching gallery images: {e}")
        return jsonify({'success': False, 'message': 'Error fetching gallery images'})

@app.route('/api/gallery', methods=['POST'])
def upload_gallery_image():
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in to upload images'})

        # Handle form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_file = request.files.get('image')

        if not title:
            return jsonify({'success': False, 'message': 'Image title is required'})

        if not image_file or not image_file.filename:
            return jsonify({'success': False, 'message': 'Image file is required'})

        # Save the image file
        image_filename = save_uploaded_file(image_file, 'image')
        if not image_filename:
            return jsonify({'success': False, 'message': 'Invalid image file format'})

        # Create new gallery image
        new_image = GalleryImage(
            title=title,
            description=description,
            image_filename=image_filename,
            uploaded_by=session['user_id']
        )

        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully!',
            'image': new_image.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error uploading gallery image: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while uploading image'})

@app.route('/api/gallery/<int:image_id>', methods=['DELETE'])
def delete_gallery_image(image_id):
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})

        image = GalleryImage.query.get_or_404(image_id)

        # Check if user owns the image
        if image.uploaded_by != session['user_id']:
            return jsonify({'success': False, 'message': 'Unauthorized'})

        # Delete associated file
        if image.image_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.image_filename))
            except:
                pass

        db.session.delete(image)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Image deleted successfully'})

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting gallery image: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while deleting image'})

# Logo Management Routes
@app.route('/api/logo')
def get_logo():
    """Get the current active logo"""
    try:
        logo = Logo.query.filter_by(is_active=True).first()
        if logo:
            return jsonify({
                'success': True,
                'logo': logo.to_dict()
            })
        else:
            return jsonify({
                'success': True,
                'logo': None,
                'message': 'No logo set'
            })
    except Exception as e:
        print(f"Error fetching logo: {e}")
        return jsonify({'success': False, 'message': 'Error fetching logo'})

@app.route('/api/logo', methods=['POST'])
def upload_logo():
    """Upload a new logo and set it as active"""
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in to upload logo'})

        logo_file = request.files.get('logo')
        
        if not logo_file or not logo_file.filename:
            return jsonify({'success': False, 'message': 'Logo file is required'})

        # Save the logo file
        logo_filename = save_uploaded_file(logo_file, 'image')
        if not logo_filename:
            return jsonify({'success': False, 'message': 'Invalid logo file format. Allowed: jpg, jpeg, png, gif, webp'})

        # Deactivate all existing logos
        Logo.query.update({'is_active': False})
        
        # Create new active logo
        new_logo = Logo(
            filename=logo_filename,
            original_filename=logo_file.filename,
            uploaded_by=session['user_id'],
            is_active=True
        )

        db.session.add(new_logo)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Logo uploaded successfully!',
            'logo': new_logo.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error uploading logo: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while uploading logo'})

@app.route('/api/logo/history')
def get_logo_history():
    """Get logo upload history"""
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})

        logos = Logo.query.join(User).order_by(Logo.uploaded_at.desc()).all()
        logos_data = [logo.to_dict() for logo in logos]
        
        return jsonify({
            'success': True,
            'logos': logos_data
        })
    except Exception as e:
        print(f"Error fetching logo history: {e}")
        return jsonify({'success': False, 'message': 'Error fetching logo history'})

@app.route('/api/logo/<int:logo_id>/set-active', methods=['POST'])
def set_logo_active(logo_id):
    """Set a specific logo as active"""
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})

        # Deactivate all logos
        Logo.query.update({'is_active': False})
        
        # Activate the selected logo
        logo = Logo.query.get(logo_id)
        if not logo:
            return jsonify({'success': False, 'message': 'Logo not found'})
            
        logo.is_active = True
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Logo set as active successfully!',
            'logo': logo.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error setting logo active: {e}")
        return jsonify({'success': False, 'message': 'Error setting logo as active'})

@app.route('/api/logo/<int:logo_id>', methods=['DELETE'])
def delete_logo(logo_id):
    """Delete a logo (cannot delete active logo)"""
    try:
        if 'loggedin' not in session:
            return jsonify({'success': False, 'message': 'Please log in'})

        logo = Logo.query.get_or_404(logo_id)

        # Prevent deleting active logo
        if logo.is_active:
            return jsonify({'success': False, 'message': 'Cannot delete active logo. Set another logo as active first.'})

        # Delete associated file
        if logo.filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], logo.filename))
            except:
                pass

        db.session.delete(logo)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Logo deleted successfully'})

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting logo: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while deleting logo'})

# Get all activities for branch management page
@app.route('/api/branches/activities/all')
def get_all_activities():
    try:
        activities = BranchActivity.query.join(Branch).join(User, BranchActivity.created_by == User.id)\
            .order_by(BranchActivity.activity_date.desc()).all()
        activities_data = [activity.to_dict() for activity in activities]
        
        return jsonify({
            'success': True,
            'activities': activities_data
        })
        
    except Exception as e:
        print(f"Error fetching all activities: {e}")
        return jsonify({'success': False, 'message': 'Error fetching activities'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)