import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import csv

# Variables provided in ../.env
LAT = os.getenv('FEEDER_LAT', '0.000')
LON = os.getenv('FEEDER_LONG', '0.000')
DST = os.getenv('HELIWATCH_RAD_NAUTICAL_MILES', '2')

SQUAWKS = {}
ICAO = []

with open('squawks.csv', mode='r') as file:
    squawks_csv = csv.DictReader(file)
    for row in squawks_csv:
        SQUAWKS.update({row.get('squawk'): row.get('function')})

with open('icao.csv', mode='r') as file:
    icao_csv = csv.DictReader(file)
    for row in icao_csv:
        ICAO.append(row)

# ADSBFI API provides the HEX code of the aircrafts within a certain radius of the given coordinates
ADSBFI = "https://opendata.adsb.fi/api/v2/lat/" + str(LAT) + "/lon/" + str(LON) + "/dist/" + str(DST)
HEX = ""

# HEXDB API provides information on the owner (among other things) of the queried aircraft (in this case a heli)
HEXDB = "https://hexdb.io/api/v1/aircraft/"
OWNER = ""

SQUAWK = ""

def identify_nearest_heli(aircrafts):
    return [item for item in aircrafts if 'hex' in item and 't' in item and item.get('t') in ICAO]

# Create HTTP Server to publish data required for the Rainmeter skin
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global HEX
        global OWNER
        global SQUAWK
        self.send_response(200)
        self.end_headers()
        data = requests.get(url=ADSBFI).json()
        aircrafts = data["aircraft"]
        if aircrafts:
            aircrafts.sort(key=lambda x: x["dst"])
            nearest_heli = identify_nearest_heli(aircrafts)
            if nearest_heli:
                if 'hex' in nearest_heli[0] and not nearest_heli[0]['hex'] == HEX:
                    HEX = nearest_heli[0]['hex']
                    SQUAWK = ""
                    if 'squawk' in nearest_heli[0]:
                        SQUAWK=SQUAWKS.get(nearest_heli[0]['squawk'])
                    owner = requests.get(url=HEXDB + nearest_heli[0].get('hex')).json().get('RegisteredOwners')
                    if owner:
                        OWNER = owner
                        self.wfile.write(owner.encode('ASCII') + " - ".encode('ASCII') + SQUAWK.encode('ASCII'))
                    else:
                        self.wfile.write("Mystery Owner of Heli".encode('ASCII') + " ".encode('ASCII') + HEX.encode('ASCII') + " - ".encode('ASCII') + SQUAWK.encode('ASCII'))
                else:
                    self.wfile.write(OWNER.encode('ASCII') + " - ".encode('ASCII') + SQUAWK.encode('ASCII'))
            else:
                self.wfile.write("Unidentifiable Heli".encode('ASCII'))
        else:
            self.wfile.write("Heli Free Zone".encode('ASCII'))


if __name__ == "__main__":
    print(ADSBFI)
    httpd = HTTPServer(('', 8003), SimpleHTTPRequestHandler)
    httpd.serve_forever()
