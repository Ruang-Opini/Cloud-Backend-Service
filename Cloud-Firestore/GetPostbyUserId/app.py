from flask import jsonify
#import json
from google.cloud import firestore

def getPostbyUserId(request):
    try:
        if request.args and 'userId' in request.args:
            userId = request.args.get('userId')
        else:
            return 'Precondition Failed', 412    

        db = firestore.Client()
        doc_ref = db.collection(u'post').where('userId', '==', userId)
        #posts = []
        doc = doc_ref.get()
        if doc.to_dict():   
            result = jsonify(doc.to_dict())
            result.status_code = 200
            #x = print(result)
            #posts.append(doc.reference)
            #return json.dumps(posts)
        else:
            result.status_code = 404
        return result
    except Exception as e:
        return e