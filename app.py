from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration - supports both SQLite and PostgreSQL
database_url = os.environ.get('DATABASE_URL', 'sqlite:///hotel_management.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# PostgreSQL specific configurations
if database_url.startswith('postgresql'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }

# Import and initialize database
from models import db
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import models and routes
from models import User, Hotel, Room, Booking, Review
from routes import auth_bp, hotel_bp, booking_bp, admin_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(hotel_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(admin_bp)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    featured_hotels = Hotel.query.filter_by(is_featured=True).limit(6).all()
    return render_template('index.html', featured_hotels=featured_hotels)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
