import pprint

from flask import Flask, request

from raven.contrib.flask import Sentry

from cloudant import cloudant

import settings

app = Flask(__name__)

sentry = Sentry(app)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/facebook', methods=['POST', 'GET'])
def facebook():
    if request.method == "GET":
        print "Handling GET in /facebook"
        mode = request.args.get("hub.mode", "")
        challenge = request.args.get("hub.challenge", "")
        verify_token = request.args.get("hub.verify_token", "")

        if mode == "subscribe" and verify_token == "v3riFY":
            return challenge, 200

    if request.method == "POST":
        print "Handling POST in /facebook"
        db = settings.CLOUDANT_DATABASE if settings.CLOUDANT_DATABASE else "raw_facebook_events"
        try:
            print "Posting to Cloudant..."
            print db
            response = cloudant.post(db, dict(data=request.json, platform="facebook"))
            pprint.pprint(response)
        except:
            print "FAIL."
            pprint.pprint(request.json)
            sentry.captureMessage(pprint.pformat(request.json), tags={"type": "Facebook"})

    return 'OK\n', 200
