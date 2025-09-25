#!/usr/bin/env python3
"""
Database setup script for PostgreSQL
This script helps you set up PostgreSQL for the Hotel Management System
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

def check_postgresql_installed():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL found: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_postgresql_windows():
    """Instructions for installing PostgreSQL on Windows"""
    print("📋 PostgreSQL Installation Instructions for Windows:")
    print("=" * 60)
    print("1. Download PostgreSQL from: https://www.postgresql.org/download/windows/")
    print("2. Run the installer and follow the setup wizard")
    print("3. Remember the password you set for the 'postgres' user")
    print("4. Make sure to add PostgreSQL to your PATH during installation")
    print("5. Restart your command prompt after installation")
    print("\nAlternatively, you can use Docker:")
    print("   docker run --name postgres-hms -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15")

def create_database():
    """Create the hotel_management database"""
    try:
        # Load environment variables
        load_dotenv()
        
        db_name = os.getenv('POSTGRES_DB', 'hotel_management')
        db_user = os.getenv('POSTGRES_USER', 'postgres')
        db_password = os.getenv('POSTGRES_PASSWORD', 'password')
        db_host = os.getenv('POSTGRES_HOST', 'localhost')
        db_port = os.getenv('POSTGRES_PORT', '5432')
        
        # Create database using psql
        create_db_command = f"psql -h {db_host} -p {db_port} -U {db_user} -c 'CREATE DATABASE {db_name};'"
        
        print(f"Creating database '{db_name}'...")
        result = subprocess.run(create_db_command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Database '{db_name}' created successfully!")
            return True
        else:
            print(f"❌ Failed to create database: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def update_env_file():
    """Update .env file with PostgreSQL configuration"""
    env_content = """# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=hotel_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_management

# Alternative SQLite (for development)
# DATABASE_URL=sqlite:///hotel_management.db
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Updated .env file with PostgreSQL configuration")

def test_connection():
    """Test database connection"""
    try:
        from app import app, db
        with app.app_context():
            db.engine.execute('SELECT 1')
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🐘 Setting up PostgreSQL for Luxury Hotels Management System")
    print("=" * 60)
    
    # Check if PostgreSQL is installed
    if not check_postgresql_installed():
        print("❌ PostgreSQL not found!")
        install_postgresql_windows()
        print("\nPlease install PostgreSQL and run this script again.")
        return
    
    # Update environment file
    update_env_file()
    
    # Create database
    if create_database():
        print("\n🎉 PostgreSQL setup completed!")
        print("\nNext steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Run the application: python app.py")
        print("3. Initialize sample data: python sample_data.py")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == '__main__':
    main()
