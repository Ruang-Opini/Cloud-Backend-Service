from os import getenv
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from google.cloud import storage
from tweepy import OAuthHandler
import tweepy
import json

# authorization tokens
consumer_key = getenv("consumer_key")
consumer_secret = getenv("consumer_secret")
access_token = getenv("access_token")
access_secret = getenv("access_secret")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## Global model variable
model = None

# Download model file from cloud storage bucket
def download_pkl_model_file():
  # Model Bucket details
  BUCKET_NAME     = "ml-model-capstone"
  PROJECT_ID      = "capstone-ruang-opini"
  GCS_MODEL_FILE  = "model_buzzer.h5"  

  # Initialise a client
  client   = storage.Client(PROJECT_ID)
    
  # Create a bucket object for our bucket
  bucket   = client.get_bucket(BUCKET_NAME)
    
  # Create a blob object from the filepath
  mdl   = bucket.blob(GCS_MODEL_FILE)

  folder = '/tmp/'
  if not os.path.exists(folder):
    os.makedirs(folder)
  # Download the file to a destination
  mdl.download_to_filename(folder + "buzzer_model.h5")

# Main entry point for the cloud function
def buzzer_sentiment(request):
  try:
    if request.args and 'trending' in request.args:
      trending = request.args.get('trending')
    else:
      return 'Precondition Failed', 412

    # Use the global model variable 
    global model

    if not model:
      download_pkl_model_file()
      buzzer_model = load_model("/tmp/buzzer_model.h5")
        
    fullnamewords_maxmin = [12, 5]
    fullnamelen_maxmin = [50,0]
    desclen_maxmin = [150, 0]
    posts_maxmin = [299 * 3, 0]
    followers_maxmin = [110*3, 0]
    following_maxmin = [302*3, 0]

    def rescale_uname(value):
      max = 15
      min = 4
      if value > max:
        value = 1.0
      elif value < min:
        value = 0.0
      else:
        value = (value-min)/(max-min)
      return value

    def rescale(value, maxmin):
      maxval = maxmin[0]
      minval = maxmin[1]
      if value > maxval:
        value = 1.0
      elif value < minval:
        value = 0.0
      else:
        value = (value-minval)/(maxval-minval)
      return value

    def processing_profil(profil_pic, username, fullname, desc, private, posts, followers, following):
      #username = username.replace('@', '')
      username = username.lower()
      #print("username = {}".format(username))
      username_len = rescale_uname(len(username))
      #print("username length = {}".format(username_len))
      fullname_words = fullname.split()
      fullname_words = len(fullname_words)
      fullname_words = rescale(fullname_words, fullnamewords_maxmin)
      #print("Fullname words = {}".format(fullname_words))
      fullname_len = rescale(len(fullname), fullnamelen_maxmin)
      #print("Fullname length = {}".format(fullname_len))
      fullname = fullname.replace(' ', '')
      fullname = fullname.lower()
            
      if fullname == username:
        same = 1
      else:
        same = 0
        
      #print("is same fullname username = {}".format(same))    
      desc_len = rescale(len(desc), desclen_maxmin)
      #print("Desc length = {}".format(desc_len))
      num_post = rescale(posts, posts_maxmin)
      #print("post = {}".format(num_post))
      followers = rescale(followers, followers_maxmin)
      #print("followers = {}".format(followers))
      following = rescale(following, following_maxmin)
      #print("following = {}".format(following))
      if profil_pic == None or profil_pic == 'null':
        profil_pic = 0
      else:
        profil_pic = 1
                    
      if private == 'true':
        private = 1
      else: 
        private = 0
            
      features = [
        profil_pic,
        username_len,
        fullname_words,
        fullname_len,
        same,
        desc_len,
        private,
        num_post,
        followers,
        following
      ]
            
      return features

    def dict_handler(dictlist, model):
      query = []
      for dict in dictlist:
        single_list = []
        profil_pic = dict['profil_pic']
        username = dict['username']
        fullname = dict['fullname']
        desc = dict['desc']
        private = dict['private']
        posts = dict['posts']
        followers = dict['followers']
        following = dict['following']
        single_list = processing_profil(profil_pic, username, fullname, desc, private, posts, followers, following)
        query.append(single_list)
      result = model.predict(query)
      return result

    usertype_list = {}
    usertype_list["type"] = {}
    BUZZER = 0
    NON = 0
    data_dict = []
    search = [trending]
    tweets = tweepy.Cursor(api.search, q=search, lang="in").items(100)
    for tweet in tweets:
      record_dict = {'profil_pic' : tweet.user.profile_image_url_https,
                      'username' : tweet.user.screen_name,
                      'fullname' : tweet.user.name,
                      'desc' : tweet.user.description,
                      'private' : tweet.user.protected,
                      'posts' : tweet.user.statuses_count,
                      'followers' : tweet.user.followers_count,
                      'following' : tweet.user.friends_count}
      data_dict.append(record_dict)

    results = dict_handler(data_dict, buzzer_model)
    for res in results:
      if res > 0.5:
        BUZZER += 1
      else:
        NON += 1

    usertype_list["type"]["buzzer"] = BUZZER
    usertype_list["type"]["non"] = NON

    return json.loads(json.dumps(usertype_list))
    
  except Exception as e:
    return e