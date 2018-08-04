import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join


def parseWundergroundTable(infile):
  """ Receives a filename for an html text file to be parsed with BeautifulSoup,
     If data is available, there should be three tables within the file.
    :return temperature dict: Dictionary with relevant temperature values
    """

  f = open(infile, "rb")
  city = infile.split('_')[1]
  date = infile.split('_')[2]
  soup = BeautifulSoup(f, 'lxml')
  tables = soup.select('table')
  if (len(tables) < 2):
    print("Unexpected number of tables")
  mytab = tables[1]
  mytab_rows = mytab.findAll('tr')

  # Parse the temperature data and store it in a dictionary
  mydict = {}
  mydict['City'] = city
  mydict['Date'] = date
  for row in mytab_rows:
    row_text = row.get_text()
    if 'Day Average Temp' in row_text:
      cells = row.findAll('td')
      mydict['ActualMean'] = get_cell_data(cells[0])
    elif 'High Temp' in row_text:
      cells = row.findAll('td')
      mydict['ActualMax'] = get_cell_data(cells[0])
    elif 'Low Temp' in row_text:
      cells = row.findAll('td')
      mydict['ActualMin'] = get_cell_data(cells[0])

  return mydict

def get_cell_data(cell):
    """ Receives a cell containing temperature data to be parsed out,
    formatted, and returned.
    :param cell: A cell from the table containing temperature data
    :return temperature: String with the formatted temperature value
    """
    temperature = cell.get_text().strip()
    temperature = temperature.replace('\xa0', '')
    temperature = temperature.replace('\n', ' ')
    temperature = temperature.replace('°', '')
    return temperature 


mypath = "C:/Users/jordanna/Documents/WorldCupData/data/wundergroundFiles"
weatherfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(weatherfiles)
allTemps = []
for datafile in weatherfiles:
  fullpath = join('data', 'wundergroundFiles', datafile)
  tempDict = parseWundergroundTable(fullpath)
  allTemps.append(tempDict)
  print(tempDict)
allTemps = pd.DataFrame(allTemps)
allTemps.to_csv('WorldCupCityTemps.csv')