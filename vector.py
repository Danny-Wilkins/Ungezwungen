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

        print(text)

        if (lang == 'en'):
            reviews_info.append((location_id, helpful_votes, rating, text))

    useful_info.append(reviews_info)