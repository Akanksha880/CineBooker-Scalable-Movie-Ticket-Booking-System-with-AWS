from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'templates', 'static'))
app.secret_key = "cinebooker_secret"

# In-memory storage (LOCAL DEPLOYMENT)
users = []
bookings = []
payments = []
booking_counter = 1
payment_counter = 1

print("=" * 50)
print("[*] CineBooker App Started")
print("=" * 50)
print("[+] Ready to accept new users!")
print("=" * 50)

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = generate_password_hash(request.form["password"]) 

        # Validate that at least email or phone is provided
        if not email and not phone:
            flash("Please provide either email or phone number")
            return redirect(url_for("signup"))

        # Check for duplicate email
        if email:
            for user in users:
                if user.get("email") == email:
                    flash("Email already exists")
                    return redirect(url_for("signup"))

        # Check for duplicate phone
        if phone:
            for user in users:
                if user.get("phone") == phone:
                    flash("Phone number already exists")
                    return redirect(url_for("signup"))

        users.append({
            "id": len(users) + 1,
            "name": name,
            "email": email,
            "phone": phone,
            "password": password
        })

        print("[+] Current Users List:", users)
        flash("Signup successful. Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    email_or_phone = request.form.get("email_or_phone", "").strip()
    password = request.form.get("password", "").strip()

    print(f"\n[LOGIN_ATTEMPT]")
    print(f"   Input: {email_or_phone}")
    print(f"   Password entered: {password}")
    print(f"   Total users in system: {len(users)}")
    
    for user in users:
        print(f"\n   Checking user: {user['name']}")
        print(f"      Email on file: {user.get('email')}")
        print(f"      Phone on file: {user.get('phone')}")
        
        # Check if login is with email or phone
        email_match = user.get("email") == email_or_phone
        phone_match = user.get("phone") == email_or_phone
        password_match = check_password_hash(user["password"], password)
        
        print(f"      Email matches: {email_match}")
        print(f"      Phone matches: {phone_match}")
        print(f"      Password matches: {password_match}")
        
        if (email_match or phone_match) and password_match:
            session["user"] = {
                "id": user["id"],
                "name": user["name"],
                "email": user.get("email", ""),
                "phone": user.get("phone", "")
            }
            print(f"\n[LOGIN_SUCCESS]: {user['name']}")
            print(f"   Session: {session['user']}\n")
            return redirect(url_for("home"))

    print(f"\n[LOGIN_FAILED]: Invalid credentials\n")
    flash("Invalid email/phone or password")
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("home1.html")

@app.route("/b1")
def book():
    if "user" not in session:
        return redirect(url_for("index"))
    
    movie = request.args.get("movie", "")
    theater = request.args.get("theater", "")
    
    # Get all booked seats for this movie/theater
    booked_seats = []
    for booking in bookings:
        if booking["movie"] == movie and booking["theater"] == theater:
            seats = booking["seats"].split(",") if booking["seats"] else []
            booked_seats.extend(seats)
    
    return render_template("b1.html", booked_seats=booked_seats, movie=movie, theater=theater)

@app.route("/my-bookings")
def my_bookings():
    if "user" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user"]["id"]
    user_bookings = [b for b in bookings if b["user_id"] == user_id]
    
    # Get payment info for each booking
    for booking in user_bookings:
        booking["payment_info"] = None
        for payment in payments:
            if payment["booking_id"] == booking["booking_id"]:
                booking["payment_info"] = payment
                break
    
    print(f"\n[+] Fetching bookings for user {user_id}")
    print(f"   Total bookings: {len(user_bookings)}")
    
    return render_template("bookings.html", bookings=user_bookings)

@app.route("/tickets", methods=["POST"])
def tickets():
    global booking_counter

    seats = request.form.get("seats", "").split(",") if request.form.get("seats") else []
    num_seats = len(seats)
    price_per_seat = int(request.form["price"])
    total_price = num_seats * price_per_seat

    booking = {
        "booking_id": booking_counter,
        "user_id": session["user"]["id"],
        "movie": request.form["movie"],
        "theater": request.form["theater"],
        "seats": ",".join(seats),
        "num_seats": num_seats,
        "price_per_seat": price_per_seat,
        "total_price": total_price,
        "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    bookings.append(booking)
    booking_counter += 1

    print("[+] Booking Added:", booking)
    print("[+] All Bookings:", bookings)

    return render_template("tickets.html", booking=booking)

@app.route("/process-payment", methods=["POST"])
def process_payment():
    global payment_counter

    if "user" not in session:
        return redirect(url_for("index"))

    booking_id = int(request.form["booking_id"])
    total_price = int(request.form["total_price"])
    payment_method = request.form.get("payment_method")
    payment_option = request.form.get("payment_option")

    # Find the booking
    booking = None
    for b in bookings:
        if b["booking_id"] == booking_id:
            booking = b
            break

    if not booking:
        flash("Booking not found")
        return redirect(url_for("home"))

    # Process payment based on method
    if payment_method == "online":
        payment_status = "completed"
        payment_desc = payment_option.upper() if payment_option == "paytm" else "Google Pay"
    elif payment_method == "cod":
        payment_status = "pending"
        payment_desc = "Cash"
    else:
        flash("Invalid payment method")
        return redirect(url_for("home"))

    # Create payment record
    payment = {
        "payment_id": payment_counter,
        "booking_id": booking_id,
        "user_id": session["user"]["id"],
        "payment_method": payment_desc,
        "payment_option": payment_option if payment_option else "N/A",
        "total_price": total_price,
        "payment_status": payment_status,
        "payment_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "movie": booking["movie"],
        "theater": booking["theater"],
        "seats": booking["seats"]
    }

    payments.append(payment)
    booking["payment_id"] = payment_counter
    booking["payment_status"] = payment_status
    payment_counter += 1

    print("[+] Payment Processed:", payment)
    print("[+] All Payments:", payments)

    return render_template("payment.html", payment=payment)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully")
    return redirect(url_for("login"))

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    if username == "admin" and password == "admin123":
        session["admin"] = True
        flash("Admin login successful")
        return redirect(url_for("admin_dashboard"))
    flash("Invalid admin credentials")
    return redirect(url_for("admin_login"))

@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    return render_template("admin_dashboard.html")

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin", None)
    flash("Admin logged out")
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
