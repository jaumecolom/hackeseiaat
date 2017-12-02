import requests as r
import cv2
import base64
from threading import Thread


def async_post(x, y, frame):
    img = encode_image(frame)
    result = r.post("http://openarms-alerts.000webhostapp.com/post-alert.php", data={'coor_x': x, 'coor_y': y, 'image': img})
    print(result.content)


def post_alert(x, y, frame):
    thread = Thread(target=async_post, args=(x, y, frame))
    thread.start()


def encode_image(image):
    img = cv2.imencode('.png', image)[1]
    return base64.b64encode(img)
