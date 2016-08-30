import bs4
import urllib2
import json
import BeautifulSoup

def lambda_handler():
  r = urllib2.urlopen('http://secure.parking.ucf.edu/GarageCount/').read()
  bs = BeautifulSoup.BeautifulSoup(r)
  
  garages = bs.findAll(lambda tag: tag.name=='tr' and tag.has_key('id') and "ctl00_MainContent_gvCounts_DXDataRow" in tag["id"])
  
  data = {}
  
  for g in garages:
    name = g.find(lambda tag: tag.name=='td' and tag.has_key('class') and tag["class"] == 'dxgv').getText().split(' ')[1]
    try:
      available = g.find(lambda tag: tag.name=='td' and tag.has_key('id') and "_2" in tag['id']).getText().split('/')[0]
      data[name] = available
    except AttributeError as e:
      print e
      
  print json.dumps(data)


lambda_handler()