#!/usr/bin/python3

import sys
import pprint
import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client
from oauth2client.file import Storage
import threading

# input - Path to the file to upload.
def uploadToGoogleDriveServer(filepath):

    FILENAME = filepath.split('/')[-1]

    # Metadata about the file.
    MIMETYPE = 'image/jpg'
    TITLE = FILENAME
    DESCRIPTION = FILENAME + " captured in the science museum at jerusalem"

    # ID of the "red chairs folder" in google drive
    PICTURES_FOLDER_ID = '0B8_BMiVz-9QqfnRPek9OTE9vMjlvODZlZzBfOHlQb3BZUGZ2bnU3OXREYl9oOVFINGx0U0E'

    # get the creds out of the file
    storage = Storage('extra_files/credentials_file')
    credentials = storage.get()

    # Create an authorized Drive API client.
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = apiclient.discovery.build('drive', 'v2', http=http)


    # Insert a file. Files are comprised of contents and metadata.
    # MediaFileUpload abstracts uploading file contents from a file on disk.
    media_body = apiclient.http.MediaFileUpload(
        filepath,
        mimetype=MIMETYPE,
        resumable=True
    )
    # The body contains the metadata for the file.
    body = {
      'title': TITLE,
      'description': DESCRIPTION,
      'parents' : [ { "id" : PICTURES_FOLDER_ID } ]
    }

    # Perform the request and print the result.
    new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
    with open("log.txt", "w") as f:
        f.write(str(new_file))


def uploadToGoogleDriveServerWithDaemon(filepath):
    t = threading.Thread(target=uploadToGoogleDriveServer, args = (filepath,))
    t.daemon = True
    t.start()