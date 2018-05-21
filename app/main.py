#!/bin/python
from flask import Flask, request
import xmlrpclib, json, ConfigParser
app = Flask(__name__)

# Get the config
config = ConfigParser.ConfigParser()
config.read("./config")

# Get everything from the config
db = config.get('odoo', 'db')
username = config.get('odoo', 'username')
password = config.get('odoo', 'password')
url = config.get('odoo', 'url')
debug = config.get('app', 'debug')
host = config.get('app', 'host')
port = config.get('app', 'port')

# Set the endpoint for common (publicly available) api calls
common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())
# Set the endpoint for object calls
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
# Get a user ID to make authenticated calls
uid = common.authenticate(db, username, password, {})

def getNumber(number):
# Searches for the phone number (exact match), returns the id of the match
    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['phone', '=', number]]])
# Gets all the information from the IDs
    record = models.execute_kw(db, uid, password,
        'res.partner', 'read', [ids])
    return json.dumps(record, ensure_ascii=True)

# /v1/ added for legacy support, url should be formatted like this /v1/contactsearch/?<phone number>
@app.route('/v1/contactsearch/', methods=["GET"])
def contactSearch():
    return getNumber(request.query_string)

if __name__ == '__main__':
   app.run(debug=debug, host=host, port=port)

