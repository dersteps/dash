#!/usr/bin/python
'''
MIT License

Copyright (c) 2017 dersteps (stefan.matyba@googlemail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Make sure scapy is installed!
from scapy.all import *

class Dash:
    '''
    The Dash class is used to handle requests from Dash Buttons (well, other ARP
    requests are caught as well...) as easy as possible.
    '''

    def __init__(self):
        '''
        Constructor. Initializes a new instance of the Dash class, creates a new
        map of MAC addresses mapping to functions. Sets the mode to 'quiet'.
        '''
        self.macs = {}
        self.quiet = True
        self.counter = 0
        self.threshold = 100
        self.count = True

    def register(self, mac, func=None, name="Dash Button"):
        '''Register all MAC addresses you want Dash to recognize and pass a function
        to this method. The function is called like a callback whenever Dash recognizes
        an ARP request originating from a given MAC address.
        '''
        self.macs[mac] = (func,name)
        if not self.quiet:
            print "Registered function for MAC address '%s' (name: '%s')" % (mac, name)

    def arp_detect(self, packet):
        '''
        scapy callback on each captured package. Will analyze the packet's origin
        MAC address and look it up in the map of all recognized MAC addresses.
        If the address is found in the map, the mapped function will be called.
        '''
        sender_mac = packet.hwsrc

        if self.count is True:
            self.counter += 1

        # If enough packets have arrived, issue a message
        if self.counter % self.threshold == 0:
            if not self.quiet:
                print "Recorded %d ARP requests so far" % self.counter

        # If the sender's MAC address is mapped and there's actually something mapped to it...
        if sender_mac in self.macs and self.macs[sender_mac] is not None:
            # Get the function mapped to the address
            func = self.macs[sender_mac][0]
            # Get the name associated with it
            name = self.macs[sender_mac][1]
            if not self.quiet:
                print "MAC address '%s' is mapped to '%s'" % (sender_mac, name)
            if func is not None:
                # Call function
                func()

    def start(self):
        '''
        Starts the Dash service (by starting the scapy sniff process).
        '''
        if not self.quiet:
            print "Starting Dash...waiting for ARP packages to arrive"
        sniff(prn=self.arp_detect, filter="arp", store=0)
