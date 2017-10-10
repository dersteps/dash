# Dash
Hacking Amazon Dash Buttons for fun

This repository contains scripts etc. for hacking Amazon Dash Buttons.

It's mostly a personal repository, so don't expect much documentation...

## Update 10.10.2017
Just found out why the previous version was not working in my network. Amazon seems to have changed the way the Dash Buttons work.
My button did not send a single ARP request, no matter how often I pressed it. Turns out they now send two consecutive DHCP requests (first has ID 1, second has ID 2). 

I changed Dash accordingly, so you can now easily react to button presses even with the newer versions. Have fun!

See `test.py` for an example.
