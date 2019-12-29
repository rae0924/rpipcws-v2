from rpipcws_v2 import app
from rpipcws_v2.camera import Camera, gen
from flask import render_template, request, Response

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/video_feed', methods=['GET'])
def video_feed():
    if request.method == 'GET':
        return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')