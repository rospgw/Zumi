# Zumi

ROS를 사용하여 Zumi로 순찰차 만들기

# 기능

1. 노란선을 좌측에 둔 차선인식

2. 보라색을 인식 후 추적

3. 장애물 인식 시 정지

4. STOP SIGN 인식 시 정지

# Arduino

아두이노에 Arduino/zzuduino 업로드

# Pi 

RaspberryPi Zero에 ROS melodic 설치

http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi

workspace에 pi 다운 후 make

imgsender.py, pi2ar.py 실행

# zumi_beta

마스터 PC의 workspace에 zumi_beta 다운 후 make

detector.py, stopdetector.py 실행
