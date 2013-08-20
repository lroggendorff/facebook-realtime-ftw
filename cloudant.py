#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple Cloudant client, which is basically just a thin wrapper around the
requests.Session class.

Usage:

    import cloudant

    db = "messages"
    message = dict(_id="OHAI", text="OHAI!")

    # Create a message
    cloudant.post(db, message)

    # Get a message
    message = cloudant.get(db, "OHAI")
"""

import json

import requests

import settings


class Cloudant(requests.Session):
    """
    Simple Cloudant client, which is basically just a thin wrapper around the
    requests.Session class.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Cloudant session.
        """
        self.username = kwargs.pop("username")
        self.password = kwargs.pop("password")
        self.account = kwargs.pop("account", self.username)

        super(Cloudant, self).__init__(*args, **kwargs)

        self.auth = (self.username, self.password)

    def request(self, method, url, *args, **kwargs):
        url = "https://{username}.cloudant.com{path}".format(username=self.account, path=url)

        return super(Cloudant, self).request(method, url, *args, **kwargs)

    def get(self, db, doc, *args, **kwargs):
        """
        Gets (reads) a document from a cloudant db
        """
        url = "/".join(("", db, doc))

        return super(Cloudant, self).get(url, *args, **kwargs)

    def post(self, db, doc, *args, **kwargs):
        """
        Posts (writes) a document to a cloudant db
        """
        url = "/".join(("", db))
        payload = json.dumps(doc)
        headers = kwargs.pop("headers", {'content-type': 'application/json'})

        return super(Cloudant, self).post(url, *args, data=payload, headers=headers, **kwargs)


cloudant = Cloudant(username=settings.CLOUDANT_USERNAME,
                    password=settings.CLOUDANT_PASSWORD,
                    account=settings.CLOUDANT_ACCOUNT)
get = cloudant.get
post = cloudant.post
