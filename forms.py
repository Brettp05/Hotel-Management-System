from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        from models import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class BookingForm(FlaskForm):
    check_in_date = DateField('Check-in Date', validators=[DataRequired()])
    check_out_date = DateField('Check-out Date', validators=[DataRequired()])
    num_guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1, max=10)])
    special_requests = TextAreaField('Special Requests', render_kw={"rows": 4})
    submit = SubmitField('Book Now')

    def validate_check_out_date(self, field):
        if field.data <= self.check_in_date.data:
            raise ValidationError('Check-out date must be after check-in date.')

    def validate_check_in_date(self, field):
        if field.data < date.today():
            raise ValidationError('Check-in date cannot be in the past.')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], 
                        validators=[DataRequired()], coerce=int)
    title = StringField('Review Title', validators=[DataRequired(), Length(min=5, max=100)])
    comment = TextAreaField('Your Review', validators=[DataRequired(), Length(min=10, max=1000)], 
                           render_kw={"rows": 5})
    submit = SubmitField('Submit Review')

class HotelSearchForm(FlaskForm):
    query = StringField('Search', render_kw={"placeholder": "Search hotels, cities..."})
    city = StringField('City', render_kw={"placeholder": "Enter city"})
    check_in = DateField('Check-in')
    check_out = DateField('Check-out')
    guests = IntegerField('Guests', validators=[NumberRange(min=1, max=10)], default=1)
    submit = SubmitField('Search')
