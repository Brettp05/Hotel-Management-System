from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from models import User, Hotel, Room, Booking, Review, db
from forms import LoginForm, RegisterForm, BookingForm, ReviewForm
from datetime import datetime, date
import json

# Blueprints
auth_bp = Blueprint('auth', __name__)
hotel_bp = Blueprint('hotel', __name__)
booking_bp = Blueprint('booking', __name__)
admin_bp = Blueprint('admin', __name__)

# Authentication Routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Hotel Routes
@hotel_bp.route('/hotels')
def hotels():
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '')
    star_rating = request.args.get('star_rating', '')
    
    query = Hotel.query.filter_by(is_active=True)
    
    if city:
        query = query.filter(Hotel.city.ilike(f'%{city}%'))
    if star_rating:
        query = query.filter(Hotel.star_rating == int(star_rating))
    
    hotels = query.paginate(page=page, per_page=12, error_out=False)
    return render_template('hotels/list.html', hotels=hotels, city=city, star_rating=star_rating)

@hotel_bp.route('/hotel/<int:hotel_id>')
def hotel_detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    rooms = Room.query.filter_by(hotel_id=hotel_id, is_available=True).all()
    reviews = Review.query.filter_by(hotel_id=hotel_id, is_verified=True).order_by(Review.created_at.desc()).limit(10).all()
    
    # Calculate average rating
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(hotel_id=hotel_id, is_verified=True).scalar() or 0
    
    return render_template('hotels/detail.html', hotel=hotel, rooms=rooms, reviews=reviews, avg_rating=avg_rating)

@hotel_bp.route('/search')
def search():
    query = request.args.get('q', '')
    city = request.args.get('city', '')
    check_in = request.args.get('check_in', '')
    check_out = request.args.get('check_out', '')
    guests = request.args.get('guests', 1, type=int)
    
    hotels = Hotel.query.filter_by(is_active=True)
    
    if query:
        hotels = hotels.filter(
            db.or_(
                Hotel.name.ilike(f'%{query}%'),
                Hotel.city.ilike(f'%{query}%'),
                Hotel.description.ilike(f'%{query}%')
            )
        )
    
    if city:
        hotels = hotels.filter(Hotel.city.ilike(f'%{city}%'))
    
    hotels = hotels.all()
    
    return render_template('hotels/search_results.html', 
                         hotels=hotels, query=query, city=city, 
                         check_in=check_in, check_out=check_out, guests=guests)

# Booking Routes
@booking_bp.route('/book/<int:room_id>', methods=['GET', 'POST'])
@login_required
def book_room(room_id):
    room = Room.query.get_or_404(room_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        # Calculate total amount
        check_in = form.check_in_date.data
        check_out = form.check_out_date.data
        nights = (check_out - check_in).days
        total_amount = room.price_per_night * nights
        
        booking = Booking(
            user_id=current_user.id,
            room_id=room_id,
            check_in_date=check_in,
            check_out_date=check_out,
            num_guests=form.num_guests.data,
            total_amount=total_amount,
            special_requests=form.special_requests.data
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking created successfully! Please complete payment.', 'success')
        return redirect(url_for('booking.booking_detail', booking_id=booking.id))
    
    return render_template('booking/book.html', room=room, form=form)

@booking_bp.route('/booking/<int:booking_id>')
@login_required
def booking_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    return render_template('booking/detail.html', booking=booking)

@booking_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('booking/my_bookings.html', bookings=bookings)

@booking_bp.route('/cancel-booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        db.session.commit()
        flash('Booking cancelled successfully', 'success')
    else:
        flash('Cannot cancel this booking', 'error')
    
    return redirect(url_for('booking.my_bookings'))

# Admin Routes
@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    stats = {
        'total_hotels': Hotel.query.count(),
        'total_rooms': Room.query.count(),
        'total_bookings': Booking.query.count(),
        'total_users': User.query.count(),
        'pending_bookings': Booking.query.filter_by(status='pending').count(),
        'revenue': db.session.query(db.func.sum(Booking.total_amount)).filter_by(status='confirmed').scalar() or 0
    }
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    current_date = datetime.now()
    
    return render_template('admin/dashboard.html', stats=stats, recent_bookings=recent_bookings, current_date=current_date)

@admin_bp.route('/admin/hotels')
@login_required
def admin_hotels():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    hotels = Hotel.query.all()
    return render_template('admin/hotels.html', hotels=hotels)

@admin_bp.route('/admin/bookings')
@login_required
def admin_bookings():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings)

@admin_bp.route('/admin/confirm-booking/<int:booking_id>')
@login_required
def confirm_booking(booking_id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'confirmed'
    db.session.commit()
    flash('Booking confirmed successfully', 'success')
    return redirect(url_for('admin.admin_bookings'))
