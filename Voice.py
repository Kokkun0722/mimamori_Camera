import time
import datetime
import pygame.mixer
import time
from mutagen.mp3 import MP3
import datetime
import pyttsx3

class Voice:
    def __init__(self,DIR_NAME):
        # セットアップ
        self.name_list=["greeting","num","week","date","serif","hello"]
        for name in self.name_list:
            lines='self.{name}_list=[]\nfor i in range(100):\n\tself.{name}_list.append("{name}"+str(i))'.format(name=name)
            exec(lines)

        # 音声を取得
        pygame.mixer.init()
        print()
        self.now = datetime.datetime.now()
        self.hour=self.now.hour
        self.DIR_NAME=DIR_NAME

        # Call関係
        self.engine = pyttsx3.init()
    
    # 喋る
    def Speak(self, voice):
        name=self.DIR_NAME.format(voice)
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(1)
        audio=MP3(name)
        time.sleep(audio.info.length)

    # あいさつをする
    def Greeting_Speak(self):
        self.Speak(self.greeting_list[self.hour//6])

    # 曜日を喋る
    def WeekDay_Speak(self):
        W=self.now.weekday()
        self.Speak(self.week_list[W])

    # リスト順にしゃべる
    def List_Speak(self, data):
        for voice in data:
            self.Speak(voice)

    # 数字からリストに
    def Num_Speak(self, num):
        data=[]
        if(num<0):
            data.append(self.num_list[10])
            num=num*(-1)
        ten=num//10
        iti=num%10
        if(ten):
            data.append(self.num_list[10+ten])
        elif(not iti):
            data.append(self.num_list[0])
        if(iti):
            data.append(self.num_list[iti])
        self.List_Speak(data)

    # 日付をしゃべる
    def Date_Speak(self, m=0,n=2):
        M=self.now.month
        D=self.now.day

        date=[M,D]
        for i in range(m,n):
            self.Num_Speak(date[i])
            self.Speak(self.date_list[i])

    # 時間を喋る
    def Time_Speak(self, m=0,n=3):
        h=self.now.hour
        M=self.now.minute
        s=self.now.second

        date=[h,M,s]
        for i in range(m,n):
            self.Num_Speak(date[i])
            self.Speak(self.date_list[i+2])
            
    def Run_Date(self):
        self.Speak(self.serif_list[2])
        self.Date_Speak()
        self.WeekDay_Speak()
        self.Speak(self.serif_list[0])
        
    def Run_Time(self):
        self.Speak(self.serif_list[1])
        self.Time_Speak(n=2)
        self.Speak(self.serif_list[0])

    def Call(self, message):
        #喋らせる
        self.engine.say(message)
        self.engine.runAndWait()

if __name__=='__main__':
    DIR_NAME=r"/home/pi/Desktop/VOICE/{}.mp3"
    vc=Voice(DIR_NAME)
    """
    vc.Run_Date()
    vc.Run_Time()
    """
    vc.Call("文字列を読み上げるやつ。文字列から直接行けるよ。")

