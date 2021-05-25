import os
from google.cloud import firestore
from flask import Flask
import json
#import datetime

app = Flask(__name__)

@app.route('/AllUsers', methods=['GET'])
def getAllUsers():
    def myconverter(o):
      if isinstance(o, datetime.datetime):
        return o.__str__()
    try:
        db = firestore.Client()
        doc_ref = db.collection(u'user').get()
        my_dict = []
        #my_dict = { x.id: x.to_dict() }
        for doc in doc_ref:
            my_dict.append({doc.id: doc.to_dict()})
        return json.loads(json.dumps(my_dict, default=myconverter))
    
    except Exception as e:
        return e

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)