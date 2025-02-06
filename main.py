import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import mysql.connector
import pygame
import RPi.GPIO as GPIO
import time
import subprocess
import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

####

####

pygame.mixer.init() # pygame chogihwa
def testt() :
    db=mysql.connector.connect(
        host='192.168.213.143',
        user='root',
        password='giga2',
        database='capstone'
    )
    cursor = db.cursor()

    def get_license_plate_from_database():
        query="SELECT car_num FROM car_number"
        cursor.execute(query)
        results=cursor.fetchall()
        
        return [result[0] for result in results]
        
        
    def compare_license_plates(result_chars, database_plate):
        if result_chars==database_plate:
            return True
        else:
            return False
	
    def send():
        smtp = smtplib.SMTP('smtp.gmail.com',587)
        smtp.starttls()
        smtp.login('iamdragon.dev@gmail.com','seiaowcbcfxvznvt')
        msg=MIMEMultipart()
        msg['Subject'] = '장애인 전용 구역 불법 주차 차량 신고합니다.'
        msg['To'] = 'mintehfl@naver.com'
        text = MIMEText('장애인 전용 구역 불법 주차 차량 번호입니다.')
        msg.attach(text)
        
        file_name='/home/giga2/yolov5/cropped_img.jpg'
		 
        with open(file_name, 'rb') as file_FD:
            etcPart = MIMEApplication(file_FD.read())
            etcPart.add_header('Content-Disposition', 'attachment', filename = file_name)
            msg.attach(etcPart)
            smtp.sendmail('iamdragon.dev@gmail.com', 'mintehfl@naver.com',msg.as_string())

        smtp.quit()

    def main(name2):
        database_plate=get_license_plate_from_database()
        
        if database_plate:
            found_match=False
            for db_plate in database_plate:
                if compare_license_plates(name2, db_plate):
                    print("번호판 일치")
                    print(db_plate)
                    found_match=True
                    break
            if not found_match:
                print("불일치")
                
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(17,GPIO.OUT)
                
                current_time=time.localtime()
                current_hour=current_time.tm_hour
                
                
                if current_hour<18:
                    pygame.mixer.music.load('/home/giga2/Downloads/alertsound.MP3')
                    pygame.mixer.music.play()
                    time.sleep(2)
                
                else:
                    GPIO.output(17, GPIO.HIGH)
                    time.sleep(2)
					
                send()
                ####
        
                print(db_plate)        
        db.close()
            

    if __name__=="__main__":
        for i in range(len(name1)):
            if not ord('가')<=ord(name1[i])<=ord('힣') or ord('A')<=ord(name[i])<=ord('Z') or ord('a')<=ord(name[i])<=ord('z'):
                name1[i]=int(name1[i])
                name1[i]=str(name1[i])
        result_name=''.join(name1)
        print(result_name)
        main(result_name)
        
def process_license_plate(input_str):
    input_str=re.sub(r'\s','',input_str)
    input_str = re.sub(r'^[^0-9가-힣]','',input_str)
    
    match = re.search(r'\d{2,3}[가-힣]\d{4}',input_str)
    
    if match:
        surffix_number_block=match.group()[-4:]
        return f"{match.group()[:-4]}{surffix_number_block}"
    surffix_number_block=input_str[-4:]
    return f"{input_str[:-4]}{surffix_number_block}"
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24
print("choumpa guri chukjungki")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("chogiwha")
time.sleep(2)

cnt=0
a=True
try:
    while True:
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start = time.time()
        
        while GPIO.input(ECHO)==1:
            stop = time.time()
            
        check_time = stop - start
        distance = check_time * 34300/2
        print("Distance : %.1f cm" % distance)
        time.sleep(1)
    
        
        if distance<=100:
            cnt+=1

            if cnt>=5 and a==True:
                import detect2
                opt=detect2.parse_opt()
                detect2.main(opt)
                cnt=0
                a=False
                name=pytesseract.image_to_string('/home/giga2/yolov5/cropped_img.jpg', lang='kor', config='--psm 8 --oem 1')
                charss=name.split('\n')[0:-1]
                name='\n'.join(charss)
                global name1
                name1=process_license_plate(name)
                name1=list(name1)
                print(name)
                
                testt()
            
        elif distance>100:
            cnt=0
            a=True
            pygame.mixer.music.stop()
            
        
except KeyboardInterrupt:
    print("guri chukjung clear")
    GPIO.cleanup()
