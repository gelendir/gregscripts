#!/usr/bin/python2
import asyncore
import smtpd

server = smtpd.DebuggingServer( ('localhost', 25), None )
asyncore.loop()
