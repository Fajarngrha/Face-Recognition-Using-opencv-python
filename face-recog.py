from threading import Timer
import cv2
import json
import time
import requests
import schedule
import datetime
import pytz
from spreadsheet import *
import telegram_send






cascade = cv2.CascadeClassifier('haarcascade__frontalface_default.xml')
camera = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainnner.yml')
#bot = telebot.TeleBot('5777158360:AAHcVqTONs6KsKEp3IN72PH_rqWDYKKz8ps')
# bot = telebot.TeleBot("5777158360:AAHcVqTONs6KsKEp3IN72PH_rqWDYKKz8ps", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

img_counter = 0
frame_set = []

start = time.time()

def conect():
    try :
        r = requests.get(url,timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False




with open('users.json') as jsonFile:
    users = json.load(jsonFile)
    
userList = []
start_time = time.time()

def detect():
    
    ret, image = camera.read()
    #imgS = cv2.resize(imgS, (960, 540))
    #imgS = cv2.flip(imgS, 1)
    
    now = datetime.now()
    localtz = pytz.timezone("Asia/Jakarta")
    date = now.astimezone(localtz).strftime("%Y-%m-%d")
    waktos = now.astimezone(localtz).strftime("%H:%M")
   
    #t = now.strftime("%Y-%m-%d_%H-%M-%S")
    #capture = 'penyewa/'+t+'.jpg'
    #file = 'tidak/'+t+'.jpg'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(gray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    face = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 4, minSize = (30,30))
    faceId = {}

    for (x,y,w,h) in face:
        cv2.rectangle(image, (x,y), (x+w, y+h), (100,0,100), 2)
        faceId, percentage = recognizer.predict(gray[y:y+h, x:x+w])
       
        if percentage < 50:
            userList.append(faceId)
            faceId = users[str(faceId)]['name']+' '+str(round(125-percentage,2))+'%'
            telegram_send.send(messages=[faceId])
        
          
            
            cv2.putText(image, faceId, (x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)
        else :
            cv2.rectangle(image, (x,y), (x+w, y+h), (100,0,100), 2)
            faceId = 'Unknown'
            cv2.putText(image, faceId, (x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1, (50,255,),2)
            if time.time() - start_time >= 2: #<---- Check if 5 sec passed
                telegram_send.send(messages=[faceId])
            
            
          
        
    run = time.time()
    now = datetime.now()

    cv2.imshow('Image',image)
    cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThres", imgMedian)

 

 
    con = conect()
    if con == True :
        x = requests.post(url, obj)
        start = time.time()
        print(x.text)
    else :
        print ('koneksi tidak tersedia')


    # k = cv2.waitKey(30) & 0xff
    # if k == 27: # press 'ESC' to quit
    #     break

schedule.every(5).seconds.do(detect)
while 1:
    schedule.run_pending()
    time.sleep(1)
    



# userList = list(set(userList))
# if userList:
#     addToSpreadsheet(users,userList)
