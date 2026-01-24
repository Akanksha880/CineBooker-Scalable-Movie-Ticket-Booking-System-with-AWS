# CineBooker - Movie Ticket Booking System

A Flask-based web application for booking movie tickets online with user authentication, seat selection, payment processing, and an admin panel.

## Features

### User Features
- **User Registration & Login** - Sign up with name, email/phone, and password
- **Movie Browsing** - View available movies and showtimes
- **Seat Selection** - Interactive seat selection grid for theaters
- **Ticket Booking** - Reserve seats for selected movies
- **Payment Processing** - Support for online and cash-on-delivery payments
- **Booking Management** - View and manage personal bookings

### Admin Features
- **Admin Panel** - Secure admin dashboard
- **System Management** - Access to admin-only operations
- **Authentication** - Admin login with secure credentials

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask Sessions, Werkzeug (password hashing)
- **Storage**: In-memory (Python dictionaries)
- **Server**: Flask development server

## Project Structure

```
CineBooker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/            # HTML templates
    ├── admin_dashboard.html
    ├── admin_login.html
    ├── b1.html          # Seat selection page
    ├── bookings.html    # User bookings list
    ├── home1.html       # User dashboard
    ├── login.html       # User login
    ├── payment.html     # Payment confirmation
    ├── signup.html      # User registration
    ├── tickets.html     # Booking confirmation
    └── static/
        └── style.css    # Application styling
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd CineBooker
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1    # Windows PowerShell
   # or
   source venv/bin/activate    # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install flask werkzeug
   ```

## Running the Application

### Start the Flask Server
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Access Points

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:5000/` | Home (redirects to login) |
| `http://127.0.0.1:5000/login` | User login page |
| `http://127.0.0.1:5000/signup` | User registration page |
| `http://127.0.0.1:5000/home` | User dashboard (after login) |
| `http://127.0.0.1:5000/b1` | Seat selection & booking |
| `http://127.0.0.1:5000/my-bookings` | View your bookings |
| `http://127.0.0.1:5000/admin-login` | Admin panel login |
| `http://127.0.0.1:5000/admin-dashboard` | Admin dashboard (after login) |

## Usage

### For Users

1. **Create an Account**
   - Click "Sign up"
   - Enter name, phone number or email, and password
   - Click "Sign Up"

2. **Log In**
   - Enter phone number/email and password
   - Click "Sign In"

3. **Book Tickets**
   - Navigate to booking page
   - Select available seats (green = available, red = selected, gray = booked)
   - Review price summary
   - Click "Confirm Booking"

4. **Process Payment**
   - Choose payment method (Online or Cash on Delivery)
   - Complete transaction

5. **View Bookings**
   - Click "My Bookings" to see all your reservations

### For Admin

1. **Login to Admin Panel**
   - Go to `http://127.0.0.1:5000/admin-login`
   - Username: `admin`
   - Password: `admin123`

2. **Access Admin Dashboard**
   - View system status
   - Manage bookings and users
   - Monitor transactions

## Default Credentials

### Admin Login
- **Username**: `admin`
- **Password**: `admin123`

## Important Notes

- **Data Storage**: User data and bookings are stored in memory and will be lost when the server restarts
- **Development Server**: The included Flask server is for development only. Use a production WSGI server (Gunicorn, uWSGI) for production deployment
- **Security**: Default admin credentials should be changed before production use

## Future Enhancements

- Database integration (SQLite, PostgreSQL)
- Email notifications
- Payment gateway integration
- Movie ratings and reviews
- Advanced search and filtering
- Multi-language support

## Support

For issues or questions, please check the server logs in the terminal where `app.py` is running.

---

**Last Updated**: January 24, 2026
**Version**: 1.0
