import nltk
import json
from itinerary_main import *
import numpy as np
from sklearn.decomposition import PCA

# returns tuples of (location_id, helpful_votes, rating, essence)
def extractReviewInfo(attractions):
    reviews = [getReviews(attraction) for attraction \
        in attractions]

    useful_info = []

    for place in reviews:
        reviews_info = []
        for review in place:
            location_id = review['location_id']
            helpful_votes = review['helpful_votes']
            rating = review['rating']
            text = review['text']
            lang = review['lang']
            if (lang == 'en'):
                text = text.encode("ascii", errors="ignore").decode()
                text = nltk.word_tokenize(text)
                tokenized = nltk.pos_tag(text)
                essence = {}
                for word, pos in tokenized:
                    if (pos in ('NNP', 'NN', 'NNPS', 'NNS', 'JJ', 'JJR', 'JJS')):
                        if (pos != 'NNP' or pos != 'NNPS'):
                            word = word.lower()

                        if (essence.get(word) == None):
                            essence[word] = 1
                        else:
                            essence[word] += 1

                reviews_info.append((location_id, helpful_votes, rating, essence))
        useful_info.append(reviews_info)
    return useful_info

def getReviewWordVectors(attractions):
    reviewInfo = extractReviewInfo(attractions)
    vocabulary = set()
    for place in reviewInfo:
        for _, _, _, reviewWords in place:
            vocabulary |= set(reviewWords.keys())
    sorted_vocab = sorted(list(vocabulary))
    vecs = []
    for place in reviewInfo:
        place_vecs = []
        for locationId, _, _, reviewWords in place:
            reviewVec = np.array([reviewWords[word] if word in reviewWords else 0 \
                    for word in sorted_vocab])
            place_vecs.append(reviewVec)
        if len(place_vecs) == 0:
            mean_review = np.zeros(len(sorted_vocab))
        else:
            mean_review = np.mean(place_vecs, axis=0)
        vecs.append(mean_review)
    return np.array(vecs)

def getPCAReviewWordVectors(attractions, n_components=6):
    vecs = getReviewWordVectors(attractions)
    pca = PCA(n_components=n_components)
    pca.fit(vecs)
    return pca.transform(vecs)

if __name__ == "__main__":
    attractions = driver(location=LocationType.ATTRACTIONS)
    print(getPCAReviewWordVectors(attractions))
    