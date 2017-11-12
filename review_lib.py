import nltk
import json
from itinerary_main import *

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
                        if (pos != 'NNP' or tup[1] != 'NNPS'):
                            word.lower()

                        if (essence.get(word) == None):
                            essence[word] = 1
                        else:
                            essence[word] += 1

                reviews_info.append((location_id, helpful_votes, rating, essence))
        useful_info.append(reviews_info)
    return useful_info

def getReviewWordVecs(attractions):
    reviewInfo = extractReviewInfo(attractions)
    vocabulary = set()
    for place in reviewInfo:
        for _, _, _, reviewWords in place:
            vocabulary |= set(reviewWords.keys())
    print(vocabulary)

if __name__ == "__main__":
    attractions = driver(location=LocationType.ATTRACTIONS)
    getReviewWordVecs(attractions)
    #print(json.dumps(not_rest, indent=4, sort_keys=True))
    #pca_vecs = getPCACategoryVectors(not_rest)
    #print(pca_vecs)
    