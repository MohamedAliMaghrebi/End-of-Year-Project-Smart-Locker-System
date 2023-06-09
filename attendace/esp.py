import socket
import threading
import mysql.connector
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

# Function to check if the card number is present in the database
# Function to check if the card number is present in the database and return authentication status
def check_card_number(card_number):
    query = "SELECT authentication FROM attendance WHERE card = %s"
    cursor.execute(query, (card_number,))
    result = cursor.fetchone()
    if result:
        if result[0] == 'TRUE':
            return "Green"  # Authentication is True
        else:
            return "Red"  # Authentication is not True
    else:
        return "Scan your Qr Code first before the URFID CARD"  # QR code needs to be scanned first


# Function to close the database connection
def close_db():
    cursor.close()
    db.close()
    print("Database connection closed.")

# Register the close_db function to be called when the script exits
atexit.register(close_db)

# Set up TCP/IP socket server on port 17
HOST = ''  # listen on all available interfaces
PORT = 17
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print(f'Server listening on port {PORT}')

def handle_request(conn, addr):
    # Receive card number from device
    card_number = conn.recv(1024).decode().strip()
    print(f'Received card number {card_number} from {addr}')

    # Check if the card number is present in the database
    status = check_card_number(card_number)

    # Send back status to device
    conn.send(status.encode())
    print(f'Sent status {status} to {addr}')

    # Close connection
    conn.close()

while True:
    # Accept incoming connection
    conn, addr = s.accept()
    print(f'Connected to {addr}')

    # Handle request in a separate thread
    t = threading.Thread(target=handle_request, args=(conn, addr))
    t.start()
