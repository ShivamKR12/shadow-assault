from flask import Flask, render_template
import threading
import webview

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    webview.create_window('Ursina App', 'http://localhost:5000')
    webview.start()