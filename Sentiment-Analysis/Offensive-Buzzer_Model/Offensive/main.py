import tweepy as tw
from tweepy import OAuthHandler
import os
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from google.cloud import storage
from os import getenv
import json

# authorization tokens
consumer_key = getenv("consumer_key")
consumer_secret = getenv("consumer_secret")
access_token = getenv("access_token")
access_secret = getenv("access_secret")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## Global model variable
model = None

# Download model file from cloud storage bucket
def download_pkl_model_file():
    # Model Bucket details
    BUCKET_NAME     = "ml-model-capstone"
    PROJECT_ID      = "capstone-ruang-opini"
    GCS_PKL_FILE    = "tokenizer_sentiment.pickle"
    GCS_MODEL_FILE  = "model_sentiment.h5"  

    # Initialise a client
    client   = storage.Client(PROJECT_ID)
    
    # Create a bucket object for our bucket
    bucket   = client.get_bucket(BUCKET_NAME)
    
    # Create a blob object from the filepath
    pkl     = bucket.blob(GCS_PKL_FILE)
    mdl   = bucket.blob(GCS_MODEL_FILE)

    folder = '/tmp/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Download the file to a destination
    pkl.download_to_filename(folder + "tokenizer_sentiment.pickle")
    mdl.download_to_filename(folder + "model_sentiment.h5")

# Main entry point for the cloud function
def offensive_sentiment(request):
    try: 
        # Use the global model variable 
        global model

        if not model:
            download_pkl_model_file()
            policy_tokenizer = pickle.load(open("/tmp/policy_tokenizer.pickle", 'rb'))
            policy_model = load_model("/tmp/policy_model.h5")
            sentiment_tokenizer = pickle.load(open("/tmp/tokenizer_sentiment.pickle", 'rb'))
            sentiment_model = load_model("/tmp/model_sentiment.h5")
        
        def Encoding_Policy(text):
            sequence = policy_tokenizer.texts_to_sequences([text])
            paded = pad_sequences(sequence, padding = 'pre', truncating='post', maxlen=125)
            return paded
        
        def Encoding_Sentiment(text):
            sequence = sentiment_tokenizer.texts_to_sequences([text])
            paded = pad_sequences(sequence, padding = 'pre', truncating='post', maxlen=125)
            return paded

        def TextProcessing_Policy(text, model):
            sequence = Encoding_Policy(text)
            result = model.predict(sequence)
            return result[0][0] * 100
        
        def TextProcessing_Sentiment(text, model):
            sequence = Encoding_Sentiment(text)
            result = model.predict(sequence)
            return result[0][0] * 100

        INDONESIA_WOE_ID = 23424846
        indonesia_trends = api.trends_place(INDONESIA_WOE_ID)
        
        tanggapan_list = {}
        tanggapan_list["tanggapan"] = []
        tanggapanDict = {}
        tanggapanDict["positif"] = []
        tanggapanDict["negatif"] = []
        for trends in indonesia_trends[0]['trends']:
            if TextProcessing_Policy(str(trends["name"]), policy_model) > 50:
                search = [str(trends["name"])]
                tweets = tw.Cursor(api.search, q=search, lang="in").items(5)
                for tweet in tweets:
                    if (not tweet.retweeted) and ('RT @' not in tweet.text):
                        if TextProcessing_Sentiment(str(tweet.text), sentiment_model) > 50:
                            tanggapanDict["positif"].append(tweet.text)
                        else:
                            tanggapanDict["negatif"].append(tweet.text)
        return len(tanggapanDict["positif"].append(tweet.text))/(tanggapanDict["positif"].append(tweet.text) + tanggapanDict["negatif"].append(tweet.text))
    except Exception as e:
        return e

