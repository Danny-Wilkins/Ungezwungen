from itinerary_main import *
import category_lib
import review_lib
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def getInputVectors(attractions):
	numAttractions = len(attractions)
	ones = np.ones(numAttractions).reshape((numAttractions, 1))
	categoryVectors = category_lib.getPCACategoryVectors(attractions)
	reviewVectors = review_lib.getPCAReviewWordVectors(attractions)
	return np.concatenate((ones, 
						   categoryVectors, 
						   reviewVectors),
						   axis = 1 )

if __name__ == "__main__":
	attractions = driver(location=LocationType.ATTRACTIONS)
	numAttractions = len(attractions)
	numSamples = 10
	attributes = getInputVectors(attractions) 
	training_indices = np.random.choice(np.arange(numAttractions), size=numSamples, replace=False)
	testing_indices = np.array([i for i in np.arange(numAttractions) if i not in training_indices])
	training_samples = attributes[training_indices]
	
	labels = []
	for i in range(numAttractions):
		if i in training_indices:
			name = attractions[i]['name'] 
			#print(name, attributes[i], sep='\n', end = '\n\n')
			userRating = input("Does {} interest you? (y/n)".format(name)).lower()
			#userRating = 'y' if np.random.random() > 0.5 else 'n'
			print(name, userRating)
			if userRating == 'y':
				labels.append(1)
			else:
				labels.append(0)
	labels = np.array(labels).reshape(numSamples)
	logistic = LogisticRegression()
	logistic.fit(training_samples, labels)
	would_like = []
	wouldnt_like = []
	for i in range(len(attributes)):
		label = '?'
		predictedLabel = logistic.predict(attributes[i])[0]
		name = attractions[i]['name']
		if i in training_indices:
			label = labels[np.where(training_indices==i)][0]
		print('{} {} \n\tPredicted class {}, real class {}'.format(i, 
			name, \
			predictedLabel, \
			label))
		if predictedLabel == 1 and label != 0:
			would_like.append(name)
		else:
			wouldnt_like.append(name)

	print("You would like: {}".format('\n\t-'.join(would_like)))
	print()
	print("You wouldn't like: {}".format('\n\t-'.join(wouldnt_like)))

