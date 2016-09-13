from random import randint
import twilio.twiml
from twilio.rest import TwilioRestClient
import config



def lambda_handler(event,context):
  verification_code = randint(10000,99999)
  phone_number = event['phone_number']
  account = config.twilio_config['account']
  token = config.twilio_config['token']
  client = TwilioRestClient(account,token)
  client.messages.create(to=phone_number,from_=config.twilio_config["number"],body='Your verification code is '+ str(verification_code))
  return verification_code


