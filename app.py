
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3
import os
import time
import base64
import numpy as np
import pandas as pd
import requests
import config
import pickle
import io
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import base64

forest = pickle.load(open('models/yield_rf.pkl', 'rb'))  # yield

model = pickle.load(open('models/classifier.pkl','rb'))
ferti = pickle.load(open('models/fertilizer.pkl','rb'))

cr = pickle.load(open('models/RandomForest.pkl', 'rb'))

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    print('vgj,hDS|m n')
    print(response)

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS seller(Id INTEGER PRIMARY KEY AUTOINCREMENT, crop TEXT, cost TEXT, district TEXT, image BLOB)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS buyer(Id INTEGER PRIMARY KEY AUTOINCREMENT, crop TEXT, cost TEXT, district TEXT, image BLOB)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS community_query(Id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, image BLOB, query TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS community_answer(query_id TEXT, username TEXT, answer TEXT)"""
cursor.execute(command)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            session['username'] = result[0]
            return redirect(url_for('market'))
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/fertilizer', methods=['GET', 'POST'])
def fertilizer():
    if request.method == 'POST':

        temp = request.form.get('temp')
        humi = request.form.get('humid')
        mois = request.form.get('mois')
        soil = request.form.get('soil')
        crop = request.form.get('crop')
        nitro = request.form.get('nitro')
        pota = request.form.get('pota')
        phosp = request.form.get('phos')
        input = [int(temp),int(humi),int(mois),int(soil),int(crop),int(nitro),int(pota),int(phosp)]

        res = ferti.classes_[model.predict([input])]
        print(f"RES   {res}")

        return render_template('fertilizer.html', prediction=res[0])
    else:
        return render_template('fertilizer.html', prediction="Something try again")

##    return render_template('fertilizer.html')

@app.route('/Yield', methods=['GET', 'POST'])
def Yield():
    if request.method == 'POST':
        state = request.form['stt']
        district = request.form['city']
        year = request.form['year']
        season = request.form['season']
        crop = request.form['crop']
        Temperature = request.form['Temperature']
        humidity = request.form['humidity']
        soilmoisture = request.form['soilmoisture']
        area = request.form['area']

        out_1 = forest.predict([[float(state),
                                 float(district),
                                 float(year),
                                 float(season),
                                 float(crop),
                                 float(Temperature),
                                 float(humidity),
                                 float(soilmoisture),
                                 float(area)]])
        return render_template('yield.html', prediction=out_1[0])

    return render_template('yield.html')

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        N = request.form['nitrogen']
        P = request.form['phosphorous']
        K = request.form['pottasium']
        ph = request.form['ph']
        rainfall = request.form['rainfall']
        temp = request.form['temperature']
        hum = request.form['humidity']
##        state = request.form['stt']
##        city = request.form['city']

##        if weather_fetch(city) != None:
##            temperature, humidity = weather_fetch(city)
        data = np.array([[N, P, K, temp, hum, ph, rainfall]])
        my_prediction = cr.predict(data)
        final_prediction = my_prediction[0]

        return render_template('crop.html', p_result=final_prediction)
##        else:
##            return render_template('crop.html', msg="Some thing went wrong, try again")

    return render_template('crop.html')

@app.route('/buyer')
def buyer():
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        cursor.execute("select * from seller")
        result = cursor.fetchall()

        if result:
            profile = []
            for row in result:
                profile.append(row[-1])

            return render_template('buyer.html', result=result, profile=profile)
        else:
            return render_template('buyer.html')

@app.route('/sell_crop', methods=['POST', 'GET'])
def sell_crop():
    if request.method == 'POST':
        crop = request.form['crop']
        cost = request.form['cost']
        dist = request.form['dist']
        file = request.files['file']
        filename = file.filename
        print(filename)
        file_content = file.read()
        File = base64.b64encode(file_content).decode('utf-8')

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO seller (crop, cost, district, image) VALUES (?,?,?,?)",[crop, cost, dist, File])
        connection.commit()

        return render_template('seller.html', msg="data uploaded successfully")

    return render_template('seller.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        try:
            city = request.form['city']
            # creating url and requests instance
            url = "https://www.google.com/search?q="+"weather"+city
            html = requests.get(url).content

            # getting raw data
            soup = BeautifulSoup(html, 'html.parser')
            temp1 = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

            # formatting data
            data = str.split('\n')
            Time = data[0]
            sky = data[1]

            # printing all data
            print("Temperature is", temp1)
            print("Time: ", Time)
            print("Sky Description: ", sky)

            temp = temp1

            temp = temp.replace('°C', '')
            temp = int(temp)

            rem = "Temperature is {} degree celcius, Time is {}, Sky Description is {}".format(temp, Time, sky) 
            
            print(rem)
            return render_template('weather.html', city=city, temp=temp, time=Time, sky=sky)
        except:
            return render_template('weather.html', msg="Try again")
    return render_template('weather.html')

@app.route('/market')
def market():
    url = "https://www.napanta.com/market-price/karnataka/bangalore/bangalore"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with class "table table-bordered table-striped"
    table = soup.find("table")
    if table:
        result = [['Commodity', 'Variety', 'Maximum Price',	'Average Price', 'Minimum Price', 'Last Updated On']]
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if cells:
                d = [cell.get_text(strip=True) for cell in cells]
                result.append(d[:-1])
    return render_template('market.html', result=result)

@app.route('/FAQ')
def FAQ():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute("select * from community_query")
    result = cursor.fetchall()
    if result:
        rows = []
        for row in result:
            cursor.execute("select * from community_answer where query_id = '"+str(row[0])+"'")
            result1 = cursor.fetchall()
            if result1:
                    rows.append([row[0], row[1], row[3], "data:image/jpeg;base64,"+row[2], result1])
            else:
                rows.append([row[0], row[1], row[3], "data:image/jpeg;base64,"+row[2], []])
        return render_template('community.html', rows = rows)
    return render_template('community.html', msg="FAQ not found")

@app.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        try:
            file = request.files['file']
            filename = file.filename
            print(filename)
            file_content = file.read()
            File = base64.b64encode(file_content).decode('utf-8')
        except:
            with open('demo.png', 'rb') as file:
                image_data = file.read()
                File = base64.b64encode(image_data).decode('utf-8')
        
        query = request.form['qn']
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO community_query (username, image, query) VALUES (?,?,?)",[session['username'], File, query])
        connection.commit()

        return redirect(url_for('FAQ'))
    return redirect(url_for('FAQ'))

@app.route('/answers', methods=['GET', 'POST'])
def answers():
    if request.method == 'POST':
        ID = request.form['ID']
        ansr = request.form['ansr']

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO community_answer (query_id, username, answer) VALUES (?,?,?)",[ID, session['username'], ansr])
        connection.commit()

        return redirect(url_for('FAQ'))
    return redirect(url_for('FAQ'))

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
