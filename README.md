# 장애인 주차구역 불법주차 단속 시스템
## 🎙️ 과제 개요 및 목표
- 광주에서 장애인 주차구역에 **불법 주차**하는 사례가 **2021년 14,186건, 2022년 14,038**으로 나타남
- 주차구역이 부족해짐에 따라, 비장애인이 장애인 주차 구역에 불법 주차하는 경우가 많이 발생. 또한, 시민이 불법 주차를 신고하더라도 차주가 **신고자를 보복하는 경우도 다수 발생**하는 추세
- 이를 사전에 방지하고자 장애인 주차 구역 불법 주차 단속 시스템을 설계

## 🪄 기술 스택
- OS: Debian
- Language: Python
- DB: MariaDB

## ⏰ 개발 기간
- 2023.09.04. ~ 2023.12.01.

## ✨ 주요 기능
- 번호판 추출하여 DB 데이터와 일치/불일치 여부 판단
- 불일치할 경우 이메일 전송(무인 신고 기능)

### 수행 로직
1. 초음파 센서를 이용하여 장애인 주차구역에 차량이 주차하는 중인지 확인
   ![image](https://github.com/user-attachments/assets/e8f9fb09-340c-4bfb-8153-523e239bc3cc)

2. 차량이 2m 이내로 들어오고 5초 이상 머물 시, 카메라로 해당 차량 촬영
   - 카메라로 촬영한 이미지를 yolov5를 사용하여 번호판 인식한 후, bounding box 좌표를 가져와 crop하여 사진 저장
     
    ![image](https://github.com/user-attachments/assets/696ab92d-1b48-4d25-835a-fec7f23ee3bf)

3. crop한 사진에 pytesseract 적용하여 해당 차량 번호 출력
   - 출력된 문자열을 차량 번호에 알맞는 포맷으로 변경
     -> 숫자와 한글만 배열에 저장한 후, 한글 뒤에 4자리 숫자만 출력하도록 설정
     ![image](https://github.com/user-attachments/assets/15887544-514d-4519-9925-c062cb52a36d)

4. DB에 등록한 장애인 차량 번호와 추출한 번호가 일치하는지 판단, 불일치하는 경우 경고음이나 경고등 출력
     - 18시 이전 불일치 시, 경고음 발생
     - 18시 이후 불일치 시, LED 불빛 발생

5. 경고음/경고등 발생 이후, 주차된 차량이 나가지 않는 경우 해당 기관으로 촬영한 번호판 사진 전송
    ![image](https://github.com/user-attachments/assets/100b1ed7-6593-48f1-abae-8c448fb75645)


## 📹시연 동영상
**< 주간 시연 영상 >**

https://github.com/user-attachments/assets/b319e9ea-bb4f-4474-8462-9ed867ea88fe

**< 야간 시연 영상 >**

https://github.com/user-attachments/assets/be3d34cd-cc85-4b21-9c03-14912df8d8c6





