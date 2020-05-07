import json
import requests

matching_engine = "https://eu-mexdemo.dme.mobiledgex.net:38001"

register_response = requests.post(
    matching_engine + "/v1/registerclient",
    json={
        "app_name": "mexfastapi",
        "app_vers": "1.0",
        "org_name": "demoorg",
        "ver": 1,
    }).json()

if not register_response:
    AssertionError("Can't Retrieve Matching Engine Response")

session_cookie = register_response["session_cookie"]

findcloudlet_response = requests.post(
    matching_engine + "/v1/findcloudlet",
    json={
        "session_cookie": session_cookie,
        "carrier_name": "TDG",
        "gps_location": {
            "latitude": 48.0,
            "longitude": 11.0,
        },
        "ver": 1,
    }).json()

print(json.dumps(findcloudlet_response, indent=4))