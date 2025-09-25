# Database Setup Guide

This guide explains how to set up different database options for the Hotel Management System.

## 🏆 Recommended: PostgreSQL

### Option 1: Docker (Easiest)

1. **Install Docker Desktop** from https://www.docker.com/products/docker-desktop

2. **Start PostgreSQL with Docker:**
   ```bash
   docker-compose up -d postgres
   ```

3. **Update your .env file:**
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_management
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database:**
   ```bash
   python sample_data.py
   ```

### Option 2: Local PostgreSQL Installation

1. **Install PostgreSQL:**
   - Windows: Download from https://www.postgresql.org/download/windows/
   - macOS: `brew install postgresql`
   - Ubuntu: `sudo apt-get install postgresql postgresql-contrib`

2. **Create database:**
   ```bash
   python database_setup.py
   ```

3. **Update .env file** (if not done automatically):
   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=hotel_management
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hotel_management
   ```

## 🗄️ Alternative: SQLite (Development Only)

For development and testing, you can use SQLite:

1. **Update .env file:**
   ```env
   DATABASE_URL=sqlite:///hotel_management.db
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

## 🍃 MongoDB (Not Recommended)

While MongoDB could work, it's not recommended for this hotel management system because:

- **Relational Data**: Hotels, rooms, bookings have clear relationships
- **ACID Transactions**: Critical for booking and payment integrity
- **Complex Queries**: SQL is better for reporting and analytics
- **Data Consistency**: Relational model ensures data integrity

If you still want to use MongoDB, you would need to:
1. Rewrite all models to use MongoDB documents
2. Implement custom relationship handling
3. Add data validation and consistency checks
4. Rewrite all queries to use MongoDB syntax

## 🚀 Quick Start with PostgreSQL

### Using Docker (Recommended):

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python sample_data.py

# 4. Run application
python app.py
```

### Using Local PostgreSQL:

```bash
# 1. Install PostgreSQL (see instructions above)

# 2. Run setup script
python database_setup.py

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python sample_data.py

# 5. Run application
python app.py
```

## 🔧 Database Configuration

### Environment Variables:

```env
# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=hotel_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Flask Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_management
```

### Connection Pool Settings:

The application automatically configures connection pooling for PostgreSQL:

- **Pool Size**: 10 connections
- **Max Overflow**: 20 additional connections
- **Pool Recycle**: 300 seconds
- **Pool Pre-ping**: Enabled (checks connections before use)

## 📊 Database Schema

### Tables:
- **users**: User accounts and profiles
- **hotels**: Hotel information and details
- **rooms**: Room types and pricing
- **bookings**: Reservation records
- **reviews**: Guest reviews and ratings

### Key Features:
- **Foreign Key Constraints**: Ensure data integrity
- **Indexes**: Optimized for common queries
- **Enums**: Type-safe status fields
- **Timestamps**: Automatic created/updated tracking

## 🛠️ Troubleshooting

### Common Issues:

1. **Connection Refused:**
   - Check if PostgreSQL is running
   - Verify connection details in .env
   - Ensure firewall allows port 5432

2. **Authentication Failed:**
   - Check username/password in .env
   - Verify user has database permissions

3. **Database Not Found:**
   - Run `python database_setup.py`
   - Or create database manually: `CREATE DATABASE hotel_management;`

4. **Permission Denied:**
   - Ensure user has CREATE privileges
   - Check PostgreSQL user roles

### Useful Commands:

```bash
# Check PostgreSQL status
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres

# Connect to database
psql -h localhost -U postgres -d hotel_management

# Reset database
docker-compose down -v
docker-compose up -d postgres
python sample_data.py
```

## 🎯 Performance Optimization

### For Production:

1. **Connection Pooling**: Already configured
2. **Indexes**: Add custom indexes for your query patterns
3. **Query Optimization**: Use EXPLAIN ANALYZE for slow queries
4. **Monitoring**: Set up database monitoring
5. **Backups**: Implement regular backup strategy

### Recommended Indexes:

```sql
-- Add these indexes for better performance
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_hotel_id ON bookings(room_id);
CREATE INDEX idx_bookings_dates ON bookings(check_in_date, check_out_date);
CREATE INDEX idx_hotels_city ON hotels(city);
CREATE INDEX idx_hotels_featured ON hotels(is_featured);
CREATE INDEX idx_rooms_hotel_id ON rooms(hotel_id);
CREATE INDEX idx_rooms_available ON rooms(is_available);
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit .env files
2. **Database Passwords**: Use strong, unique passwords
3. **Connection Encryption**: Enable SSL in production
4. **User Permissions**: Use least-privilege principle
5. **Regular Updates**: Keep PostgreSQL updated

---

**Choose PostgreSQL for the best experience with this hotel management system! 🏨✨**
