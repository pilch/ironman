from bs4 import BeautifulSoup
import pandas as pd
import urllib
from time import sleep

baseurl = 'http://www.ironman.com/triathlon/events/americas/ironman/lake-placid/results.aspx?%s'

def readPage(baseurl,athleteurl):
    url = baseurl % athleteurl
    f = urllib.urlopen(url).read()
    soup = BeautifulSoup(f,'lxml')
    return soup

def getGeneralInfo(soup):
    t = soup.find('table',id='general-info').findAll('td')
    t.pop(0)
    data = [x.text.encode('utf-8') for x in t if x.strong is None]
    alltd = [x.text for x in soup.findAll('td')]
    for i in range(0,len(alltd)):
        if alltd[i] == 'T1: Swim-to-bike' or alltd[i] == 'T2: Bike-to-run':
            data.append(alltd[i+1].encode('utf-8'))
    headers = [x.text.encode('utf-8') for x in t if x.strong is not None]
    headers.append('T1')
    headers.append('T2')
    df = pd.DataFrame([data],columns=headers)
    return df

def getAll(baseurl,output):
    soup1 = readPage(baseurl,output[:1]['URL'].to_string(index=False).encode('utf-8'))
    df = getGeneralInfo(soup1)
    for i in range(1,len(output)):
        print i
        thisurl = output['URL'].iloc[i]
        thissoup = readPage(baseurl,thisurl)
        thisdf = getGeneralInfo(thissoup)
        df = df.append(thisdf)
        print('Completed page ' + str(i))
        sleep(1)
    return df

def go():
    output = pd.read_csv('lakeplacid2017results2.csv')
    athletes = getAll(baseurl,output)
    athletes.to_csv('lakeplacid2017detailedresults.csv',index=False)

athletes = pd.read_csv('lakeplacid2017detailedresults.csv')
output = pd.read_csv('lakeplacid2017results2.csv')
athletes['URL'] = output['URL']
M = pd.concat([output,athletes],axis=1)
M.to_csv('masteroutput.csv',index=False)

def convert(col):
    L = col.str.split(':')
    back = []
    for each in L:
        try:
            t = int(each[0])*60 + int(each[1]) + float(each[2])/60
        except:
            t = 0
        back.append(t)
    return back


def convertToMinutes(M):
    M['SwimNum'] = convert(M['Swim'])
    M['RunNum'] = convert(M['Run'])
    M['BikeNum'] = convert(M['Bike'])
    M['T1Num'] = convert(M['T1'])
    M['T2Num'] = convert(M['T2'])

convertToMinutes(M)
M.to_csv('masteroutput.csv',index=False)