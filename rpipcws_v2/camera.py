from threading import Thread
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time


class VideoStream:  # customized PiVideoStream class from imutils
    def __init__(self, resolution=(320, 240), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(
            self.raw_capture, format='bgr', use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in preparation for the next frame
            self.frame = f.array
            self.raw_capture.truncate(0)
            # if the thread indicator variable is set, stop the thread and resource camera resources
            if self.stopped:
                self.stream.close()
                self.raw_capture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


class Camera:  # edited from Smart-Security-Camera by HackerShackOfficial on github, requires opencv
    def __init__(self):
        self.stream = VideoStream().start()
        time.sleep(2.0)

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        frame = self.stream.read()
        jpeg = cv2.imencode('.jpg', frame)[1]
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
