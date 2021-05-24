import requests
import json
from bs4 import BeautifulSoup

def getAllPolicyCategory(request):
    try:
        BASE_URL = 'https://peraturan.go.id'
        homePage = requests.get(BASE_URL)
        homeSoup = BeautifulSoup(homePage.content, 'html.parser')
  
        resultCategory = {}
        resultCategory["category"] = { }
  
        tabJenis = homeSoup.find(id='jenis')
        resultCategory["category"]["jenis"] = []
        jenisCategory = tabJenis.find_all('a')

        for category in jenisCategory:
          jsonJenis = {}
          jsonJenis["name"] = category.text.strip()
          jsonJenis["url"] = BASE_URL+category['href']
          resultCategory["category"]["jenis"].append(jsonJenis)
    
        tabCategory = homeSoup.find(id='kategori')
        resultCategory["category"]["kategori"] = []

        kategoryCategory = tabCategory.find_all('a')
        for kategori in kategoryCategory:
          jsonCategory = {}
          jsonCategory["name"] = kategori.text.strip()
          jsonCategory["url"] = BASE_URL+kategori['href']
          resultCategory["category"]["kategori"].append(jsonCategory)
        return json.loads(json.dumps(resultCategory))
    except Exception as e:
        return e
