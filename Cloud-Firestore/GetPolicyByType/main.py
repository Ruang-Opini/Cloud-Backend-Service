import requests
import json
from bs4 import BeautifulSoup

def getPolicyByType(request):
    try:
        if request.args and 'url' in request.args:
          BASE_URL = 'https://peraturan.go.id'
          URL = request.args.get('url')
          page = requests.get(str(BASE_URL+"/"+URL))

          soup = BeautifulSoup(page.content, 'html.parser')

          results = soup.find_all('tbody')
            
          resultData = { }
          resultData['policy'] = []

          jsonData = { }

          for data in results:
            nama = data.find_all('td')
            i = 0
            for m in nama:
              if i == 0: 
                jsonData = { }
                jsonData["no"] = m.text.strip()
              elif i == 1 : jsonData["uu"] = m.text.strip()
              elif i == 2 : jsonData["name"] = m.text.strip()
              else: 
                links = m.find_all('a')
                jsonData["link"] = []
                for read in links: 
                  link = read['href']
                  jsonData["link"].append(link)
                resultData['policy'].append(jsonData)
                i = -1
              i+=1
          return json.loads(json.dumps(resultData))
        else:
          return 'Precondition Failed', 412
    except Exception as e:
        return e