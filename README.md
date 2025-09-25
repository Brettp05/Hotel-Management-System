# Luxury Hotels Management System

A comprehensive hotel management system built with Python Flask, featuring a modern web interface for luxury hotel bookings. This system provides complete functionality for hotel bookings, user management, and administrative operations.

## Features

### 🏨 Hotel Management
- **Hotel Listings**: Browse and search through luxury hotels
- **Detailed Views**: Comprehensive hotel information with images and amenities
- **Room Management**: Different room types with pricing and availability
- **Search & Filter**: Advanced search by location, star rating, and dates

### 👤 User Management
- **User Registration & Login**: Secure authentication system
- **Profile Management**: User profiles with booking history
- **Role-based Access**: Separate interfaces for guests and administrators

### 📅 Booking System
- **Room Booking**: Easy booking process with date selection
- **Booking Management**: View, modify, and cancel bookings
- **Payment Integration**: Ready for payment gateway integration
- **Booking Confirmation**: Email notifications and confirmations

### 🛠️ Admin Dashboard
- **Dashboard Overview**: Key metrics and statistics
- **Hotel Management**: Add, edit, and manage hotel properties
- **Booking Management**: Oversee all bookings and confirmations
- **User Management**: Manage user accounts and permissions

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on all devices
- **Bootstrap 5**: Modern, clean interface
- **Interactive Elements**: Smooth animations and transitions
- **Luxury Hotel Branding**: Professional luxury hotel aesthetic

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Icons**: Font Awesome
- **Images**: Unsplash (placeholder images)

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd HMS
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///hotel_management.db
```

### 5. Initialize Database
```bash
python sample_data.py
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Default Login Credentials

### Admin Account
- **Email**: admin@luxuryhotels.com
- **Password**: admin123

### Regular User Accounts
- **Email**: user1@example.com to user5@example.com
- **Password**: password123

## Project Structure

```
HMS/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── routes.py              # Application routes
├── forms.py               # WTForms definitions
├── sample_data.py         # Sample data generator
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── layouts/
│   │   └── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── hotels/
│   │   ├── list.html
│   │   └── detail.html
│   ├── booking/
│   │   ├── book.html
│   │   ├── detail.html
│   │   └── my_bookings.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   └── bookings.html
│   ├── index.html
│   ├── about.html
│   └── contact.html
└── static/               # Static assets
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
```

## Key Features Explained

### Hotel Search & Filtering
- Search by city, hotel name, or description
- Filter by star rating (3-5 stars)
- Date-based availability checking
- Guest count filtering

### Booking Process
1. **Search**: Find hotels by location and dates
2. **Select**: Choose from available rooms
3. **Book**: Fill in booking details and special requests
4. **Confirm**: Review booking summary and complete payment
5. **Manage**: View and manage bookings in user dashboard

### Admin Features
- **Dashboard**: Overview of key metrics and recent activity
- **Hotel Management**: Add/edit hotel properties and rooms
- **Booking Management**: View all bookings and confirmations
- **User Management**: Manage user accounts and permissions

### Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Touch-friendly interface
- Optimized for all screen sizes

## Customization

### Adding New Hotels
1. Access the admin dashboard
2. Use the hotel management interface
3. Add hotel details, images, and amenities
4. Configure room types and pricing

### Payment Integration
The system is ready for payment gateway integration:
- Stripe
- Razorpay
- PayPal
- Other payment processors

### Email Notifications
Configure email settings in the Flask app for:
- Booking confirmations
- Payment receipts
- Cancellation notifications
- Marketing emails

## Database Schema

### Users Table
- User authentication and profile information
- Role-based access control (admin/regular user)

### Hotels Table
- Hotel information and amenities
- Location and contact details
- Featured hotel flagging

### Rooms Table
- Room types and pricing
- Availability status
- Hotel association

### Bookings Table
- Booking details and dates
- Payment status tracking
- User and room associations

### Reviews Table
- Guest reviews and ratings
- Hotel and user associations
- Verification status

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Hotels
- `GET /hotels` - List all hotels
- `GET /hotel/<id>` - Hotel details
- `GET /search` - Search hotels

### Bookings
- `POST /book/<room_id>` - Create booking
- `GET /booking/<id>` - Booking details
- `GET /my-bookings` - User's bookings
- `GET /cancel-booking/<id>` - Cancel booking

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/hotels` - Manage hotels
- `GET /admin/bookings` - Manage bookings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@tajhotels.com
- Phone: +91 22 1234 5678

## Future Enhancements

- [ ] Real-time availability updates
- [ ] Advanced payment processing
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with external booking systems
- [ ] Loyalty program features
- [ ] Event management system

---

**Built with ❤️ for luxury hospitality management**
