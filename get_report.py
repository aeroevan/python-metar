#!/usr/bin/python
#
import os
import sys
import getopt
import string
import urllib.request, urllib.parse, urllib.error
from metar import metar

BASE_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations"

def usage():
    program = os.path.basename(sys.argv[0])
    print(("Usage: %s <station> [ <station> ... ]" % program))
    options = """Options:
    <station> . a four-letter ICAO station code (e.g., "KEWR")"""
    print(options)
    sys.exit(1)


stations = []
debug = False

try:
    opts, stations = getopt.getopt(sys.argv[1:], 'd')
    for opt in opts:
        if opt[0] == '-d':
            debug = True
except:
    usage()

if not stations:
    usage()

for name in stations:
    url = "%s/%s.TXT" % (BASE_URL, name)
    if debug:
        sys.stderr.write("[ "+url+" ]")
    try:
        urlh = urllib.request.urlopen(url)
        report = ''
        for line_b in urlh:
            line = line_b.decode('ascii')
            if line.startswith(name):
                report = line.strip()
                obs = metar.Metar(line)
                print((obs.string()))
                break
        if not report:
            print(("No data for %s\n\n" % (name,)))
    except metar.ParserError as err:
        print(("METAR code: "+ line))
        print((string.join(err.args,", ") + "\n"))
    except:
        print(("Error retrieving %s data\n" % (name,)))
        raise
