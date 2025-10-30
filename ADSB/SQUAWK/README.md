# SQUAWK

This script transforms a provided CSV of squawk codes into a more usable format for ADSB/main.py by listing 
each code individually instead of in a range. The provided codes are specific to the UK, you may have to retrieve a 
list of codes specific to your region.
The input CSV has accidentally been deleted but should not be of relevance.

Squawk code list format found online (https://www.deeside.com/squawk-codes/), e.g.:
* 0003 	Surrey/Sussex HEMS (HLE60)
0004 — 0005 	Scottish Non-standard Flights

Preprocessing into CSV with regex search and replace in VSCode:
0003,,Surrey/Sussex HEMS (HLE60)
0004,0005,Scottish Non-standard Flights

Script output:
0003,Surrey/Sussex HEMS (HLE60)
0004,Scottish Non-standard Flights
0005,Scottish Non-standard Flights