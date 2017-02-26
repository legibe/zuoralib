import json
import requests

header = {
    'content-type': 'application/json'
}

body = {
    'hello': 'world',
    'SubscriptionName': 'ZZ-0000010'
}

url = 'https://localhost/subscriptionCreated'
url = 'https://52.41.210.72/subscriptionCreated'
r = requests.post(url=url, headers=header, data=json.dumps(body), verify=False)
print r.status_code, r.reason, r.json()
