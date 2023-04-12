from itertools import count
import cv2
import pandas as pd
import numpy as np
import os
from trainner import trainner
import json
from datetime import datetime

camera = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()


if os.path.exists('data-id.csv'):
    id_names = pd.read_csv('data-id.csv')
    id_names = id_names[['id', 'name']]
else:
    id_names = pd.DataFrame(columns=['id', 'name'])
    id_names.to_csv('data-id.csv')

if not os.path.exists('data'):
    os.makedirs('data')

print('Welcome!')
#print('\nPlease put in your ID.')
#print('If this is your first time choose a random ID between 1-10000')

# id = int(input('ID: '))
name = ''
if id in id_names['id'].values:
    name = id_names[id_names['id'] == id]['name'].item()
    print(f'Welcome Back {name}!!')
else:
    name = input('Please Enter you name: ')
    
    id_names = id_names.append({'id': id, 'name': name}, ignore_index=True)
    id_names.to_csv('data-id.csv')

print("\nLet's capture!")



count = 0

while 1:

    ret, image = camera.read()

    grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    face = cascade.detectMultiScale(grayImage,
                                    scaleFactor = 1.5,
                                    minNeighbors = 5,
                                    minSize= (30,30))

    for (x,y,w,h) in face:
        
        cv2.rectangle(image, (x,y), (x+w,y+h), (100,100,0), 2)
        face_region = grayImage [y:y + h, x:x + w]
        cv2.imwrite('dataset/User.' + str(id) + '.' + str(count) + '.jpg', grayImage[y:y+h+5, x:x+w+5])
        #img_name = f'face.{id}.{datetime.now().microsecond}.jpeg'
        #cv2.imwrite(f'faces/{id}/{img_name}',face_img)
        count += 1
        if np.average(face_region) :
            face_img = cv2.resize(face_region, (220, 220))
            img_name = f'face.{id}.{datetime.now().microsecond}.jpeg'
            cv2.imwrite(f'faces/{id}/{img_name}',face_img)
            count += 1


    if count == 300:
        break
    
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    cv2.imshow('Frame',image)
camera.release()
cv2.destroyAllWindows()

with open('users.json') as json_file:
    data = json.load(json_file)

username = {
            'name':name
           }
data[id] = username

with open("users.json", "w") as file:  
    json.dump(data, file,indent = 4)
    
trainner()
