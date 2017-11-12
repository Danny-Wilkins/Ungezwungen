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