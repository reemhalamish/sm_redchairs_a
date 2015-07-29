#!/usr/bin/python3

"""my variation og Google Drive Quickstart in Python.

This script gets a credentials code in the browser

Re'em
"""

import pprint
from oauth2client.file import Storage
import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client

# OAuth 2.0 scope that will be authorized.
# Check https://developers.google.com/drive/scopes for all available scopes.
OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'

# Location of the client secrets.
CLIENT_SECRETS = 'client_secrets.json'

# Path to the file to upload.
FILENAME = 'blank.jpg'

# Metadata about the file.
MIMETYPE = 'image/jpg'
TITLE = 'BlAnK'
DESCRIPTION = 'the blank picture'

# Perform OAuth2.0 authorization flow.
flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an authorized Drive API client.
http = httplib2.Http()
credentials.authorize(http)
drive_service = apiclient.discovery.build('drive', 'v2', http=http)


# save the credentials
storage = Storage('extra_files/credentials_file')
storage.put(credentials)
