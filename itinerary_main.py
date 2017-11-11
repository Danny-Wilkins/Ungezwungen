#key: 521d44db-20a6-45f9-9f25-836918a17934
import requests
import json
import numpy as np
from scipy import stats
from geopy.geocoders import Nominatim
from flask import Flask
from flask import render_template

app = Flask(__name__)

API_KEY =  "521d44db-20a6-45f9-9f25-836918a17934"

class TransportType:
    WALKING = 2
    BIKING = 5
    CAR = 10
    #Public transportation is weird because we need to factor in dropoff locations
    #BUS = ???
    #SUBWAY = ???

class LocationType:
    ATTRACTIONS = 'attractions'
    RESTAURANTS = 'restaurants'

def main():
    values = driver()
    
    print(values)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<location>')
def driver(location=LocationType.RESTAURANTS):
    #location = input("Please enter an address: ")

    #In the end, if this fails, it would be best to direct to a "failed to find address" page. From there, this can all be called again from the top. No loops or anything.
    while True:
        try:
            return getPlacesInArea(address, 9, 18, 100, distance=TransportType.WALKING, location=location)
        except Exception as e:
            print("Address not found. Please enter a different location.")
            print(e)
            address = input("Please enter an address: ")
#End goal is to fill parameters in using forms on the front end

def getPlacesInArea(address, start_time, end_time, price_range, location=LocationType.RESTAURANTS, distance=TransportType.WALKING):
	
    try:
        loc = geolocator(address)
    except Exception as e:
        raise e
    
    request_url = ('https://api.tripadvisor.com/api/partner/2.0/map/{},{}/{}' \
            + '?key={}&distance={}').format(loc['lat'], loc['lng'], location, API_KEY, distance)
    
    return requests.get(request_url).json()['data']

def isRestaurant(attraction):
    return attraction['category'] == LocationType.RESTAURANTS

def filterRestaurants(dump, restaurants=True):
    return [attraction for attraction in dump \
            if isRestaurant(attraction) == restaurants]

def getReviews(attraction):
    locationId = attraction["location_id"]
    request_url = 'https://api.tripadvisor.com/api/partner/2.0/location/{0}/reviews?key={1}'\
        .format(locationId, API_KEY)
    return requests.get(request_url).json()

def geolocator(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    print(location.address)

    return {'lat':location.latitude, 'lng':location.longitude}

if __name__ == '__main__':
	main()
