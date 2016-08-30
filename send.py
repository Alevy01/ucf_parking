from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import config

account = config.twilio_config['account']
token = config.twilio_config['token']
client = TwilioRestClient(account, token)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
  """Respond to incoming text with a simple text message."""
  body = request.form.getlist('Body')
  resp = twilio.twiml.Response()
  resp.message("This is your body. " + str(body[0]))
  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)