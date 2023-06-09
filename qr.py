import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import mysql.connector
import urllib.request
import atexit

# Create a connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

# Create a cursor to execute SQL queries
cursor = db.cursor()

# Function to check if the data is present in the attendance table
def check_data(data):
    query = "SELECT qrcode, name FROM attendance WHERE qrcode = %s"
    cursor.execute(query, (data,))
    result = cursor.fetchone()
    if result:
        print("Attendance already marked for QR code:", result[0], "Owner:", result[1])
        query = "UPDATE attendance SET authentication = 'TRUE' WHERE qrcode = %s"
        cursor.execute(query, (data,))
        db.commit()
        print("Authentication marked as True for QR code:", data)

    else:
        query = "INSERT INTO attendance (qrcode) VALUES (%s)"
        cursor.execute(query, (data,))
        db.commit()
        print("Attendance marked for QR code:", data)


# Function to close the database connection
def close_db():
    cursor.close()
    db.close()
    print("Database connection closed.")

# Register the close_db function to be called when the script exits
atexit.register(close_db)

font = cv2.FONT_HERSHEY_PLAIN

url='http://192.168.43.158/'
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

prev=""
pres=""
while True:
    img_resp=urllib.request.urlopen(url+'cam-hi.jpg')
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        pres=obj.data
        if prev == pres:
            continue
        else:
            print("Type:", obj.type)
            print("Data:", obj.data.decode())
            prev=pres
            # Check if the QR code data is present in the attendance table
            check_data(obj.data.decode())

        cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                    (255, 0, 0), 3)
        cv2.destroyAllWindows() # close the OpenCV window when a face is detected
        exit()

    cv2.imshow("live transmission", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
