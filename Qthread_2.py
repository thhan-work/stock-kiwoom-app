import requests
import os
import datetime
from PyQt5.QtTest import *
from PyQt5.QtCore import *         # 쓰레드 함수를 불러온다.
from kiwoom import Kiwoom          # 로그인을 위한 클래스
from PyQt5.QtWidgets import *      #PyQt import


class Thread2(QThread):
    def __init__(self, parent):   # 부모의 윈도우 창을 가져올 수 있다.
        super().__init__(parent)  # 부모의 윈도우 창을 초기화 한다.
        self.parent = parent      # 부모의 윈도우를 사용하기 위한 조건


        ################## 키움서버 함수를 사용하기 위해서 kiwoom의 능력을 상속 받는다.
        self.k = Kiwoom()
        ##################

        self.detail_account_info_event_loop = QEventLoop()

        self.k.kiwoom.OnReceiveConditionVer.connect(self.OnReceiveConditionVer)
        self.k.kiwoom.OnReceiveTrCondition.connect(self.OnReceiveTrCondition)

        self.GetConditionLoad()


        #for n in self.k.condition.list['Name']:
            #self.parent.kiwom_list.addItem(n)
            
    def GetConditionLoad(self):
        result = self.k.kiwoom.dynamicCall("GetConditionLoad")
        
        if result == 1:
            print("조건식 받기 성공")
        
        elif result != 1:
            print("조건식 받기 실패")

        self.detail_account_info_event_loop.exec_()

    def OnReceiveConditionVer(self):
        self.k.condition_list = []
        temporary_condition_list = self.k.kiwoom.dynamicCall("GetConditionNameList()").split(';')

        print(temporary_condition_list)
        k = 0

        for data in temporary_condition_list:

            try:
                a = data.split("^")
                obj = {'conditionCd' : str(a[0]), 'conditionNm' : str(a[1])}
                self.k.condition_list.append(obj)

            except IndexError:
                pass

        for data in self.k.condition_list:
            print(data['conditionCd'])
            print(data['conditionNm'])

            self.request_stock(str(data['conditionCd']), str(data['conditionNm']))
            QTest.qWait(3600)
            if k == 6:
                break

            k += 1


        #self.detail_account_info_event_loop.exit()

    def request_stock(self, conditionCd, conditionNm):

        print("종목검색식 종목 가져오기")
        print(conditionCd)
        print(conditionNm)

        result = self.k.kiwoom.dynamicCall("SendCondition(Qstring, Qstring, int, int)", "0150", conditionNm, conditionCd, 0)

        print(result)

        if result == 1:
            print("조건검색 종목 받기 성공")

        elif result != 1:
            print("조건검색 종목 받기 실패")

        self.detail_account_info_event_loop.exec_()

    def OnReceiveTrCondition(self, scrno, codelist, code_name, code_number, sPrevNext):
        self.k.code_list = []

        code = codelist.split(';')

        for data in code:

            try:
                self.k.code_list.append(data)

            except IndexError:
                pass

        print('OnReceiveTrCondition')
        print(scrno)
        print(code_name)
        print(code_number)
        print(sPrevNext)
        print(self.k.code_list)
        print('============ OnReceiveTrCondition =============')

        if sPrevNext == "2":
            self.request_stock(sPrevNext="2")
        else:
            self.detail_account_info_event_loop.exit()