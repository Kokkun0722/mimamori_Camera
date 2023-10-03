import cv2
import time
import datetime
import requests
import time
import datetime

class LineUploader:
    def __init__(self, url, token, headers, UPLOAD_IMAGE):
        self.url = url
        self.token = token
        self.headers = headers
        self.UPLOAD_IMAGE=UPLOAD_IMAGE
    
    def upload(self, frame):
        cv2.imwrite("output.jpg", frame)
        time.sleep(2)

        dt_now = datetime.datetime.now()
        payload = {"message": "\n" + str(dt_now) + "\n"}
        image = self.UPLOAD_IMAGE
        files = {'imageFile': open(image, 'rb')}

        requests.post(self.url, params=payload, headers=self.headers, files=files)