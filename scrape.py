import bs4
import urllib2
import json
import BeautifulSoup
import psycopg2
import datetime
import twilio.twiml
from twilio.rest import TwilioRestClient
import config


def lambda_handler(event, context):
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

  conn = psycopg2.connect(dbname=config.db_config['dbname'], user=config.db_config['user'], password=config.db_config['password'], host=config.db_config['host'], port=config.db_config['port'])
  cur = conn.cursor()
  today = datetime.datetime.today().weekday()
  time = datetime.datetime.now().time()
  hour = time.hour
  minute = time.minute

  #This will overflow past midnight but we don't care. There will be no texts to be sent at that time.
  #UI should check if time is valid class time prior to submitting.
  if minute >=53:
    hour = hour + 1
  
  minute = myround(minute)
  #Check if hour comes back at 05 or just 5. If just 5, pad 0 to front.
  now = str(hour) + str(minute)
  if len(now) != 4:
    now += '0'
  if hour < 10:
    now = '0' + now

  query = 'SELECT * from "user_texts" where "day"='+str(today)+' AND "time"='+str(now)+';'
  cur.execute(query)
  users = cur.fetchall();
  account = config.twilio_config['account']
  token = config.twilio_config['token']
  client = TwilioRestClient(account, token)
  gTable = {} 
  for user in users:
    num = user[0]
    building = user[3]
    resultGarage = ''
    if building in gTable: 
      resultGarage = gTable[building] 
    else:
      resultGarage = garage_logic(building,data)
      gTable[building] = resultGarage
    # print the message
    msg = 'You should park in Garage ' +resultGarage+ '. It has the most open spots in relation to ' + building  +'.'
    message = client.messages.create(to=num, from_=config.twilio_config['number'], body=msg)
  
def myround(x, base=15):
  return int(base * round(float(x)/base)) % 60

def garage_logic(building,data):
  dict = {
    'HEC': ['C','D'],
    'ENG1': ['B','C'],
    'ENG2': ['C','D'],
    'BA1': ['B','C'],
    'BA2': ['B','C'],
    'HPA': ['D','H'],
    'HPA2': ['D','C'],
    'CB1': ['H','D'],
    'CB2': ['H','D'],
    'CSB': ['B','I'],
    'PSY': ['H','D'],
    'NSC': ['H','D'],
    'CAH': ['H','D'],
    'VAB': ['H','I'],
    'PAC': ['H','I'],
    'ED': ['A','I'],
    'TA': ['A','I'],
    'MSB': ['A','B'],
    'CHEM': ['B','Libra'],
    'RWC': ['B','Libra'],
    'BIO': ['B','Libra'],
    'PSB': ['B','Libra']
    }
  return dict[building][0] if data[dict[building][0]] > data[dict[building][1]] else dict[building][1]
