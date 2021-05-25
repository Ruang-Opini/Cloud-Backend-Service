from google.cloud import firestore
import json
import datetime

def getAllUsers(request):
    def myconverter(o):
      if isinstance(o, datetime.datetime):
        return o.__str__()
    try:
        db = firestore.Client()
        doc_ref = db.collection(u'user').get()
        my_dict = {}
        my_dict["user"] = []
        for doc in doc_ref:
            my_dict["user"].append({doc.id: doc.to_dict()})
        return json.loads(json.dumps(my_dict, default=myconverter))
    
    except Exception as e:
        return e