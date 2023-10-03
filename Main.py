import cv2,time
import Voice as VC
import MotionDetector as MD
import LineUploder as LU
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

THROUD = 2.0e6
FPS = 60
max_presence_time = 0.5
max_absence_time = 1
presence_time = 0
absence_time = 0
prev_exist_state=[0,0]

isStarted = False
prev_exist = False
shot_flag = False

# クラスを読み込む
vc=VC.Voice(DIR_NAME)
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

while ret == True:
    # モーション関数
    flag,diff=md.detect(frame,THROUD,30)
    
    # 差分フレームを表示
    cv2.imshow("diff",diff)
    
    # 人が存在していない状態から初めて人が存在したか？
    if(not isStarted and not flag):
        isStarted=True
        vc.Speak("hello1")
        vc.Greeting_Speak()

    # 人の存在状況を更新し、前回との差分を取る
    human_exist=flag
    human_move=int(human_exist)-int(prev_exist)
    
    # 人が存在する場合、存在時間の制限値を増やす。
    if(human_exist):
        absence_time=0
        presence_time+=1
    # 存在しない場合、非存在時間の制限値を増やす
    else:
        presence_time=0
        absence_time+=1

    # 存在時間の制限値に基づいて、存在フラグを判断する
    exist_flag=[presence_time>max_presence_time*FPS,absence_time>max_absence_time*FPS]
    
    # 存在フラグが変化し、かつshot_flagがFalseである場合、LINE通知関数を呼び出す。
    if exist_flag[0]-prev_exist_state[0]==1 and not shot_flag and isStarted:
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
            sc_left.move(0)
        else:
            vc.Greeting_Speak()
            time.sleep(0.5)
            vc.Date_Speak()
            vc.WeekDay_Speak()
            time.sleep(0.5)
            vc.Time_Speak()
            lu.upload(frame)
            shot_flag=True
    elif exist_flag[1]-prev_exist_state[1]==-1:
        shot_flag=False

    # "q"キーが押された？
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    time.sleep(1/FPS)

    # 状態を更新
    prev_exist=human_exist
    prev_exist_state=exist_flag
    ret, frame = cap.read()

cv2.destroyAllWindows()
cap.release()
