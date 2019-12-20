# Zumi

ROS를 사용하여 Zumi로 순찰차 만들기

## 기능

1. 노란선을 좌측에 둔 차선인식

2. 보라색을 인식 후 추적

3. 장애물 인식 시 정지

4. STOP SIGN 인식 시 정지

## Arduino

아두이노에 Arduino/zzuduino 업로드

### zzuduino

i2c 통신으로 raspberrypi에서 값을 받아

노란색(0~17)이면 라인트레이싱

보라색(255)면 일정 거리 내의 IR센서를 이용한 추적

STOP SIGN(100) 인식하면 정지

IR센서 값이 일정 값 이하면 정지

아무것도 인식 못하면 오른쪽으로 조금씩 회전

으로 기능 수행

## Pi 

RaspberryPi Zero에 ROS melodic 설치

http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi

workspace에 pi 다운 후 make

'imgsender.py', 'pi2ar.py' 실행

### imgsender.py

'sender' Node를 생성하여 picamera의 이미지를 'image_topic' Topic으로 Publish

cv_bridge를 이용하여 image 송신

통신속도를 빠르게 하기위해 frame을 100,100으로 낮춤

### pi2ar.py

마스터PC에서 받은 값을 I2C를 이용하여 Arduino로 전송

'pi' node를 생성하여 'yellow_x'와 'stop' topic을 Subscribe

평소(st==0)에는 'yellow_x' 값을 그대로 Arduino로 전송

STOP SIGN을 인식하면(st==200) 'stop' 값(200) Arduino로 전송

5번 전송 후 다시 'yellow_x' 값을 Arduino로 전송(라인트레이싱)

STOP SIGN 인식을 멈추면(st==0) count 초기화

## zumi_beta

마스터 PC의 workspace에 zumi_beta 다운 후 make

detector.py, stopdetector.py 실행
