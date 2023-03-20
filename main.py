import sys                        # system specific parameters and functions : 파이썬 스크립트 관리

import args as args
import self as self
from PyQt5 import uic             # ui 파일을 가져오기위한 함수

from PyQt5.QtCore import *        # eventloop/스레드를 사용 할 수 있는 함수 가져옴.
from PyQt5.QtWidgets import QMainWindow, QApplication

################# 부가 기능 수행(일꾼) #####################################
from kiwoom import Kiwoom          # 키움증권 함수/공용 방 (싱글턴)
from Qthread_1 import Thread1      #
from Qthread_2 import Thread2      #

class Login_Machnine(QMainWindow):       # QMainWindow : PyQt5에서 윈도우 생성시 필요한 함수

    def __init__(self, *args, **kwargs):                      # Main class의 self를 초기화 한다.

        print("Login Machine 실행합니다.")
        super(Login_Machnine, self).__init__(*args, **kwargs)

        #### 기타 함수
        self.login_event_loop = QEventLoop()  # 이때 QEventLoop()는 block 기능을 가지고 있다.

        ####키움증권 로그인 하기
        self.k = Kiwoom()                     # Kiwoom()을 실행하며 상속 받는다. Kiwoom()은 전지적인 아이다.
        self.set_signal_slot()                # 키움로그인을 위한 명령어 전송 시 받는 공간을 미리 생성한다.
        self.signal_login_commConnect()

        self.get_stock_info()
        #self.get_condition_info()

    def set_signal_slot(self):
        self.k.kiwoom.OnEventConnect.connect(self.login_slot)  # 내가 알고 있는 login_slot에다가 특정 값을 던져 준다.

    def signal_login_commConnect(self):
        self.k.kiwoom.dynamicCall("CommConnect()")  # 네트워크적 서버 응용프로그램에 데이터를 전송할 수 있게 만든 함수
        self.login_event_loop.exec_()  # 로그인이 완료될 때까지 계속 반복됨. 꺼지지 않음.

    def get_stock_info(self):
        print("종목 정보 가져오기")
        ##### 1번 일꾼 실행
        h1 = Thread1(self)
        h1.start()

    def get_condition_info(self):
        print("종목 정보 가져오기")
        ##### 1번 일꾼 실행
        h2 = Thread2(self)
        h2.start()

    def login_slot(self, errCode):
        if errCode == 0:
            print("로그인 성공")
            #self.statusbar.showMessage("로그인 성공")
            #self.get_account_info()                    # 로그인시 계좌정보 가져오기

        elif errCode == 100:
            print("사용자 정보교환 실패")
        elif errCode == 101:
            print("서버접속 실패")
        elif errCode == 102:
            print("버전처리 실패")
        self.login_event_loop.exit()  # 로그인이 완료되면 로그인 창을 닫는다.

    #def get_account_info(self):
        #account_list = self.k.kiwoom.dynamicCall("GetLoginInfo(String)", "ACCNO")

if __name__=='__main__':             # import된 것들을 실행시키지 않고 __main__에서 실행하는 것만 실행 시킨다.
                                     # 즉 import된 다른 함수의 코드를 이 화면에서 실행시키지 않겠다는 의미이다.
    app = QApplication(sys.argv)     # PyQt5로 실행할 파일명을 자동으로 설정, PyQt5에서 자동으로 프로그램 실행
    CH = Login_Machnine()            # Main 클래스 myApp으로 인스턴스화
    #CH.show()                        # myApp에 있는 ui를 실행한다.
    app.exec_()                      # 이벤트 루프