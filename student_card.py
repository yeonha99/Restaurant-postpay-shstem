import cv2
import io
import os

from google.cloud import vision
from google.cloud.vision import types


client = vision.ImageAnnotatorClient()
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = capture.read()
    cv2.imshow("VideoFrame", frame)
    cv2.imwrite("./book_img/img.png", frame)

    filenames = os.listdir('./book_img')

    for filename in filenames:
        path = os.path.join('./book_img', filename)

        #Load the img into memory
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        with open('./book_txt/'+filename[0:-4]+'.txt', 'w') as f:
            f.write(texts[0].description)
            f.close()

        with open('./book_txt/'+filename[0:-4]+'.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line: break
                if '인하대학교' in line:
                    print("you are inha university student!!!")
                    break;
                if 'STUDENT' in line:
                    print("you are inha university student!!!")
                    break;

            f.close()

    if cv2.waitKey(1) > 0: break

capture.release()
cv2.destroyAllWindows()
