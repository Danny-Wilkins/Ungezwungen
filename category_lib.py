from itinerary_main import *
from functools import reduce
import numpy as np
from sklearn.decomposition import PCA

def getCategories(attractions):
	cats = []
	for attraction in attractions:
		attraction_cats = set()
		groups = attraction["groups"]
		for group in groups:
			attraction_cats.add(group['name'])
			categories = group['categories']
			for category in categories:
				attraction_cats.add(category['name'])
		cats.append(attraction_cats)
	return cats

def reduceCategories(categories):
	return reduce((lambda x, y: x | y), categories)

def getCategoryVectors(attractions):
	categories = getCategories(attractions)
	allCategories = list(sorted(reduceCategories(categories)))
	catergoryVecs = []
	for i in range(len(categories)):
		vec = np.array([1 if cat in categories[i] else 0 for cat in allCategories])
		catergoryVecs.append(vec)
	return np.array(catergoryVecs)

def getPCACategoryVectors(attractions, n_components=6):
	categories = getCategories(attractions)
	vecs = getCategoryVectors(attractions)
	pca = PCA(n_components=n_components)
	pca.fit(vecs)
	return pca.transform(vecs)

if __name__ == "__main__":
	attractions = driver(location=LocationType.ATTRACTIONS)
	not_rest = filterRestaurants(attractions, restaurants=False)
	#print(json.dumps(not_rest, indent=4, sort_keys=True))
	pca_vecs = getPCACategoryVectors(not_rest)
	print(pca_vecs)
	


