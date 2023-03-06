import time
import requests
from bs4 import BeautifulSoup
import random
import pprint


def neetConnect(url):
  '''
  return Response Object
  '''

  for i in range(3):
    try:
      random_sleep_link = random.uniform(5, 10) 
      print("Sleep for " + str(random_sleep_link) + " Seconds...")
      time.sleep(random_sleep_link)
      print("Now Requesting to  [" + url + " ] ...")
      page = requests.get(url)
      print("Success! Returning...")
      return page

    except requests.exceptions.RequestException as e: 
      random_sleep_except = random.uniform(240,360)
      print("I've encountered an error! I'll pause for"+str(random_sleep_except/60) + " minutes and try again \n")
      time.sleep(random_sleep_except) 
      continue 

    else:
      break 

  else: #if x amount of retries on the try-part don't work...#
    raise Exception("Something really went wrong here... I'm sorry.") #...raise an exception and stop the script#

def getIssueObj(soup):
  print("Parsing HTML...")
  card_box = soup.find('div', {'id': 'cardBox'})
  author = card_box.find('td', {'class': 'name'}).text
  textColumn = card_box.find('div', {'class': 'textColumn'})
  ddAll = textColumn.find_all('dd')

  info = {   
    "classify": ddAll[0].text.rstrip(),
    "anthology": ddAll[1].text.rstrip(),
    "theme": ddAll[2].text.rstrip(),
    "meaning": ddAll[3].select_one('p:nth-child(1)').text.rstrip(),
    "interpretation": ddAll[3].select_one('p:nth-child(2)').text.rstrip()
  }

  tableAll = textColumn.find_all('table')

  script = []
  for i, table in enumerate(tableAll):
    trAll = table.find_all('tr')
    yomi = trAll[0].find('th').string
    text = trAll[1].find('td').string
    script.append({"text": text, "yomi": yomi})

  issue = {"author": author,"script": script,"info": info}
  print("Parsing is Done!")
  return issue


url = 'https://www.samac.jp/search/poems_detail.php?id='

data = []

for i in range(1, 3):
    r = neetConnect(url + str(i))
    if not r:
       continue
    content_type_encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
    soup = BeautifulSoup(r.content,"lxml",from_encoding=content_type_encoding) 
    issue = getIssueObj(soup)
    data.append(issue)
    print(str(i) + "-issue is appended.")


pprint.pprint(data)

