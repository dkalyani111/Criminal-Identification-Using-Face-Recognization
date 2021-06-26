import cv2
import numpy as np 
import sqlite3
from dbConnection import insert_police_record
import mysql.connector as con
import os
#conn = sqlite3.connect('database.db')
#c = conn.cursor()
import datetime
from datetime import timedelta
import Single_Email as se
def mark_attend():
  fname = "recognizer/trainingData.yml"
  if not os.path.isfile(fname):
    print("Please train the data first")
    exit(0)
  face_cascade = cv2.CascadeClassifier('haar.xml')
  cap = cv2.VideoCapture(0)
  recognizer = cv2.face.LBPHFaceRecognizer_create()
  recognizer.read(fname)
  if True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
      ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
      #print(conf)
      nn=log(ids)
      name=""
      
      #print(nn)
      for i in nn:
        print (i[1])
        name=i[1]
        #if(i[7]=="Red"):
         # print("red")
        db = con.connect(host="localhost", user="root", password="", database="db_accident")
        cur = db.cursor()
        query="SELECT head_name,email,lat_, long_,min(sqrt(pow((69.1 * (lat_ - (19.0948))), 2) +pow((69.1 * ((74.7480) - long_) * cos(lat_ / 57.3)), 2))) AS distance FROM tbl_police "
        cur.execute(query)
        names=cur.fetchall()
        
        for row,prediction in zip(names,nn):
              print(nn)
              print(row)
              
              location="http://maps.google.com/?q="+str(19.0948)+","+str(74.7480)
              msg ="Dear "+str(row[0])+",\nCriminal spotted.\nDetails are as Follow:\n"
              details="Name: " +str(nn[0][1])+"\nMobile: "+str(nn[0][2])+"\nCrime Details:"+str(nn[0][4])+"\nAddress: "+str(nn[0][3])+"\nAdhar:" +str(nn[0][5])+"\nLocation: "+location
              print(msg+details)
              se.send_email(str(row[1]),msg+details)
              
   
      if conf < 100:
        cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
      else:
        cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
    cv2.imshow('Face Recognizer',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
      pass
  cap.release()
  cv2.destroyAllWindows()


def log(id):
    flag=str(id)
    db = con.connect(host="localhost", user="root", password="", database="db_accident")
    cur = db.cursor()
    
    query="select * from tbl_criminal_record where id='"+flag+"'"
    cur.execute(query)
    names=cur.fetchall()
    for row in names:
       return names

    db.commit()
 


