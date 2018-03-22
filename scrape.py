from bs4 import BeautifulSoup
import pandas as pd
import urllib
from time import sleep

baseurl = "http://www.ironman.com/triathlon/events/americas/ironman/lake-placid/results.aspx?p=%s&ps=20#axzz5AFmpHIgY"

def readFile(baseurl,p):
    url = baseurl % p
    f = urllib.urlopen(url).read()
    soup = BeautifulSoup(f,'lxml')
    if soup.find('table',id='eventResults') is not None:
        return soup.find('table',id='eventResults')
    else:
        print('No such table found')
        return 'NA'

def grabTable(soup):
    headers = [str(x.text) for x in soup.findAll('th')]
    headers.append('URL')
    L = []
    M = soup.findAll('tr')
    M.pop(0)
    for row in M:
        a = [str(x.text.encode('utf-8')) for x in row.findAll('td')]
        a.append(row.a['href'])
        L.append(a)
    df = pd.DataFrame(L,columns = headers)
    return df

def iterate(n):
    soup = readFile(baseurl,1)
    df = grabTable(soup)
    for i in range(2,n+1):
        soup = readFile(baseurl,i)
        newdf = grabTable(soup)
        df = df.append(newdf)
        print("Completed page " + str(i))
        sleep(1)
    return df

# output = iterate(138)
# output.to_csv('lakeplacid2017results2.csv',index=False)