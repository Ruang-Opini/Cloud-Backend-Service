from flask import jsonify
from google.cloud import firestore

def getUser(request):
    try:
        if request.args and 'userId' in request.args:
            userId = request.args.get('userId')
        else:
            return 'Precondition Failed', 412
        
        client = firestore.Client()
        doc_ref = client.collection(u'user').document(u'{}'.format(userId))
        doc = doc_ref.get()
        if doc.to_dict():
            response = jsonify(doc.to_dict())
            response.status_code = 200
        else:
            response = jsonify({
                'httpResponseCode': '404',
                'errorMessage': 'User does not exist'
            })
            response.status_code = 404
        return response
    except Exception as e:
        return e