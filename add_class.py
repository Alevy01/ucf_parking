import psycopg2


def lambda_handler(event, context):
  phone_number = event['phone_number']
  conn = psycopg2.connect(dbname="parking_test_db", user="alevy", password="parkingdb", host="parking-test-db.cwhygsajux1b.us-east-1.rds.amazonaws.com", port=5432)
  cur = conn.cursor()
  for course in event['classes']:
    q = 'INSERT into "user_texts" ("phone_number", "day", "time", "building") values (\''+phone_number+'\', \''+str(course['day'])+'\', \''+str(course['time'])+'\', \''+course['building']+'\');'
    cur.execute(q)
  conn.commit()   