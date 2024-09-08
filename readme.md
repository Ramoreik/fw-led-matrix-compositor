# Framework to use Framework's LED Matrix

The approach of this framework is to use `Pillow` to generate `9x34` black and white images.
Then we use `inputmodule-control` to provide them to the led matrix's controller as a black and white image.

Useful to use the matrixes as part of your `status` setups on linux, like show battery, brightness or volume percentage in fun ways.
You can also just animate scenes that react to certain events. (like catching a packet with scapy in the case of `packet-cat`)
It could be submitting a flag in a CTF as well, sky is the limit !

There are provided examples of what can be achieved in `rainfall.py`, `snowfall.py` and `packet-cat.py`.
This whole thing depends on `Pillow`, and `scapy` if you want to test out `packet-cat.py`.

If you find a bug or want new features/concepts added, feel free to contribute !
Enjoy :)

