#!C:\Users\Lenovo\AppData\Local\Programs\Python\Python37-32\python.exe

from flask import Blueprint, render_template, request, redirect, url_for
from weather_app.utils import main_funcs
from flask import Flask, render_template, request
import requests
import json
from weather_app import db
from weather_app.models import weather_model
import datetime
import pickle
from flask import flash
import numpy as np



bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


key = '586f4e3658eec1d5c3596fe660841cff'
url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=" + key

@bp.route('/weather', methods=["POST","GET"])
def weather_index():
    if request.method == "POST":
        new_city = request.form.get("city")
        new_city_new = requests.get(url.format(new_city)).json()
        # breakpoint()
        if new_city_new:
            new_city_obj = weather_model.City(name=new_city,
                                              temperature=new_city_new["main"]["temp"],
                                              description=new_city_new["weather"][0]["description"].capitalize())
            db.session.add(new_city_obj)
            db.session.commit()

    cities = weather_model.City.query.all()
    weather_data = []
    weather = dict()

    for city in cities:
        response = requests.get(url.format(city.name)).json()
        if response["cod"] == "404":
            city_obj = weather_model.City.query.filter_by(name=city.name).first()
            db.session.delete(city_obj)
            db.session.commit()
        else:
            weather = {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "city": city.name,
                "temperature": response["main"]["temp"],
                "description": response["weather"][0]["description"].capitalize(),
                "icon": response["weather"][0]["icon"],
            }
            weather_data.append(weather)
    return render_template("weather.html", weather_data=weather_data)

@bp.route("/delete", methods=["POST"])
def delete():
    citytitle = request.form.get("citytitle")
    city = weather_model.City.query.filter_by(name=citytitle).first()
    db.session.delete(city)
    db.session.commit()
    flash(f'Successfully deleted {city.name}!', 'success')
    return redirect(url_for("main.weather_index"))



@bp.route("/login")
def login_index():
    return render_template("login.html")


@bp.route('/fire')
def hello_world():
    return render_template("fire.html")

@bp.route("/predict",methods=["POST","GET"])
def predict():
    model = pickle.load(open('weather_app/routes/model.pkl', 'rb'))
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)

    if output>str(0.8):
        return render_template('fire.html',pred='산불이 발생할 확률 {}% \n'
                                                '주의수준😡'.format(int(float(output)*100)))
    elif output>str(0.3):
        return render_template('fire.html',pred='산불이 발생할 확률 {}% \n'
                                                '경계수준😞'.format(int(float(output)*100)))
    elif output<str(0.2):
        return render_template('fire.html', pred='산불이 발생할 확률 {}% \n'
                                                 '안전수준☺️ '.format(int(float(output)*100)))
