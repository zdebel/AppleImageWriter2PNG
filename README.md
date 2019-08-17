A Python script to convert raw byte stream dedicated for an Apple Image Writer I printer into a PNG picture.

Usage:
python aiw2png.py filename.bin

Will output a processed PNG file named filename.bin.png.

I've tested the script with raw output of a Print Screen command on an Apple Mac LC III. The graphics.bin was provided by a friend
and comes from Apple ]['s Print Shop.

There are a few unsupported codes (mainly dedicated to page / font size). If you're able to provide binary dumps that don't work 
properly I can implement them.

The way I dumped the data is I simply connected a RS232 <-> USB converter accordingly and set the baud rate to 9600, 8n1 mode.
