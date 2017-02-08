import http.client
import json

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/event.json")
r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read().decode("utf-8")
conn.close()

print(json.loads(data1))
