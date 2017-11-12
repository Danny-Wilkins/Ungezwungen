from itinerary_main import *
from sklearn.linear_model import LogisticRegression
from ml_lib import getInputVectors
import numpy as np
import webbrowser
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

numSamples = 10

def getAttractions():
	attractions = None
	while attractions is None:
		address = input("Enter an address: ")
		try:
			attractions = getAttractionsInArea(address)
			if len(attractions) <= numSamples:
				attractions = getAttractionsInArea(address, distance=TransportType.CAR)
			if len(attractions) <= numSamples:
				print("Not enough attractions in area. You can visit all {} attractions!.".format(len(attractions)))
				print("Please try another location.")
				attractions = None
		except Exception as ex:
			print("Invalid address. Try again.")
	return attractions

def demo():
	attractions = getAttractions()
	numAttractions = len(attractions)
	attributes = getInputVectors(attractions) 
	training_indices = np.random.choice(np.arange(numAttractions), size=numSamples, replace=False)
	testing_indices = np.array([i for i in np.arange(numAttractions) if i not in training_indices])
	training_samples = attributes[training_indices]
	
	labels = []
	for i in training_indices:
		name = attractions[i]['name'] 
		while True:
			userRating = input("Does {} interest you? ([y]es/[n]o/more [i]nfo) ".format(name))
			lowerRating = userRating.lower()
			#userRating = 'y' if np.random.random() > 0.5 else 'n'
			#print("Does {} interest you? (y/n) {}".format(name, userRating))
			if 'i' in lowerRating:
				url = attractions[i]['web_url']
				webbrowser.open(url)
			else:
				if 'y' in lowerRating:
					labels.append(1)
				elif 'n' in lowerRating:
					labels.append(0)
				else:
					print('Invalid input "{}"'.format(userRating))
					continue
				break

	labels = np.array(labels).reshape(numSamples)
	logistic = LogisticRegression()
	logistic.fit(training_samples, labels)
	would_like = []
	might_like = []
	wouldnt_like = []
	for i in range(numAttractions):
		label = '?'
		predictedLabel = logistic.predict(attributes[i])[0]
		name = attractions[i]['name']
		prob = logistic.predict_proba(attributes[i])[0][1]
		if i in training_indices:
			label = labels[np.where(training_indices==i)][0]
		# print('{} {} \n\tPredicted class {}, real class {}, prob {}'.format(i, 
		# 	name, \
		# 	predictedLabel, \
		# 	label,
		# 	prob))
		if label == 1 or (prob >= 0.6 and label != 0):
			would_like.append((prob, name))
		elif label != 0 and prob >= 0.4:
			might_like.append((prob, name))
		else:
			wouldnt_like.append(name)

	would_like.sort(reverse=True)
	might_like.sort(reverse=True)
	print("\nYou would like:")
	for prob, name in would_like:
		print('\t-{}'.format(name))
	print("\nYou might like:")
	for prob, name in might_like:
		print('\t-{}'.format(name))
	print("\nYou wouldn't like:")
	for name in wouldnt_like:
		print('\t-{}'.format(name))

if __name__ == "__main__":
	demo()
	
