__author__ = 'reem'
import os
import urllib2

def check_in():

    fqn = os.uname()[1]
    ext_ip = urllib2.urlopen('http://whatismyip.org').read()
    print ("Asset: %s " % fqn, "Checking in from IP#: %s " % ext_ip)



import ipgetter
def check_in2():
    my_ip = ipgetter.myip()
    print my_ip
    print type(my_ip)

check_in2()


