#!/usr/bin/env python3
"""
Azure Automation documentation : https://aka.ms/azure-automation-python-documentation
Azure Python SDK documentation : https://aka.ms/azure-python-sdk
"""
import socket
import ssl
import re,sys,os,datetime

def ssl_expiry_date(domainname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=domainname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)
    conn.connect((domainname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt).date()

def ssl_valid_time_remaining(domainname):
    """Number of days left."""
    expires = ssl_expiry_date(domainname)
    return expires - datetime.datetime.utcnow().date()
    
#####Main Section
# client = boto3.client('sns')
def lambda_handler(event, context):
#    HOST_LIST = os.environ.get('HOSTLIST', '').split(',')
    HOST_LIST = "az03pfgdidevjnk01.dev.az03.pfgdi.cloud"
    HOST_LIST = HOST_LIST.split(',')
    HOST_LIST = filter(None, (x.strip() for x in HOST_LIST))
    for dName in HOST_LIST:
        print(dName)
        expDate = ssl_valid_time_remaining(dName.strip())
        (a, b) = str(expDate).split(',')
        (c, d) = a.split(' ')
    # Critical alerts 
        if int(c) < 7:
            print('Critical')
      # Frist critical alert on 20 th day      
        elif int(c) == 10:
            print('Warning')
    #third warning alert on 30th day      
        elif int(c) == 14:
            print('Warning')
        else:
            print('Everything Fine..')

lambda_handler(False, False)