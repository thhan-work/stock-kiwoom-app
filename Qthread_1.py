import os

import requests
from PyQt5.QtCore import *         # 쓰레드 함수를 불러온다.
from kiwoom import Kiwoom          # 로그인을 위한 클래스
from PyQt5.QtWidgets import *      #PyQt import
import paramiko
import csv

class Thread1(QThread):
    def __init__(self, parent):   # 부모의 윈도우 창을 가져올 수 있다.
        super().__init__(parent)  # 부모의 윈도우 창을 초기화 한다.
        self.parent = parent      # 부모의 윈도우를 사용하기 위한 조건


        ################## 키움서버 함수를 사용하기 위해서 kiwoom의 능력을 상속 받는다.
        self.k = Kiwoom()
        ##################

        ################## 사용되는 변수
        self.stock_Screen = "2000"         # 계좌평가잔고내역을 받기위한 스크린

        ###### 슬롯
        ##self.k.kiwoom.OnReceiveTrData.connect(self.trdata_slot)  # 내가 알고 있는 Tr 슬롯에다 특정 값을 던져 준다.
        self.deleteItemList()
        ###### 종목 가져오기
        self.getItemList()  # 종목 이름 받아오기

        self.sendItemListFTP()

    def deleteItemList(self):
        if os.path.exists("dist/stockInfo.csv"):
            os.remove("dist/stockInfo.csv")

    def getItemList(self):
        marketList = ["0", "10"]

        for market in marketList:
            codeList = self.k.kiwoom.dynamicCall("GetCodeListByMarket(QString)", market).split(";")[:-1]

            f = open("dist/stockInfo.csv", "a", encoding="utf8", newline='')  # "a" 달아 쓴다. "w" 덮어 쓴다. files라느 파이썬 페키지 볼더를 만든다.
            wr = csv.writer(f)
            wr.writerow(['TICKER', 'TICKER_NM', 'TICKER_TYPE', 'TICKER_STAT'])


            for code in codeList:
                name = self.k.kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
                stat = self.k.kiwoom.dynamicCall("GetMasterConstruction(QString)", code)
                # self.k.All_Stock_List.append({"종목코드": code, "종목명": name, "종목구분": market, "감리구분": stat})


                wr.writerow([code, name, market, stat])

                #f.write("%s\t%s\t%s\t%s\n" % (code, name, market, stat))  # t는 tap을 의미한다.
                #f.close()

            f.close()
    def sendItemListFTP(self):
        host = '34.64.233.250'
        port = 22
        transprot = paramiko.transport.Transport(host, port)
        username = 'stockdesk'
        password = 'stockdesk!@%^'

        # 연결
        transprot.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transprot)

        # Upload - 파일 업로드
        remotepath = '/home/stockdesk/daily-raw/conditions/stockInfo.csv'  # sftp에 업로드 될때 파일 경로와 파일이름(이렇게 저장이 됨)을 써줍니다.
        localpath = 'dist/stockInfo.csv'  # local피시의 파일 경로와 파일이름(pc에 저장되어있는 파일이름)을 써줍니다.
        sftp.put(localpath, remotepath)

        # Close - 꼭 닫아줍시다.
        sftp.close()
        transprot.close()

    def sendItemListApi(self):

        if os.path.exists("dist/stockInfo.txt"):
            f = open("dist/stockInfo.txt", "r", encoding="utf8")
            # text = open('rose_data.txt', 'rb')

            files = {
                'text': f
            }

            res = requests.post('https://~~~~', files=files)

            ##lines = f.readlines()  # 여러 종목이 저장되어 있다면 모든 항목을 가져온다.

            ##for line in lines:
            ##if line != "":  # 만약에 line이 비어 있지 않다면
            ##ls = line.split("\t")  # \t(tap)로 구분을 지어 놓는다.
            ##code = ls[0]
            ##name = ls[1]
            ##market = ls[2]
            ##stat = ls[3].split("\n")[0]
            ##self.Getanal_code.append([code, name, market, stat])
            f.close()