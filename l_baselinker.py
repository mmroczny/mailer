import requests
import json



API_KEY = "1234-12345-IKXLUTWB3WTKCPQ567D91TSP1S66YXF2F5S9Q0N0XFV4NL1ZXXXXXXXXXXXXXXXX"
def baselinker_request(method, params = {}):
  return requests.post("https://api.baselinker.com/connector.php", data={
    "token": API_KEY,
    "method": method,
    "parameters": json.dumps(params)
  })
