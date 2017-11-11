#key: 521d44db-20a6-45f9-9f25-836918a17934
import requests
import json
import operator
import numpy as np
from scipy import stats
from geopy.geocoders import Nominatim
from flask import Flask
from flask import render_template

app = Flask(__name__)

API_KEY =  "521d44db-20a6-45f9-9f25-836918a17934"

class transportation:
    WALKING = 2
    BIKING = 5
    CAR = 10
    #Public transportation is weird because we need to factor in dropoff locations
    #BUS = ???
    #SUBWAY = ???

def main():
    values = driver()
    
    #print(values)
    for i in values:
        print(i[0], i[1][0], i[1][1])
        
    #print json.dumps(r.json(), indent=4, sort_keys=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<location>')
def driver(location):
    #location = input("Please enter an address: ")

    #In the end, if this fails, it would be best to direct to a "failed to find address" page. From there, this can all be called again from the top. No loops or anything.

    while True:
        try:
            return getPlacesInArea(location, 9, 18, 100, transportation.WALKING)
        except Exception as e:
            print("Address not found. Please enter a different location.")
            print(e)
            address = input("Please enter an address: ")
#End goal is to fill parameters in using forms on the front end

def getPlacesInArea(address, start_time, end_time, price_range, distance=transportation.WALKING): 

    try:
        loc = geolocator(address)
    except Exception as e:
        raise e
        
    r = requests.get('https://api.tripadvisor.com/api/partner/2.0/map/{},{}/restaurants?key={}&distance={}'.format(loc['lat'], loc['lng'], API_KEY, distance))
    
    return #json.dumps(r.json(), indent=4, sort_keys=True)

def geolocator(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    print(location.address)

    #print location.latitude, location.longitude

    return {'lat':location.latitude, 'lng':location.longitude}

if __name__ == '__main__':
	main()
