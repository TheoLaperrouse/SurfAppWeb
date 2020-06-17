import http.client
import json
import csv
import os
from os import system, path
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

jsonToSend = {}
jsonToSend['spots'] = []


def getScore(json, directionVent):
    score = 0
    if json['maree'] == 'Montante':
        score += 3
    if json['houle'] > 1.0:
        score += 10
    elif json['houle'] > 0.5:
        score += 7
    if json['periode'] > 11:
        score += 3
    elif json['periode'] > 8:
        score += 1
    if json['tempEau'] > 16:
        score += 3
    elif json['tempEau'] > 12:
        score += 1
    if json['tempExt'] > 20:
        score += 3
    elif json['tempExt'] > 12:
        score += 1
    if json['vitesseVent'] > 30:
        score -= 1
    elif json['vitesseVent'] > 40:
        score -= 3
    score += directionVentScore(json['directionVent'], directionVent)
    return score


def directionVentScore(directionVentSpot, directionVent):
    if(directionVentSpot == 'Nord'):
        if directionVent in ['N', 'NNE', 'NNO']:
            return 3
        elif directionVent in ['NO', 'ONO', 'NE', 'ENE']:
            return 1
    elif(directionVentSpot == 'Sud'):
        if directionVent in ['S', 'SSE', 'SSO']:
            return 3
        elif directionVent in ['SO', 'OSO', 'SE', 'ESE']:
            return 1
    elif(directionVentSpot == 'Ouest'):
        if directionVent in ['ONO', 'O', 'OSO']:
            return 3
        elif directionVent in ['NO', 'SO', 'NNO', 'SSO']:
            return 1
    elif(directionVentSpot == 'Est'):
        if directionVent in ['E', 'ENE', 'ESE']:
            return 3
        elif directionVent in ['NE', 'SE', 'SSE', 'NNE']:
            return 1
    if(directionVentSpot == 'Nord-Ouest'):
        if directionVent in ['NO', 'NNO', 'ONO']:
            return 3
        elif directionVent in ['O', 'N', 'NNE', 'OSO']:
            return 1
    elif(directionVentSpot == 'Nord-Est'):
        if directionVent in ['ENE', 'NNE', 'NE']:
            return 3
        elif directionVent in ['N', 'E', 'NNO', 'ESE']:
            return 1
    elif(directionVentSpot == 'Sud-Ouest'):
        if directionVent in ['SO', 'SSO', 'OSO']:
            return 3
        elif directionVent in ['O', 'ONO', 'S', 'SSE']:
            return 1
    elif(directionVentSpot == 'Sud-Est'):
        if directionVent in ['SE', 'SSE', 'ESE']:
            return 3
        elif directionVent in ['ENE', 'SSO', 'S', 'E']:
            return 1
    return 0


def sendMail(previsionSurf):
    gmail_user = 'theolaperrousesendmail@gmail.com'
    gmail_password = 'sendmail35235'
    receveir = 'theolaperrouse@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = 'theolaperrouse@gmail.com'
    msg['Subject'] = 'Prévision Sessions Surf pour la semaine'
    body = previsionSurf
    body = MIMEText(body)
    msg.attach(body)
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, receveir, msg.as_string())
    server.close()


def addSpot(spotToAdd):
    with open('./serveur/spots.json', "r") as file:
        data = json.load(file)
        data['spots'].append(spotToAdd)
    with open('./serveur/spots.json', 'w') as file:
        json.dump(data, file, indent=4)


def serverResponse(posLocation, nom_spot, directionVent):
    conn = http.client.HTTPSConnection('api.worldweatheronline.com')
    payload = ""
    parameters = f"/premium/v1/marine.ashx?q={posLocation}&key=5b4541479ee849d29a8152452202505&lang=fr&format=json&tide=yes&tp=3&num_of_days=7"
    conn.request("GET", parameters, payload)
    res = conn.getresponse().read()
    infosMeteo = json.loads(res)
    parseResponse(infosMeteo, nom_spot, directionVent)
    return jsonToSend


def parseResponse(infos, spot, directionVent):
    spot.replace('%20', ' ')
    semaineMeteo = infos['data']['weather']
    for jour in semaineMeteo:
        for hours in jour['hourly']:
            jsonWeatherInfo = {}
            jsonWeatherInfo['location'] = spot
            jsonWeatherInfo['date'] = getJour(jour['date'])
            jsonWeatherInfo['hours'] = getHour(hours['time'])
            jsonWeatherInfo['directionVent'] = hours['winddir16Point']
            jsonWeatherInfo['vitesseVent'] = float(hours['windspeedKmph'])
            jsonWeatherInfo['tempExt'] = float(hours['tempC'])
            jsonWeatherInfo['maree'] = getTypeMaree(
                jsonWeatherInfo['hours'], jour['tides'][0])
            jsonWeatherInfo['tempEau'] = float(hours['waterTemp_C'])
            jsonWeatherInfo['valueWeather'] = hours['lang_fr'][0]['value']
            jsonWeatherInfo['houle'] = float(hours['swellHeight_m'])
            jsonWeatherInfo['periode'] = float(hours['swellPeriod_secs'])
            score = getScore(jsonWeatherInfo, directionVent)
            if score > 11:
                jsonWeatherInfo['score'] = score
                jsonToSend['spots'].append(jsonWeatherInfo)


# Ajouter taille des marées : Grand Coeff = Bien --> tide['tideHeight_mt']
def getTypeMaree(hour, tides):
    tidesDay = tides['tide_data']
    heurePrevision = datetime.datetime.strptime(hour, '%H:%M')
    for tide in tidesDay:
        heureMaree = datetime.datetime.strptime(tide['tideTime'], '%I:%M %p')
        if heurePrevision > heureMaree:
            if (tide['tide_type'] == 'HIGH'):
                return 'descendante'
            else:
                return 'montante'


def getHour(hour):
    if(len(hour) == 0 or len(hour) == 3):
        return datetime.datetime.strptime(hour[0], '%H').strftime('%H:%M')
    else:
        return datetime.datetime.strptime(hour[:2], '%H').strftime('%H:%M')


def getJour(date):
    DayWeek = ['Lundi', 'Mardi', 'Mercredi',
               'Jeudi', 'Vendedi', 'Samedi', 'Dimanche']
    Month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
             'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    dateTime = datetime.datetime.strptime(date, ('%Y-%m-%d'))
    nomJour = DayWeek[dateTime.weekday()]
    nomMois = Month[dateTime.month-1]
    return f'{nomJour} {dateTime.day} {nomMois}'
