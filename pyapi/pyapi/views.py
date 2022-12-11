from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests

def getDetails(request, country):
    details = {}

    page = requests.get("https://en.wikipedia.org/wiki/"+country)
    soup = BeautifulSoup(page.content, 'html.parser')

    flag = soup.find(class_="infobox-image")

    details['flag_link'] = "https:"+flag.find('img')['src']

    captial = soup.find(class_='mergedbottomrow').find_previous('tr')

    if(captial.find_all('li')!=None):
        details['captial'] = []
        for i in captial.find_all('li'):
            details['captial'].append(i.find('a')['title'])
    if(captial.find('li')==None):
        details['captial'] = captial.find('a')['title']

    largest = soup.find(class_='mergedbottomrow')

    if(largest.find_all('li')!=None):
        details['largest_city'] = []
        for i in largest.find_all('li'):
            details['largest_city'].append(i.find('a')['title'])
    if(largest.find('li')==None):
        details['largest_city'] = largest.find('a')['title']

    languages = soup.find(class_='mergedtoprow')

    if(languages.find_all('li')!=None):
        details['offical_lanuages'] = []
        for i in languages.find_all('li'):
            details['offical_lanuages'].append(i.find('a')['title'])
    if(languages.find('li')==None):
        details['offical_lanuages'] = languages.find('a')['title']
    area = soup.find_all(class_="mergedtoprow")[2].find_next(class_="mergedrow").find('td').getText()
    details["area_total"] = area.split(" ")[0]

    population = soup.find_all(class_="mergedtoprow")[3].find_next(class_="mergedrow").find('td').getText()
    if('[' in population):
        details["Population"] = population[:population.index('[')]
    if('[' not in population):
        details["Population"] = population

    gdp = soup.find_all(class_="mergedtoprow")[5].find_next(class_="mergedrow").find('td').getText()

    details["GDP_nominal"] = gdp
    
    return JsonResponse(details,safe=False)