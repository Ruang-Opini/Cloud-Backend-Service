from tweepy import OAuthHandler
import tweepy
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
api = tweepy.API(auth, auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## Global model variable
model = None

# Download model file from cloud storage bucket
def download_pkl_model_file():
    # Model Bucket details
    BUCKET_NAME     = "ml-model-capstone"
    PROJECT_ID      = "capstone-ruang-opini"
    GCS_PKL_FILE    = "tokenizerkebijakan.pickle"
    GCS_MODEL_FILE  = "model_kebijakan.h5"  

    # Initialise a client
    client   = storage.Client(PROJECT_ID)
    
    # Create a bucket object for our bucket
    bucket   = client.get_bucket(BUCKET_NAME)
    
    # Create a blob object from the filepath
    pkl   = bucket.blob(GCS_PKL_FILE)
    mdl   = bucket.blob(GCS_MODEL_FILE)

    folder = '/tmp/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Download the file to a destination
    pkl.download_to_filename(folder + "policy_tokenizer.pickle")
    mdl.download_to_filename(folder + "policy_model.h5")

# Main entry point for the cloud function
def policy_sentiment(request):
    try:
        # Use the global model variable 
        global model

        if not model:
            download_pkl_model_file()
            tokenizer = pickle.load(open("/tmp/policy_tokenizer.pickle", 'rb'))
            policy_model = load_model("/tmp/policy_model.h5")
        
        def Encoding(text):
            sequence = tokenizer.texts_to_sequences([text])
            paded = pad_sequences(sequence, padding = 'pre', truncating='post', maxlen=125)
            return paded

        def TextProcessing(text, model):
            sequence = Encoding(text)
            result = model.predict(sequence)
            return result[0][0] * 100

        INDONESIA_WOE_ID = 23424846
        indonesia_trends = api.trends_place(INDONESIA_WOE_ID)
        trending_list = {}
        trending_list["trending"] = []
        for trends in indonesia_trends[0]['trends']:
            if TextProcessing(str(trends["name"]), policy_model) > 50:
                trending_list["trending"].append(trends["name"])
        return json.loads(json.dumps(trending_list))

    except Exception as e:
        return e