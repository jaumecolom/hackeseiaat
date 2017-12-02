import requests as r
import cv2
import base64


def post_alert(x, y, frame):
    img = encode_image(frame)
    r.post("http://openarms-alerts.000webhostapp.com/post-alert.php", data={'coor_x': x, 'coor_y': y, 'image': img})


def encode_image(image):
    img = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(img)
