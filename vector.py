from get_reviews import reviews
import nltk

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
            for tup in tokenized:
                word, pos = tup
                if (pos in ('NNP', 'NN', 'NNPS', 'NNS', 'JJ', 'JJR', 'JJS')):
                    if (pos != 'NNP' or tup[1] != 'NNPS'):
                        word.lower()

                    if (essence.get(word) == None):
                        essence[word] = 1
                    else:
                        essence[word] += 1

            reviews_info.append((location_id, helpful_votes, rating, essence))

    useful_info.append(reviews_info)

for thing in useful_info:
    print(*thing)