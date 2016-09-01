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
      

  g_data = json.dumps(data)
  conn = psycopg2.connect(dbname="parking_test_db", user="alevy", password="parkingdb", host="parking-test-db.cwhygsajux1b.us-east-1.rds.amazonaws.com", port=5432)
  cur = conn.cursor()
  today = datetime.datetime.today().weekday()
  time = datetime.datetime.now().time()
  hour = time.hour
  minute = time.minute
  if minute >=53:
    hour = hour + 1
  
  minute = myround(minute)
  now = str(hour) + str(minute)
  if len(now) != 4:
    now += '0'

  query = 'SELECT * from "user_texts" where "day"='+str(today)+' AND "time"='+str(now)+';'
  cur.execute(query)
  users = cur.fetchall();

  account = config.twilio_config['account']
  token = config.twilio_config['token']
  client = TwilioRestClient(account, token)

  for user in users:
    num = user[0]
    message = client.messages.create(to=num, from_=config.twilio_config['number'], body="")
  
def myround(x, base=15):
  return int(base * round(float(x)/base)) % 60

event = {'building' : 'A'}
lambda_handler(event, '')

