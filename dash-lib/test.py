#!/usr/bin/python
'''
MIT License

Copyright (c) 2017 dersteps

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

# Import Dash library
from dash import Dash

# Create new Dash service
dash = Dash()

# Make it quiet
dash.quiet = False

# The callback we will assign to the MAC address associated with the Dash Button
# we'll use as a doorbell
def doorbellCallback():
    print "Doorbell is ringing!"

# The callback we will assign to the MAC address associated with the Dash Button
# we'll use to toggle a light
def livingRoomLightCallback():
    print "Toggle living room lights"


# Replace "xx:xx:xx:xx:xx:xx" and "yy:yy:yy:yy:yy:yy" with your Dash Buttons' actual MAC addresses
dash.register("xx:xx:xx:xx:xx:xx", func=doorbellCallback, name="Doorbell")
dash.register("yy:yy:yy:yy:yy:yy", func=livingRoomLightCallback, name="Living room lights")

# Start Dash (requires root)
dash.start()
