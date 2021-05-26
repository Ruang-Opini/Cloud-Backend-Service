from google.cloud import firestore
import json 
import datetime

def getLatestDiscussions(request):
    def myconverter(o):
      if isinstance(o, datetime.datetime):
        return o.__str__()
    try:
        db = firestore.Client()
        doc_ref = db.collection(u'discussion')
        latest = datetime.datetime.now() - datetime.timedelta(days=7)
        query = doc_ref.where(u'createdAt', u'>', latest).order_by(
            u'createdAt', direction=firestore.Query.DESCENDING)
        results = query.get()
        my_dict = {}
        my_dict["discussion"] = []
        for doc in results:
            my_dict["discussion"].append({doc.id: doc.to_dict()})
        return json.loads(json.dumps(my_dict, default=myconverter))
    except Exception as e:
        return e