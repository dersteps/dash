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
from pprint import pprint

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
        self.threshold = 10
        self.count = True
        self.seen_first = False
        self.mode = "dhcp"
        self.iface=None
        self.discovered = {}
        self.amazon_ouis = [
            "F0D2F1", "F0272D", "AC63BE", "A002DC", "94BA31", "8871E5", "8841C1", "84D6D0", "74C246", "747548", "70B3D5", "6854FD", 
            "5CC9D3", "50F5DA", "50B363", "44650D", "34D270", "0C47C9", "001A90"
        ]

    def register(self, mac, func=None, name="Dash Button"):
        '''Register all MAC addresses you want Dash to recognize and pass a function
        to this method. The function is called like a callback whenever Dash recognizes
        an ARP request originating from a given MAC address.
        '''
        self.macs[mac] = (func,name)
        if not self.quiet:
            print "Registered function for MAC address '%s' (name: '%s')" % (mac, name)

    def dhcp_detect(self, packet):
        '''
        scapy callback on captured packets. Will check the packet's source MAC address.
        If that MAC is recognized, the function mapped to it will be executed.
        '''

        if not self.quiet:
            print "Detected DHCP request from %s" % packet.src

        if self.count is True:
            self.counter += 1

        # If enough packets have arrived, issue a message
        if self.counter % self.threshold == 0:
            if not self.quiet:
                print "Recorded %d DHCP requests so far" % self.counter

        # If the sender's MAC address is mapped and there's actually something mapped to it...
        if packet.src in self.macs and self.macs[packet.src] is not None:
            # Get the function mapped to the address
            func = self.macs[packet.src][0]
            # Get the name associated with it
            name = self.macs[packet.src][1]
            if not self.quiet:
                print "MAC address '%s' is mapped to '%s'" % (packet.src, name)
            if func is not None:
                # Call function
                pkt_id = packet.id

                if pkt_id == 1:
                    self.seen_first = True
                    return
                elif pkt_id == 2:
                    if self.seen_first:
                        # This is it!
                        self.seen_first = False
                        func()
         

    def arp_detect(self, packet):
        '''
        scapy callback on each captured package. Will analyze the packet's origin
        MAC address and look it up in the map of all recognized MAC addresses.
        If the address is found in the map, the mapped function will be called.
        '''
        sender_mac = packet.hwsrc
        target_mac = packet.hwdst

        if not self.quiet:
            print "Detected ARP request from %s to %s" % (sender_mac, target_mac)

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

    def amazon_mac(self, oui):
        if "".join(oui[0:8].split(":")).upper() in self.amazon_ouis:
            return True
        return False

    def discover_stop_filter(self, packet):
        if self.counter >= self.threshold:
            for oui in self.discovered.keys():
                if self.amazon_mac(oui):
                    print "Likely a Dash button, or other Amazon device: %s" % oui 
            return True
        return False


    def discover(self, packet):
        self.counter += 1
        if not packet.src in self.discovered:
            self.discovered[packet.src] = 0
            amazon = self.amazon_mac(packet.src)
            add = "non-Amazon MAC"
            if amazon:
                add = "Amazon MAC"
            print "Discovered MAC '%s' (%s)" % (packet.src, add)
        self.discovered[packet.src] += 1
        out = "\r"
        

    def start(self):
        '''
        Starts the Dash service (by starting the scapy sniff process).
        '''
        if self.mode is None:
            print "Warning: No mode set, falling back to 'dhcp'"
            self.mode = "dhcp"

        if not self.quiet:
            if self.iface is None:
                print "Starting Dash (all interfaces, mode: %s)" % self.mode
            else:
                print "Starting Dash (%s, mode: %s)" % (self.iface, self.mode)

        if self.mode is not None:
            if self.mode is "dhcp":
                sniff(iface=self.iface, filter="udp and (port 67 or 68)", prn=self.dhcp_detect, store=0)
            elif self.mode is "arp":
                sniff(iface=self.iface, prn=self.arp_detect, filter="arp", store=0)
            elif self.mode is "discover":
                print "Will listen until %d packets (set via dash.threshold) are captured" % self.threshold
                sniff(iface=self.iface, prn=self.discover, filter="arp or (udp and (port 67 or 68))", store=0, stop_filter=self.discover_stop_filter)
            else:
                print "Error: unrecognized mode '%s', use 'dhcp' or 'arp'" % mode
