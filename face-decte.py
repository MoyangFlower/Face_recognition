import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import base64
import baidu_face_decte
import time

cascPath = "haarcascades_cuda/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# 打开视频捕获设备
video_capture = cv2.VideoCapture(0)
path_name = "D:\\Doc_Record\\PyCharm\\Face_recognition\\data"
catch_pic_num = 4
max_identify_num = 4
identify_time = 0
num = 0
error_num =0
color = (0, 255, 0)
access_token =baidu_face_decte.get_access_token()
SUCCESS_flag = True
while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        break

    # 读视频帧
    ret, frame = video_capture.read()
    if not ret:
        break
    # 转为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 调用分类器进行检测
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32),)
    #flags=cv2.cv.CV_HAAR_SCALE_IMAGE)



    if len(faces) > 0:
        # 画矩形框
        for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 画出矩形框
            cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

            # 显示当前捕捉到了多少人脸图片了，这样站在那里被拍摄时心里有个数，不用两眼一抹黑傻等着
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'num:%d' % (num), (x + 30, y + 30), font, 1, (255, 0, 255), 4)

            num += 1
            if num < (catch_pic_num):  # 如果超过指定最大保存数量退出循环

                img_name = '%s\\%d.jpg' % (path_name, num)
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]

                cv2.imwrite(img_name, image)

            while identify_time < max_identify_num and SUCCESS_flag and error_num < 10:
                identify_time += 1
                f = open(img_name, 'rb')
                image = base64.b64encode(f.read())
                result = baidu_face_decte.identify_face(access_token, image)
                if result['result']:
                    score = result['result']['user_list'][0]['score']
                    print(result['error_msg'], score)
                    if score > 80:
                        print("成功登陆！欢迎 "+result['result']['user_list'][0]['user_info'])
                        SUCCESS_flag = False
                    else:
                        print("不好意思，你还未注册！")
                        error_num += 1
                        SUCCESS_flag = False



    # 显示视频
    cv2.imshow('Video', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# 关闭摄像头设备
video_capture.release()

# 关闭所有窗口
cv2.destroyAllWindows()
