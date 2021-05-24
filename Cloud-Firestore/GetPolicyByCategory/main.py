import requests
import json
from bs4 import BeautifulSoup

def getPolicyByCategory(request):
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
          td = results[0].find_all('td')
          i = 0

          for content in td:
            res = content.text.strip()
            if i == 0 : 
              jsonData = { }
              jsonData['no'] = res
            elif i == 1: jsonData['name'] = res
            elif i == 2: jsonData['policyNum'] = res
            elif i == 3: jsonData['year'] = res
            elif i == 4: 
              links = content.find_all('a')
          
              jsonData['link'] = BASE_URL+links[0]['href'] 
              jsonData['about'] = res
            elif i == 6: 
              i= -1
              resultData['policy'].append(jsonData)
            i+=1
          return json.loads(json.dumps(resultData))
        else:
          return 'Precondition Failed', 412
    except Exception as e:
        return e