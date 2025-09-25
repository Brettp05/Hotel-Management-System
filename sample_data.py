#!/usr/bin/env python3
"""
Sample data script for Taj Hotels Management System
Run this script to populate the database with sample data
"""

from app import app, db
from models import User, Hotel, Room, Booking, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
import random

def create_sample_data():
    """Create sample data for the hotel management system"""
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@luxuryhotels.com',
            first_name='Admin',
            last_name='User',
            phone='+91 9876543210',
            is_admin=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Create regular users
        users = []
        for i in range(5):
            user = User(
                username=f'user{i+1}',
                email=f'user{i+1}@example.com',
                first_name=f'User{i+1}',
                last_name='Test',
                phone=f'+91 987654321{i}'
            )
            user.set_password('password123')
            users.append(user)
            db.session.add(user)
        
        # Create sample hotels
        hotels_data = [
            {
                'name': 'Grand Palace Hotel, Mumbai',
                'description': 'An iconic luxury hotel overlooking the Gateway of India and Arabian Sea. This heritage property offers world-class amenities and exceptional service.',
                'address': 'Apollo Bunder, Colaba',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'country': 'India',
                'zip_code': '400001',
                'phone': '+91 22 6665 3366',
                'email': 'mumbai@luxuryhotels.com',
                'website': 'https://www.luxuryhotels.com/mumbai/grand-palace',
                'star_rating': 5,
                'is_featured': True
            },
            {
                'name': 'Lakeview Palace, Udaipur',
                'description': 'A romantic luxury hotel floating on Lake Pichola. This 18th-century palace offers breathtaking views and royal hospitality.',
                'address': 'Lake Pichola',
                'city': 'Udaipur',
                'state': 'Rajasthan',
                'country': 'India',
                'zip_code': '313001',
                'phone': '+91 294 242 8800',
                'email': 'udaipur@luxuryhotels.com',
                'website': 'https://www.luxuryhotels.com/udaipur/lakeview-palace',
                'star_rating': 5,
                'is_featured': True
            },
            {
                'name': 'Royal Heights Palace, Hyderabad',
                'description': 'A magnificent palace hotel offering royal luxury and heritage charm. Perched 2000 feet above the city, it provides panoramic views.',
                'address': 'Engine Bowli, Falaknuma',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'country': 'India',
                'zip_code': '500053',
                'phone': '+91 40 6629 8585',
                'email': 'hyderabad@luxuryhotels.com',
                'website': 'https://www.luxuryhotels.com/hyderabad/royal-heights-palace',
                'star_rating': 5,
                'is_featured': True
            },
            {
                'name': 'Oceanview Resort, Mumbai',
                'description': 'A contemporary luxury hotel in Bandra West with stunning Arabian Sea views and modern amenities.',
                'address': 'Bandra West',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'country': 'India',
                'zip_code': '400050',
                'phone': '+91 22 6668 1234',
                'email': 'oceanview@luxuryhotels.com',
                'star_rating': 5,
                'is_featured': False
            },
            {
                'name': 'Garden Palace, Bangalore',
                'description': 'A heritage luxury hotel set in 20 acres of lush gardens in the heart of Bangalore.',
                'address': 'Race Course Road',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'country': 'India',
                'zip_code': '560001',
                'phone': '+91 80 6660 5660',
                'email': 'bangalore@luxuryhotels.com',
                'star_rating': 5,
                'is_featured': False
            },
            {
                'name': 'Business Center Hotel, Chennai',
                'description': 'A luxury business hotel in the heart of Chennai with modern facilities and warm hospitality.',
                'address': '37, Mahatma Gandhi Road, Nungambakkam',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'country': 'India',
                'zip_code': '600034',
                'phone': '+91 44 6600 0000',
                'email': 'chennai@luxuryhotels.com',
                'star_rating': 5,
                'is_featured': False
            }
        ]
        
        hotels = []
        for hotel_data in hotels_data:
            hotel = Hotel(**hotel_data)
            hotels.append(hotel)
            db.session.add(hotel)
        
        db.session.commit()
        
        # Create sample rooms for each hotel
        room_types = [
            {'type': 'Deluxe Room', 'base_price': 15000, 'max_occupancy': 2},
            {'type': 'Executive Suite', 'base_price': 25000, 'max_occupancy': 2},
            {'type': 'Presidential Suite', 'base_price': 50000, 'max_occupancy': 4},
            {'type': 'Garden View Room', 'base_price': 18000, 'max_occupancy': 2},
            {'type': 'Sea View Room', 'base_price': 22000, 'max_occupancy': 2},
            {'type': 'Heritage Suite', 'base_price': 35000, 'max_occupancy': 3}
        ]
        
        for hotel in hotels:
            for i, room_type in enumerate(room_types):
                # Create 3-5 rooms of each type
                num_rooms = random.randint(3, 5)
                for j in range(num_rooms):
                    room = Room(
                        hotel_id=hotel.id,
                        room_number=f"{room_type['type'][:2].upper()}{i+1:02d}{j+1:02d}",
                        room_type=room_type['type'],
                        description=f"Luxurious {room_type['type'].lower()} with modern amenities and elegant decor.",
                        max_occupancy=room_type['max_occupancy'],
                        price_per_night=room_type['base_price'] + random.randint(-2000, 5000),
                        is_available=random.choice([True, True, True, False])  # 75% available
                    )
                    db.session.add(room)
        
        db.session.commit()
        
        # Create sample bookings
        rooms = Room.query.all()
        booking_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        
        for i in range(20):
            room = random.choice(rooms)
            user = random.choice(users)
            check_in = date.today() + timedelta(days=random.randint(-30, 60))
            check_out = check_in + timedelta(days=random.randint(1, 7))
            
            booking = Booking(
                user_id=user.id,
                room_id=room.id,
                check_in_date=check_in,
                check_out_date=check_out,
                num_guests=random.randint(1, room.max_occupancy),
                total_amount=room.price_per_night * (check_out - check_in).days,
                status=random.choice(booking_statuses),
                special_requests=random.choice([
                    None, 
                    "Late check-in requested",
                    "Vegetarian meals only",
                    "High floor room preferred",
                    "Airport pickup required"
                ]),
                payment_status=random.choice(['pending', 'paid', 'refunded']),
                payment_method=random.choice([None, 'Credit Card', 'UPI', 'Net Banking'])
            )
            db.session.add(booking)
        
        db.session.commit()
        
        # Create sample reviews
        confirmed_bookings = Booking.query.filter_by(status='confirmed').all()
        
        for i in range(15):
            if confirmed_bookings:
                booking = random.choice(confirmed_bookings)
                review = Review(
                    user_id=booking.user_id,
                    hotel_id=booking.room.hotel_id,
                    rating=random.randint(3, 5),
                    title=random.choice([
                        "Excellent stay!",
                        "Perfect luxury experience",
                        "Outstanding service",
                        "Beautiful property",
                        "Highly recommended",
                        "Memorable experience",
                        "World-class hospitality"
                    ]),
                    comment=random.choice([
                        "The hotel exceeded all our expectations. The staff was incredibly attentive and the facilities were top-notch.",
                        "Beautiful property with excellent service. The room was spacious and well-appointed.",
                        "A truly luxurious experience. The food was exceptional and the location was perfect.",
                        "Outstanding hospitality and attention to detail. Will definitely return.",
                        "The hotel staff went above and beyond to make our stay memorable. Highly recommended!",
                        "Stunning architecture and impeccable service. A perfect blend of heritage and modernity.",
                        "Exceptional experience from check-in to check-out. The amenities were world-class."
                    ]),
                    is_verified=True
                )
                db.session.add(review)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        print(f"Created:")
        print(f"- 1 admin user (admin@luxuryhotels.com / admin123)")
        print(f"- 5 regular users")
        print(f"- {len(hotels)} hotels")
        print(f"- {len(rooms)} rooms")
        print(f"- 20 bookings")
        print(f"- 15 reviews")

if __name__ == '__main__':
    create_sample_data()
