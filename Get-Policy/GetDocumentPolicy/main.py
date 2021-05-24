import requests
import json
from bs4 import BeautifulSoup

BASE_URL = "https://peraturan.go.id"

def getDoc(URL):
    docPage = requests.get(str(BASE_URL + "/" + URL))
    docSoup = BeautifulSoup(docPage.content, 'html.parser')

    result = docSoup.find_all('center')
    center = result[0].find_all('a')
    jsonData = {}
    jsonData['policy'] = []
    jsonData['policy'].append(center[0]['href'])
    return json.loads(json.dumps(jsonData))

def getDocumentPolicy(request):
    try:
        if request.args and 'url' in request.args:
            URL = request.args.get('url')
            return getDoc(URL)
        else:
            return 'Precondition Failed', 412
    except Exception as e:
        return e