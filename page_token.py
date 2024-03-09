from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal 

from Ui_token import Ui_Token

from utils import logger
import requests
import json
import traceback
from pathvalidate import is_valid_filename

from qfluentwidgets import MessageBox

def get_page(token):
    url = "https://ak.hypergryph.com/user/api/inquiry/gacha?page=1&token=" + token + "&channelId=1"
    print(url)
    try:
        r = requests.get(url)
        s = r.content.decode("utf-8")
        j = json.loads(s)
    except Exception:
        logger.error("登录失效: " + traceback.format_exc())
        return -1
    # logger.debug(j['data']['list'])
    # logger.debug(j['data']['pagination'])
    try:
        # print(j)
        all_page = j['data']['pagination']['total']
        return all_page
    except KeyError:
        logger.error("登录失效: " + traceback.format_exc())
        return -1


def get_record(token, all_page, username):
    record = []
    num =  0
    ddl = 0

    # 与本地记录合并
    try :
        f = open(username + '_record_json.json', 'r', encoding='utf-8')
        a = json.loads(f.read())
        ddl = a[0]['ts']
        print(ddl)
        f.close()
    except FileNotFoundError:
        logger.error("与本地记录合并，无本地记录: " + traceback.format_exc())

    for page in range(all_page):
        url = "https://ak.hypergryph.com/user/api/inquiry/gacha?page=" + str(page + 1) + "&token=" + token + "&channelId=1"
        r = requests.get(url)
        s = r.content.decode("utf-8")
        j = json.loads(s)

        # logger.debug("ts & ddl: " + str(j['data']['list']) + ", " + str(ddl))
        if ((len(j['data']['list']) == 0) or (j['data']['list'][0]['ts'] <= ddl)):
            # 不存在新记录
            break

        for i in j['data']['list']:
            ts = i['ts']
            pool = i['pool']
            # {name, rarity, isNew}
            chars = i['chars']
            # logger.debug(chars)

            for j in chars:
                # logger.debug(j)
                if (ts > ddl): 
                    # 只保存新记录
                    record.append({'ts': ts, 'pool': pool, 'name': j['name'], 'rarity': j['rarity'], 'isNew': j['isNew']})
                    # logger.debug(record[num])
                    num = num + 1

                
    if ((len(record) != 0) and (ddl == 0)):
        # 存在新记录 且 不存在本地记录
        json_dict = json.dumps(record, indent=2, sort_keys=False, ensure_ascii=False) # 写为多行
        with open(username + "_record_json.json", "w", encoding='utf-8') as f:
            f.write(json_dict)
    elif ((len(record) != 0) and (ddl != 0)):
        # 存在新记录 且 存在本地记录
        with open(username + '_record_json.json', "r+", encoding='utf-8') as f:
            old = json.loads(f.read())
            f.seek(0)
            record += old
            json_dict = json.dumps(record, indent=2, sort_keys=False, ensure_ascii=False) # 写为多行
            f.write(json_dict)
        
    logger.info("寻访数据获取完成")


class Page_token(QWidget, Ui_Token):
    signal_str = pyqtSignal(str)


    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setupUi(self)

        self.PushButton.clicked.connect(self.click_bnt)
        self.username = "default"
        self.token = ""
        

    def click_bnt(self):
        self.token = self.LineEdit.text()
        self.token = self.token.replace(' ', '')
        self.token = self.token.replace('+', '%2B')
        self.token = self.token.replace('/', '%2F')
        self.token = self.token.replace('?', '%3F')
        self.token = self.token.replace('#', '%23')
        self.token = self.token.replace('&', '%26')
        self.token = self.token.replace('=', '%3D')

        if (is_valid_filename(self.LineEdit_4.text()) or self.LineEdit_4.text() == ""):
            self.username = self.LineEdit_4.text()

            if (self.username == ""):
                self.username = "default"

            if (self.token == ""):
                # 无寻访凭证，直接读取文件
                try :
                    f = open(self.username + '_record_json.json', 'r', encoding='utf-8')
                    f.close()
                    self.LineEdit.setText("")
                    self.LineEdit_4.setText("")
                    self.show_record()
                    return
                except FileNotFoundError:
                    logger.error("用户名登录，无本地记录: " + traceback.format_exc())
                    self.show_norecord()
        elif (self.LineEdit_4.text() != ""):
            logger.debug("非法文件名。")
            self.show_valid() 
            return

        logger.info("获取官网寻访记录总页数")
        all_page = get_page(self.token)
        logger.debug("all_page: " + str(all_page))

        if all_page == -1:
            self.show_wrong()
        elif all_page == 0:
            self.show_empty()
        else:
            logger.info("获取官网寻访记录")
            get_record(self.token, all_page, self.username)
            self.LineEdit.setText("")
            self.LineEdit_4.setText("")
            self.show_correct()


    def show_correct(self):
        w = MessageBox("登录凭证提交成功","<br>请进入寻访统计页面查看结果。<br>", self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')
        self.signal_str.emit(self.username)

    
    def show_record(self):
        w = MessageBox("用户名登录成功","<br>请进入寻访统计页面查看结果。<br>", self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')
        # reply = QMessageBox.information(self,"用户名登录成功","<br>请进入寻访统计页面查看结果。<br>",QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        # print(reply)
        self.signal_str.emit(self.username)


    def show_norecord(self):
        w = MessageBox("用户名登录失败","<br>请进入更换用户名或输入寻访凭证。<br>", self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


    def show_wrong(self):
        w = MessageBox("登录凭证提交失败","<br>请重新查询并输入。<br>", self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


    def show_empty(self):
        w = MessageBox("暂无寻访记录","<br>该账号暂无可查询的寻访记录。<br>", self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')


    def show_valid(self):
        w = MessageBox("文件名非法","<br>请重新输入用户名。<br>", self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')



        