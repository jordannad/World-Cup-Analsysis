import numpy as np 
import pandas as pd
from datetime import datetime, time, date
import time
from selenium import webdriver
from os import listdir
from os.path import isfile, join

def getWundergroundPages(city, countrycode, station, day, month, year):
    """
    Function to write a text file of historical weather data for a 
    Wunderground station.

    Args:
        station (string): Station code from the Wunderground website
        day (int): Day of month for which data is requested
        month (int): Month for which data is requested
        year (int): Year for which data is requested

    """
    url = ('https://www.wunderground.com/history/daily/%s/%s/%s/date/%s-%s-%s?cm_ven=localwx_history' 
           % (countryCode, city, station, year, month, day))
    browser = webdriver.Chrome('C:/Users/jordanna/Downloads/chromedriver_win32/chromedriver.exe')
    try: 
      browser.get(url)
      time.sleep(10)
    except:
      print('Problem loading page for %s on %s-%s-%s' % (city, year, month, day))

    pageOutput = browser.page_source
    outfile = ('data/wundergroundFiles/WundergroundData_%s_%s-%s-%s_WorldCup%s.txt' 
        % (city.replace('/', ''), year, month, day, year))
    f = open(outfile, "wb")
    f.write(pageOutput.encode())
    f.close()
    browser.close()


df = pd.read_csv('data/worldCupMatches.csv')
df[['date','time']] = df['Datetime'].str.split('-',expand=True)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['City'] = df['City'].str.rstrip()

stations = pd.read_csv('data/wundergroundStations.csv')
stations['City'] = stations['City'].str.rstrip()
dfPost2002 = df[df['Year'] > 2002]
cities = stations.City.unique()

for city in cities:
  print("Getting data for " + city)
  station = stations.loc[stations['City'] == city, 'Station'].item()
  wundergroundCity = stations.loc[stations['City'] == city, 'Wcityname'].item()
  countryCode = stations.loc[stations['City'] == city, 'CountryCode'].item()
  subdf = dfPost2002[dfPost2002['City'] == city]
  uniqueDates = subdf["Datetime"].map(pd.Timestamp.date).unique()
  for date in uniqueDates:
    print(date)
    getWundergroundPages(wundergroundCity, countryCode, station, date.day, date.month, date.year)
 
