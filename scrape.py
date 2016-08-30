import bs4
import urllib2
import BeautifulSoup

r = urllib2.urlopen('http://secure.parking.ucf.edu/GarageCount/').read()
bs = BeautifulSoup.BeautifulSoup(r)

garages = bs.findAll(lambda tag: tag.name=='tr' and tag.has_key('id') and "ctl00_MainContent_gvCounts_DXDataRow" in tag["id"])

for g in garages:
  name = g.find(lambda tag: tag.name=='td' and tag.has_key('class') and tag["class"] == 'dxgv').getText().split(' ')[1]
  try:
    available = g.find(lambda tag: tag.name=='td' and tag.has_key('id') and "_2" in tag['id']).getText().split('/')[0]
    print name + " " + available
  except AttributeError:
    print name
  
  


