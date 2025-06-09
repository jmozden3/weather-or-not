from flask import render_template, request, redirect, url_for, session
from app import app
from datetime import datetime, timedelta
import random
from flask import Flask

from app.weather import get_coordinates, get_weather_data, calculate_score
from app.holiday import get_holiday_fact

def get_random_date(start_year=1979):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

@app.route("/")
def index():
    city = request.args.get("city")
    date = request.args.get("date")
    if city and date:
        # Pre-fill session for challenge mode
        session["city"] = city
        session["date"] = date
        return redirect(url_for("game"))
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    city = request.form["city"]
    date = get_random_date()
    session["city"] = city
    session["date"] = date.strftime("%Y-%m-%d")
    return redirect(url_for("game"))

@app.route("/game")
def game():
    city = session.get("city")
    date = session.get("date")
    return render_template("game.html", city=city, date=date)

@app.route("/submit", methods=["POST"])
def submit():
    def convert_time_24_to_12(time_str):
        # Converts 'HH:MM' (24-hour) to 'h:mma' (e.g., '5:30am', '9:10pm')
        try:
            dt = datetime.strptime(time_str.strip(), "%H:%M")
            return dt.strftime("%I:%M%p").lstrip("0").lower()
        except Exception:
            return time_str

    user_data = {
        "high": int(request.form["high"]),
        "low": int(request.form["low"]),
        "rain": request.form["rain"].strip().lower(),
        "sunrise": convert_time_24_to_12(request.form["sunrise"].strip()),
        "sunset": convert_time_24_to_12(request.form["sunset"].strip())
    }

    city = session.get("city")
    date = session.get("date")

    lat, lon = get_coordinates(city)
    if lat is None:
        return "Sorry, couldn't find that city.", 400

    # Retry logic for missing weather data
    max_attempts = 5
    attempt = 0
    actual_data = None
    current_date = date
    while attempt < max_attempts:
        actual_data = get_weather_data(lat, lon, current_date)
        if actual_data is not None:
            break
        # Pick a new random date and update session
        new_date = get_random_date()
        current_date = new_date.strftime("%Y-%m-%d")
        session["date"] = current_date
        attempt += 1

    if actual_data is None:
        return "Weather data not available for that day/location.", 400

    score = calculate_score(user_data, actual_data)
    holiday = get_holiday_fact(current_date)

    return render_template(
        "result.html",
        score=score,
        actual=actual_data,
        user=user_data,
        city=city,
        date=current_date,
        holiday=holiday
    )

# Jinja2 filter for wordy date (e.g., August 10th, 1993)
def date_wordy(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1:'st',2:'nd',3:'rd'}.get(day%10, 'th')
        return dt.strftime(f"%B {day}{suffix}, %Y")
    except:
        return date_str

def holiday_wordy(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1:'st',2:'nd',3:'rd'}.get(day%10, 'th')
        return dt.strftime(f"%B {day}{suffix}")
    except:
        return date_str

app.jinja_env.filters['date_wordy'] = date_wordy
app.jinja_env.filters['holiday_wordy'] = holiday_wordy
