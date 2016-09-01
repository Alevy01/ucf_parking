import psycopg2
import config

def lambda_handler(event, context):
  phone_number = event['phone_number']
  conn = psycopg2.connect(dbname=config.db_config['dbname'], user=config.db_config['user'], password=config.db_config['password'], host=config.db_config['host'], port=config.db_config['port'])
  cur = conn.cursor()
  for course in event['classes']:
    q = 'INSERT into "user_texts" ("phone_number", "day", "time", "building") values (\''+phone_number+'\', \''+str(course['day'])+'\', \''+str(course['time'])+'\', \''+course['building']+'\');'
    cur.execute(q)
  conn.commit()   
