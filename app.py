from flask import Flask, render_template, Response
import cv2 as cv

app = Flask(__name__)

camera = cv.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        frame = cv.flip(frame, 1)

        if not success:
            break
        else:
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/video', methods=["GET", "POST"])
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True)
# while(1):
#     generate_frames()
