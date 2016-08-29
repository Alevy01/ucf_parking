from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient

account = "AC8902f665df08b74da8713b438bb27631"
token = "a5ef95787f4dc83d458feb16deccd8ea"
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