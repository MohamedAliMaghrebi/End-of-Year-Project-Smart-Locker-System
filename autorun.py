import subprocess
import threading

# Define a function to run a Python script
def run_script(script_name):
    subprocess.call(["python", script_name])

# Define a list of script names to run
script_names =["face.py","qr.py","esp.py","base.py"]
#script_names=["esp.py","face_detection_attendace.py"]

# Create a list of threads for running the scripts
threads = []
for script_name in script_names:
    thread = threading.Thread(target=run_script, args=[script_name])
    threads.append(thread)

# Start the first thread to run the first script
current_thread = threads.pop(0)
current_thread.start()

# Continuously monitor the running threads and start the next thread once the current thread has finished running
while threads:
    # Wait for the current thread to finish running
    current_thread.join()
    
    # Start the next thread to run the next script
    current_thread = threads.pop(0)
    current_thread.start()

# Wait for the last thread to finish running
current_thread.join()
