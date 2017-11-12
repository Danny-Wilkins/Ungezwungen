from itinerary_main import *
import json

attractions = driver(location=LocationType.ATTRACTIONS)
not_rest = filterRestaurants(attractions, restaurants=False)
reviews = [getReviews(attraction) for attraction \
		in not_rest]

print(json.dumps(reviews, indent=4, sort_keys=True))