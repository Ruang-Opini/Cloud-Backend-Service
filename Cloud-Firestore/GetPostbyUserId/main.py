from flask import jsonify
from google.cloud import firestore
#import json
import datetime
import pytz

def getPostbyUserId(request):
    try:
        if request.args and 'userId' in request.args:
            userId = request.args.get('userId')
        else:
            return 'Precondition Failed', 412    
    
        def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
        
        db = firestore.Client()
        collection = db.collection("post").where("userId", "==", userId)
        posts = []
        for doc in collection.stream():   
            result = doc.to_dict()
            print(json.loads(json.dumps(result, default=myconverter)))
            posts.append(doc.reference)
        return posts

    except Exception as e:
        return e