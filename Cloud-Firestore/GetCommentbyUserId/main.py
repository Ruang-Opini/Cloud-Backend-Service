from google.cloud import firestore
import json
import datetime
import pytz

def getCommentbyUserId(request):
    try:
        if request.args and 'userId' in request.args:
            userId = request.args.get('userId')
        else:
            return 'Precondition Failed', 412

        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        db = firestore.Client()
        doc_ref = db.collection(u'comment')
        query = doc_ref.where(u'userId', u'==', userId).order_by(
            u'createdAt', direction=firestore.Query.DESCENDING)
        results = query.get()
        my_dict = {}
        my_dict["comment"] = []
        for doc in results:
            my_dict["comment"].append({doc.id: doc.to_dict()})
        return json.loads(json.dumps(my_dict, default=myconverter))
    except Exception as e:
        return e