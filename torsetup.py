#!/usr/bin/env python
import base
import urllib2
import socket

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

try:
    import socks
    # safe normal socket stuff in case we can not find Tor socket
    originalDefaultproxy = socks._defaultproxy
    originalSocket = socket.socket
    originalCreate_connection = socket.create_connection

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", base.TORPORT)

    # patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

    ip = urllib2.urlopen('http://icanhazip.com').read()
    print "Tor socket found. Your IP seems to be: ", ip
except Exception as e:
    if type(e) != urllib2.URLError:  # URLError --> no Tor
        import traceback
        print traceback.format_exc()
    print
    try:
        socks._defaultproxy = originalDefaultproxy
        socket.socket = originalSocket
        socket.create_connection = originalCreate_connection
    except NameError:
        pass
    print "Tor connection failed - your IP will be revealed to blockchain.info"
    print "Press <enter> to continue anyway, <ctrl-c> to cancel."
    raw_input()
