import time
import BaseHTTPServer
from os.path import isfile as file_exists, getsize
import ipgetter
from constants import *
import threading
import socket

HOST_NAME = '' # that means localhost
EXTERNAL_IP = ""
INTERNAL_IP = ""

httpd = None # object to use on close

''' string!! '''
def get_ip():
    global EXTERNAL_IP, INTERNAL_IP
    if EXTERNAL_IP:
        return EXTERNAL_IP
    return INTERNAL_IP

''' integer!! '''
def get_port():
    return PORT_NUMBER

''' string!! '''
def get_download_url(img_id):
    ip = EXTERNAL_IP if EXTERNAL_IP else INTERNAL_IP
    return "http://" + ip + ":" + str(PORT_NUMBER) + "/" + str(img_id) + ".jpg"

def refresh_my_ip():
    global EXTERNAL_IP
    EXTERNAL_IP = ipgetter.myip()

def to_real_path(path_from_client):
    return "pic/" + path_from_client


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/php")
        s.end_headers()

    def do_GET(s): # my function. reem
        """Respond to a GET request."""
        img_string = s.path[1:]
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".

        if img_string: # if not empty string
            img_path = to_real_path(img_string)
            if file_exists(img_path):
                MyHandler.send_file(s, img_path)
                return

        # reached here? there is a problem with the file
        MyHandler.send_nothing(s)
    
    def send_nothing(s):
        print "nothing"
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>File not found</title></head>")
        s.wfile.write("<body><p>File was too old, so it has been deleted. Please come again to the museum to take another picture!</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")


    def send_file(s, filepath):
        s.send_response(200)
        s.send_header("Content-Type", "image/jpg")
        s.send_header("Content-Disposition", "attachment")
        s.send_header("Content-Length", getsize(filepath));
        s.end_headers()
        with open(filepath, 'rb') as f:
            s.wfile.write(f.read())
        print "file %s has finished serving!" % (filepath)

def init_server():
    global httpd, EXTERNAL_IP, INTERNAL_IP
#    MY_IP = ipgetter.myip()
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s %s:%s" % (HOST_NAME, EXTERNAL_IP, PORT_NUMBER)
    INTERNAL_IP = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    print "local ip: %s" % INTERNAL_IP
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        close_server()

def init_server_on_different_thread():
    t = threading.Thread(target=init_server, args = tuple())
    t.daemon = True
    t.start()


def close_server():
    global httpd
    if httpd is None: return

    httpd.server_close()
    print time.asctime(), "Server stops - %s %s:%s" % (HOST_NAME, EXTERNAL_IP, PORT_NUMBER)

