#!/usr/bin/env python3
"""
Setup script for Taj Hotels Management System
Run this script to set up the application
"""

import os
import sys
import subprocess

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///hotel_management.db
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("⚠️  .env file already exists")

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Installed required packages")
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/css',
        'static/js', 
        'static/images',
        'templates/layouts',
        'templates/auth',
        'templates/hotels',
        'templates/booking',
        'templates/admin'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Created necessary directories")

def setup_database():
    """Set up the database with sample data"""
    try:
        from sample_data import create_sample_data
        create_sample_data()
        print("✅ Database initialized with sample data")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)

def main():
    """Main setup function"""
    print("🏨 Setting up Luxury Hotels Management System...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install requirements
    install_requirements()
    
    # Setup database
    setup_database()
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  python app.py")
    print("\nThen visit: http://localhost:5000")
    print("\nDefault admin login:")
    print("  Email: admin@luxuryhotels.com")
    print("  Password: admin123")

if __name__ == '__main__':
    main()
