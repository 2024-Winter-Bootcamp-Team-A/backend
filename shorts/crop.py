import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

def crop_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    new_width = 585.14
    new_height = 1024

    img_resized = img.resize((int(new_width), new_height), Image.LANCZOS)

    left = (img.width - new_width) / 2
    top = 0
    right = (img.width + new_width) / 2
    bottom = new_height

    img_cropped = img.crop((left, top, right, bottom))

    img_array = np.array(img_cropped)
    # RGB에서 BGR로 색상 순서 변경 (OpenCV 형식)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)


    return img_array




