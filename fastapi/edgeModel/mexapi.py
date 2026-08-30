import json
import cv2
import requests
import datetime
import os

class Edge:
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

    token_server = register_response["token_server_uri"]
    token_response = requests.get(token_server, allow_redirects=False)
    token = token_response.headers["Location"].split("dt-id=")[1]

    verifylocation_response = requests.post(
        matching_engine + "/v1/verifylocation",
        json={
            "session_cookie": session_cookie,
            "carrier_name": "TDG",
            "gps_location": {
                "latitude": 48.0,
                "longitude": 11.0,
            },
            "verify_loc_token": token,
            "ver": 1,
        }).json()

    def registerClient(self):
        return json.dumps(self.findcloudlet_response, indent=4)

    def verifyLocation(self):
        return json.dumps(self.verifylocation_response, indent=4)

    def getFQDN(self):
        return self.findcloudlet_response["fqdn"]


class Video:
    def getStream(self):
        #self.cap = cv2.VideoCapture('/Users/paulocfborges/PycharmProjects/mexFastAPI/venv/fastapi/bin/edgeModel/videos/demovideo-2.mp4')
        self.cap = cv2.VideoCapture(os.environ["VIDEO_PATH"])

        while (True):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # grab the current timestamp and draw it on the frame
            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, .90, (0, 0, 255), 2)
            # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            (flag, encodedImage) = cv2.imencode(".jpg", frame)

            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')



        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

