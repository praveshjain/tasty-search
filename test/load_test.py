from .. import Settings
import requests
import time
import urllib

total_time = 0
num_queries = 0
with open(Settings.HOME + '/../data/load.txt') as input_file:
    for line in input_file:
        if not line.strip():
            continue
        query_map = {'query': line}
        url = 'http://{IP}:{PORT}/search?{QUERY}'.format(IP=Settings.ELASTIC_IP, PORT=5000, QUERY=urllib.urlencode(query_map))
        start_time = time.time() * 1000
        resp = requests.get(url)
        assert resp.status_code == 200
        end_time = time.time() * 1000
        num_queries += 1
        total_time += end_time - start_time

print total_time
print num_queries
