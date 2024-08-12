from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from models import db, User, Flight, Booking
from forms import LoginForm, SignupForm, SearchForm

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search_flights', methods=['GET', 'POST'])
@login_required
def search_flights():
    form = SearchForm()
    if form.validate_on_submit():
        flights = Flight.query.filter_by(departure_time=form.departure_time.data).all()
        return render_template('search_results.html', flights=flights)
    return render_template('search_flights.html', form=form)

@app.route('/book_flight', methods=['POST'])
@login_required
def book_flight():
    flight_id = request.form.get('flight_id')
    flight = Flight.query.get(flight_id)
    if flight and flight.available_seats > 0:
        booking = Booking(user_id=current_user.id, flight_id=flight.id, booking_time=datetime.now())
        flight.available_seats -= 1
        db.session.add(booking)
        db.session.commit()
        flash('Flight booked successfully!')
    else:
        flash('No available seats for this flight.')
    return redirect(url_for('my_bookings'))

@app.route('/my_bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

# Add other routes for admin functionality

if __name__ == '__main__':
    app.run(debug=True)
