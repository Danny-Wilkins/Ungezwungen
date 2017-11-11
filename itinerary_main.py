#key: 521d44db-20a6-45f9-9f25-836918a17934
import requests
import json
import operator
import numpy as np
from scipy import stats
from geopy.geocoders import Nominatim

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
    
    print(values)
    
    '''for i in values:
		print i[0], i[1][0], i[1][1]'''
        
    #print json.dumps(r.json(), indent=4, sort_keys=True)

def driver():
    address = input("Please enter an address: ")
    while True:
        try:
            return getPlacesInArea(address, 9, 18, 100, transportation.WALKING)
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
    
    print(json.dumps(r.json(), indent=4, sort_keys=True))

    '''
    #print json.dumps(r.json(), indent=4, sort_keys=True)
    js = r.json()
    
    print js

    prices = []
    ratings = []    
    for item in js['data']:
    	if(item['price_level'] == None):
    		continue    
    	prices.append(float(len(item['price_level'])))
    	ratings.append(float(item['rating']))   
    prices = np.array(prices)
    ratings = np.array(ratings) 
    try:
    	slope, intercept, r_value, p_value, std_err = stats.linregress(prices, ratings)
    except:
    	print "No restaurants found nearby. Please try again."
    	return getRestaurantsInArea(raw_input("Enter address: "))
    
    #print slope, intercept, r_value, p_value, std_err  
    values = {} 
    for item in js['data']:
    	if(item['price_level'] == None):
    		continue    
    	#print item['name'], value(item, slope, intercept)
    	v = value(item, slope, intercept)   
    	values[item['name']] = (round(v, 3), grade(v))  
    values = sorted(values.items(), key=operator.itemgetter(1), reverse=True)   
    return values
    '''

def geolocator(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    print(location.address)

    #print location.latitude, location.longitude

    return {'lat':location.latitude, 'lng':location.longitude}


if __name__ == '__main__':
	main()
