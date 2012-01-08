#!/usr/bin/env python2
"""
Small script to send a WAKE-ON-LAN packet
to a computer on a network.

I'm not the original author of this script (only
tweaked it a bit) but I can't find who wrote it
anymore. anyways, WAKE-ON-LAN packets are fairly
simple to implement.

"""
import socket
import struct

def wake_on_lan(macaddress, ipaddress='<broadcast>', port=7):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
 
    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = '' 

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (ipaddress, port))

if __name__ == '__main__':
    # Use macaddresses with any seperators.
    #wake_on_lan('0F:0F:DF:0F:BF:EF')
    #wake_on_lan('0F-0F-DF-0F-BF-EF')
    # or without any seperators.
    #wake_on_lan('0F0FDF0FBFEF')
