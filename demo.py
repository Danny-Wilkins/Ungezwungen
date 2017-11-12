from itinerary_main import *
from sklearn.linear_model import LogisticRegression
from ml_lib import getInputVectors
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

np.random.seed(0)

def getAttractions():
	attractions = None
	while attractions is None:
		address = input("Enter an address: ")
		try:
			attractions = getAttractionsInArea(address)
		except Exception as ex:
			#print(ex)
			print("Invalid address. Try again.")
	return attractions

def demo():
	attractions = getAttractions()
	numAttractions = len(attractions)
	numSamples = 10
	attributes = getInputVectors(attractions) 
	training_indices = np.random.choice(np.arange(numAttractions), size=numSamples, replace=False)
	testing_indices = np.array([i for i in np.arange(numAttractions) if i not in training_indices])
	training_samples = attributes[training_indices]
	
	labels = []
	for i in training_indices:
		name = attractions[i]['name'] 
		#print(name, attributes[i], sep='\n', end = '\n\n')
		userRating = input("Does {} interest you? (y/n)".format(name)).lower()
		#userRating = 'y' if np.random.random() > 0.5 else 'n'
		#print(name, userRating)
		if userRating.lower()[0] == 'y':
			labels.append(1)
		else:
			labels.append(0)
	labels = np.array(labels).reshape(numSamples)
	#print(training_indices)
	#print(labels)
	logistic = LogisticRegression()
	logistic.fit(training_samples, labels)
	would_like = []
	wouldnt_like = []
	for i in range(numAttractions):
		label = '?'
		predictedLabel = logistic.predict(attributes[i])[0]
		name = attractions[i]['name']
		prob = logistic.predict_proba(attributes[i])[0][1]
		if i in training_indices:
			#print(np.where(training_indices==i))
			label = labels[np.where(training_indices==i)][0]
		print('{} {} \n\tPredicted class {}, real class {}, prob {}'.format(i, 
			name, \
			predictedLabel, \
			label,
			prob))
		if label == 1 or (predictedLabel == 1 and label != 0):
			would_like.append((prob, name))
		else:
			wouldnt_like.append(name)

	would_like.sort(reverse=True)
	print("You would like:")
	for prob, name in would_like:
		print('\t-{}'.format(name))
	print("")
	print("You wouldn't like:")
	for name in wouldnt_like:
		print('\t-{}'.format(name))

if __name__ == "__main__":
	demo()
	
