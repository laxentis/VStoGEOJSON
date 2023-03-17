import urllib.request
import json
from geojson import Point, Feature, FeatureCollection, dump

status = ""
with urllib.request.urlopen('https://data.vatsim.net/v3/vatsim-data.json') as url:
    status = json.load(url)
#with open('status.json', 'w') as f:
#    json.dump(status, f)
features = []
for pilot in status['pilots']:
    position = Point((pilot['longitude'], pilot['latitude']))
    ft = Feature(
        geometry=position, properties={
            'cid': pilot['cid'],
            'name': pilot['name'],
            'callsign': pilot['callsign'],
            'server': pilot['server'],
            'altitude': pilot['altitude'],
            'groundspeed': pilot['groundspeed'],
            'transponder': pilot['transponder'],
            'heading': pilot['heading'],
            'QNH': {'inHg': pilot['qnh_i_hg'], 'mb': pilot['qnh_mb']},
            'flight_plan': pilot['flight_plan'] or "None",
            'departure':  'ZZZZ' if pilot['flight_plan'] is None else pilot['flight_plan']['departure'],
            'destination': 'ZZZZ' if pilot['flight_plan'] is None else pilot['flight_plan']['arrival'],
            'aircraft': 'UNKN' if pilot['flight_plan'] is None else pilot['flight_plan']['aircraft_short'],
            'logon_time': pilot['logon_time'],
            'last_updated': pilot['last_updated']
        }
    )
    features.append(ft)
feature_collection = FeatureCollection(features)
with open('status.geojson', 'w') as f:
    dump(feature_collection, f)
