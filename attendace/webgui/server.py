import os
import json
import base64
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')



def home():
    json_file_path = 'Attendance.json'
    image_folder_path = 'C:\\Users\\USER\\OneDrive\\Documents\\PROJECT\\attendace\\image_folder'

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        image_path = os.path.join(image_folder_path, item['name'] + '.jpg')
        with open(image_path, 'rb') as f:
            image_data = f.read()

        item['image'] = base64.b64encode(image_data).decode()

    return render_template('logs.html', user_data=data)

if __name__ == '__main__':
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

