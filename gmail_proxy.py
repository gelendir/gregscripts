#!/usr/bin/python2
"""
Simple SMTP Gmail proxy
By Gregory Eric Sanderson Turcot Temlett MacDonnell Forbes

One of the servers that I maintain has a crappy Exim that randomly crashes. In a fit of frustration,
while looking for a solution that would notify me when problems occured, I hacked together this script.
When monit can't send me warning messages through Exim, it sends them to my gmail account through
this script that acts as a backup SMTP server.

This script is licensed under the WTFPL license.
"""
import smtpd
import asyncore
import smtplib
import sys
import logging

class GmailProxy( smtpd.SMTPServer ):

    gmail_smtp = 'smtp.gmail.com'
    gmail_port = 587

    def __init__(self, localaddr, username, passwd, logger=None):
        smtpd.SMTPServer.__init__(self, localaddr, None)
        self._username = username
        self._passwd = passwd

        if not logger:
            logger = logging.getLogger()
            logger.addHandler( logging.NullHandler() )

        self.logger = logger

    def process_message(self, peer, mailfrom, rcpttos, data):

        self.logger.debug("Recevied request - peer : %s from : %s to : %s" % (peer, mailfrom, rcpttos) )

        server = smtplib.SMTP(self.gmail_smtp, self.gmail_port)

        server.starttls()
        server.ehlo()
        server.login(self._username, self._passwd)

        gmail_adress = "%s@gmail.com" % self._username

        try:
            server.sendmail( gmail_adress, rcpttos, data )
        except Exception as e:
            self.logger.error( e )
        else:
            self.logger.debug("Request sent")
        finally:
            server.quit()


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print """Simple SMTP Gmail Proxy

Starts an SMTP server and relays messages through Gmail's SMTP.

Usage : gmail_proxy.py username password [host=localhost] [port=1025] [log_file]
"""
        sys.exit()

    username, password = sys.argv[1:3]

    host = 'localhost'
    if len(sys.argv) > 3:
        host = sys.argv[3]

    port = 1025
    if len(sys.argv) > 4:
        port = int(sys.argv[4])

    logger = None
    if len(sys.argv) > 5:
        logger = logging.getLogger('gmail_proxy')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler( sys.argv[5], 'a')
        handler.setFormatter( logging.Formatter(fmt='%(asctime)s - %(message)s') )
        logger.addHandler(handler)

    proxy = GmailProxy( (host, port), username, password, logger )
    asyncore.loop()
