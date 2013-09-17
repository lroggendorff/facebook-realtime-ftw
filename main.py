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
        mode = request.args.get("hub.mode", "")
        challenge = request.args.get("hub.challenge", "")
        verify_token = request.args.get("hub.verify_token", "")

        # TODO
        # Verify verify_token

        if mode == "subscribe" and verify_token:
            return challenge, 200

    if request.method == "POST":
        db = settings.CLOUDANT_DATABASE if settings.CLOUDANT_DATABASE else "raw_facebook_events"
        try:
            cloudant.post(db, dict(data=request.json, platform="facebook"))
        except:
            sentry.captureMessage(pprint.pformat(request.json), tags={"type": "Facebook"})

    return 'OK\n', 200
