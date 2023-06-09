import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition
import time
import mysql.connector

#path = r'attendace\image_folder'
path =r'C:\Users\USER\OneDrive\Documents\PROJECT\attendace\image_folder'
url = 'http://192.168.43.158/cam-hi.jpg'
card_dict = {
    "MELEK": {"card": "1791937176", "qrcode": "MELEK_QR_CODE_STRING"},
    "ALI [ENG]": {"card": "384148168", "qrcode": "ALI_QR_CODE_STRING"},
    "MORAD [PR]": {"card": "323821322", "qrcode": "MORAD_QR_CODE_STRING"}
}
# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

mycursor = mydb.cursor()

# Create attendance table if it doesn't exist
mycursor.execute("CREATE TABLE IF NOT EXISTS attendance (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), time DATETIME, card DOUBLE, qrcode VARCHAR(255), authentication VARCHAR(255))")


images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    now = datetime.now()
    dtString = now.strftime('%Y-%m-%d %H:%M:%S')
    
    card_data = card_dict.get(name, {"card": "Unknown", "qrcode": "Unknown"})
    card = card_data["card"]
    qrcode = card_data["qrcode"]
    
    if card == "Unknown":
        print(f"Could not find card number for {name}")
        return
    
    sql = "INSERT INTO attendance (name, time, card, qrcode) VALUES (%s, %s, %s, %s)"
    val = (name, dtString, card, qrcode)
    mycursor.execute(sql, val)

    mydb.commit()


encodeListKnown = findEncodings(images)
print('Encoding Complete')

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    imgS = cv2.resize(img, (0, 0), None, 0.30, 0.30)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            cv2.destroyAllWindows() # close the OpenCV window when a face is detected
            exit()

    cv2.imshow('Face Recognation System for door security system (ALI)', img)
    cv2.resizeWindow('Face Recognation System for door security system (ALI)',320,240)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cv2.imread