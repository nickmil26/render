from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Set in Render environment variables
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Your channel username with @ or channel ID

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No file selected', 400
    
    # Send to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': (file.filename, file.stream, file.mimetype)}
    data = {'chat_id': CHANNEL_ID}
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        return 'Image successfully posted to Telegram channel!'
    else:
        return f'Error posting to Telegram: {response.text}', 500

if __name__ == '__main__':
    app.run(debug=True)