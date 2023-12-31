import cv2,time
import Voice as VC
import MotionDetector as MD
import LineUploder as LU
import time
# import ServoController as SC

Arduino=False

# デバイスによって変わる

# UPLOAD_IMAGE=r'/home/pi/Desktop/output.jpg'
# UPLOAD_IMAGE=r'/home/pi/Desktop/mimamori_Camera/output.jpg'
# DIR_NAME=r"/home/pi/Desktop/VOICE/{}.mp3"
UPLOAD_IMAGE=r'C:\Users\佃萌名\output.jpg'
DIR_NAME=r"c:\Users\佃萌名\Desktop\VOICE\{}.mp3"

# 変数を入れる
url="https://notify-api.line.me/api/notify"
token="XfeZrJIh1meAmMM38vJVlDoKvfzY2HrX2PpPEFqWRir"
headers = {"Authorization": "Bearer " + token}

THROUD = 25 #0~100 画面占有率
MAX_HUMAN_DETECTION=1 #秒数　人間検知秒数
RATE=75 #Call関数の喋る速度

human_detection=0
prev_flag = 0

isStarted = False
shot_flag = False

# クラスを読み込む
vc=VC.Voice(DIR_NAME,RATE)
md=MD.MotionDetector()
lu=LU.LineUploader(url, token, headers,UPLOAD_IMAGE)
if(Arduino):
    sc_left=SC.ServoController(0x8,0)
    sc_right=SC.ServoController(0x8,1)
vc.Speak("hello0")

# カメラ初期化
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
md.init_background(frame)
if(Arduino):
    sc_left.move(0)
    sc_right.move(0)

pre_time=time.time()
while ret == True:
    # 計測開始
    now_time=time.time()
    delta_time=now_time-pre_time
    if(delta_time>0.1):
        delta_time=0.1
    pre_time=now_time

    # モーション関数と差分フレーム
    flag,diff=md.detect(frame,THROUD,30)
    flag=int(flag)
    cv2.imshow("diff",diff)
    
    # 人が存在していない状態から初めて人が存在したか？
    if(not isStarted and not flag):
        isStarted=True
        vc.Speak("hello1")

    if(isStarted):
        if(flag):
            human_detection+=delta_time
        else:
            human_detection-=delta_time
        # human_detectionをある値に整形する
        if(human_detection > MAX_HUMAN_DETECTION ):
            human_detection=MAX_HUMAN_DETECTION
        elif(human_detection < 0):
            human_detection=0

    print("人間検知秒数",int(human_detection*1000),"ms")

    # 存在フラグが変化し、かつshot_flagがFalseである場合、LINE通知関数を呼び出す。
    if human_detection>=MAX_HUMAN_DETECTION and not shot_flag and isStarted:
        if(Arduino):
            sc_left.move(4)
        vc.Greeting_Speak()
        time.sleep(0.5)
        vc.Date_Speak()
        vc.WeekDay_Speak()
        time.sleep(0.5)
        vc.Time_Speak()
        lu.upload(frame)
        shot_flag=True
        if(Arduino):
            sc_left.move(0)
    elif flag-prev_flag==-1:
        shot_flag=False

    # "q"キーが押された？
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    # 状態を更新
    prev_flag=flag
    ret, frame = cap.read()
    print()

cv2.destroyAllWindows()
cap.release()
