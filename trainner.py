import cv2
import os
from PIL import Image
import numpy as np

def trainner():
    faceArr, ids = [], []

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    imagePath = [os.path.join('dataset',f) for f in os.listdir('dataset')]

    for paths in imagePath:
        if os.path.split(paths)[-1].split('.')[-1] != 'jpg':
            continue

        img = Image.open(paths).convert('L')

        imgArr = np.array(img,'uint8')

        faceId = int(os.path.split(paths)[-1].split('.')[1])

        face = cascade.detectMultiScale(imgArr)

        for (x,y,w,h) in face:
            faceArr.append(imgArr[y:y+h, x:x+w])
            ids.append(faceId)

    recognizer.train(faceArr,np.array(ids))
    recognizer.save('trainner.yml')
    print('Training Complete!')
