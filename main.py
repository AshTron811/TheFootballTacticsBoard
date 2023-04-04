# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 18:04:45 2021

@author: DELL
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8)

img1=cv2.imread('Background/FootballPythonBg.png',cv2.IMREAD_UNCHANGED)

class DragImg():
    def __init__(self,path,posOrigin):
        self.posOrigin=posOrigin
        self.path=path
        
        self.img=cv2.imread(self.path,cv2.IMREAD_UNCHANGED)
        
        self.size=self.img.shape[:2]
    
    def update(self,cursor):
        ox,oy=self.posOrigin
        h,w=self.size
        #Check if in region
        if ox<cursor[0]<ox+w and oy<cursor[1]<oy+h:
            self.posOrigin=cursor[0]-w//2,cursor[1]-h//2

path='FootballPython'
myList=os.listdir(path)
print(myList)

y=10
listImg=[]
for x,pathImg in enumerate(myList):
    i=x
    if i%8==0:
        y+=60
        
    listImg.append(DragImg(f'{path}/{pathImg}',[y,(i%8)*80]))

print(len(listImg))

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img, flipType=False)
    
    h,w,_=img1.shape
    img=cvzone.overlayPNG(img, img1,[0,0])
    
    if hands:
        lmList=hands[0]['lmList']
        #Check if clicked
        length,info,img=detector.findDistance(lmList[4], lmList[8],img)

        if length<80:
            cursor=lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)
            
    try:
        for imgObject in listImg:
            h,w=imgObject.size
            ox,oy=imgObject.posOrigin
            img=cvzone.overlayPNG(img, imgObject.img,[ox,oy])
    except:
        pass
    
    cv2.imshow('Image',img)
    cv2.waitKey(1)