#key: 521d44db-20a6-45f9-9f25-836918a17934
import requests
import json
import numpy as np
import random
from scipy import stats
from geopy.geocoders import Nominatim
from flask import Flask
from flask import render_template

app = Flask(__name__)

API_KEY =  "521d44db-20a6-45f9-9f25-836918a17934"

class TransportType:
    WALKING = 2
    BIKING = 5
    CAR = 20
    #Public transportation is weird because we need to factor in dropoff locations
    #BUS = ???
    #SUBWAY = ???

class LocationType:
    ATTRACTIONS = 'attractions'
    RESTAURANTS = 'restaurants'

def main():
    #values = driver()
    
    #print(values)
    pass
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<address>')
def driver(address, location=LocationType.ATTRACTIONS):
    #location = input("Please enter an address: ")
    return render_template('suggestions.html')
    #In the end, if this fails, it would be best to direct to a "failed to find address" page. From there, this can all be called again from the top. No loops or anything.
    '''while True:
        try:
            pass
            #return str(getPlacesInArea(address, 9, 18, 100, location, TransportType.WALKING))
            #attractions = getPlacesInArea(address, 9, 18, 100, location, TransportType.WALKING)
            #dump = getAttractionsReviews(attractions)
            #indexById = {attraction['location_id']: attraction for attraction in attractions}
            #prettyPrint([[item[thing] for thing in item] for item in attractions])
            #innerDump = [place[0] if len(place) > 0 else "" for place in dump]
            #prettyPrint(dump)
            #prettyPrint(indexById["7008030"]['name'])
            #print(indexById['4303229']['name'])
            #[[review['text'] for review in place] for place in dump]
            #print(j[0]['data'][0]['text'])
            #return render_template('results.html', address=address, attractions=indexById, reviews=innerDump)
            #showSuggestions(innerDump)
        except Exception as e:
            print("Address not found. Please enter a different location.")
            print(e)
            #address = input("Please enter an address: ")'''
#End goal is to fill parameters in using forms on the front end

def getAttractionsInArea(address, distance=TransportType.WALKING):
    return getPlacesInArea(address, 9, 18, 100, distance=TransportType.WALKING, location=LocationType.ATTRACTIONS)

def prettyPrint(js):
    print(json.dumps(js, indent=4, sort_keys=True))

def getPlacesInArea(address, start_time, end_time, price_range, location=LocationType.RESTAURANTS, distance=TransportType.WALKING):
    try:
        loc = geolocator(address)
    except Exception as e:
        raise e

    #print(location)
    
    request_url = ('https://api.tripadvisor.com/api/partner/2.0/map/{0},{1}/{2}' \
            + '?key={3}&distance={4}').format(loc['lat'], loc['lng'], location, API_KEY, distance)
    
    return requests.get(request_url).json()['data']

def isRestaurant(attraction):
    return attraction['category'] == LocationType.RESTAURANTS


def filterRestaurants(dump, restaurants=True):
    return [attraction for attraction in dump \
            if isRestaurant(attraction) == restaurants]

def getAttractionsReviews(attractions):
    return [getReviews(attraction) for attraction in attractions]

def getReviews(attraction):
    locationId = attraction["location_id"]
    request_url = 'https://api.tripadvisor.com/api/partner/2.0/location/{0}/reviews?key={1}'\
        .format(locationId, API_KEY)
    return requests.get(request_url).json()['data']

def geolocator(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    print(location.address)

    return {'lat':location.latitude, 'lng':location.longitude}

if __name__ == '__main__':
	main()
