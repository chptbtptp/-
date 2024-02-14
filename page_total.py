from PyQt5.QtWidgets import QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt
import json
from utils import logger
import traceback

from qfluentwidgets import FlowLayout
from PyQt5.QtCore import QEasingCurve

from Ui_total import Ui_Total

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        child.deleteLater()


class Page_total(QWidget, Ui_Total):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setupUi(self)

        self.username = "default"
        self.a = []
        self.s = set()

        self.layout1 = FlowLayout(self.BodyLabel_3, needAni=True)
        self.layout1.setAnimation(250, QEasingCurve.OutQuad)
        self.layout2 = FlowLayout(self.BodyLabel_4, needAni=True)
        self.layout2.setAnimation(250, QEasingCurve.OutQuad)
        self.layout3 = FlowLayout(self.BodyLabel_5, needAni=True)
        self.layout3.setAnimation(250, QEasingCurve.OutQuad)
        self.layout4 = FlowLayout(self.BodyLabel_6, needAni=True)
        self.layout4.setAnimation(250, QEasingCurve.OutQuad)
        self.layout5 = FlowLayout(self.BodyLabel_7, needAni=True)
        self.layout5.setAnimation(250, QEasingCurve.OutQuad)

        # 创建 Matplotlib 图表区域
        # self.figure, self.ax = plt.subplots(figsize=(12, 12))  # 设置图表大小为 12x6 英寸
        self.figure, self.ax = plt.subplots() 
        plt.axis('off')
        
        
        self.canvas = FigureCanvas(self.figure)
        self.horizontalLayout_2.addWidget(self.canvas)

        # 初始化时显示 空白
        self.show_default()

    def get_data_str(self, username):
        self.username = username
        self.show_pie_chart()
        self.show_table()
        print(self.username)


    def show_default(self):
        try :
            f = open(self.username + '_record_json.json', 'r', encoding='utf-8')
            self.show_pie_chart()
            self.show_table()
        except FileNotFoundError:
            logger.error("无本地记录: " + traceback.format_exc())
            return False
        

    def get_pool(self, i):
        pool_name = self.a[i]['pool']
        # pool_time = self.a[i]['ts']
        pool_num = 0
        # 所有卡池内的下标
        # char5_list = []
        # char6_list = []
        # 本卡池内的数量
        char5_list_pool = []
        char6_list_pool = []
        # 所有5星6星角色
        char_list = []
        char_num_list = []
        color_list = []
        j = i

        # while ((pool_time - self.a[j]['ts'] < 2160000) and (j <= len(self.a))):
        while (j < len(self.a)):
            # 在卡池持续时间内
            if (pool_name == self.a[j]['pool']): 
                # 当前寻访记录为目标卡池
                self.s.add(j)
                pool_num = pool_num + 1
                if (self.a[j]['rarity'] == 4):
                    # 5星角色
                    # char5_list.append(j)
                    char5_list_pool.append(pool_num)
                    char_list.append('5星:' + self.a[j]['name'])
                    char_num_list.append(pool_num)
                    color_list.append('''QPushButton{background:#FFFFFF;}''')
                elif (self.a[j]['rarity'] == 5):
                    # 6星角色
                    # char6_list.append(j)
                    char6_list_pool.append(pool_num)
                    char_list.append('6星:' + self.a[j]['name'])
                    char_num_list.append(pool_num)
                    color_list.append('''QPushButton{background:#FFCC00;}''')
            j = j + 1

        return (pool_num, pool_name, char5_list_pool, char6_list_pool, char_num_list, char_list, color_list)


    def show_pie_chart(self):
        f = open(self.username + '_record_json.json', 'r', encoding='utf-8')
        content = f.read()
        self.a = json.loads(content)
        self.s = set()

        data = [0, 0, 0, 0]
        for t in self.a:
            data[t['rarity'] - 2] = data[t['rarity'] - 2] + 1
        
        labels = ['3 star', '4 star', '5 star', '6 star']  # 示例标签
        explode = (0, 0, 0, 0.1)

        self.ax.cla()  # 清除当前子图
        plt.axis('off')
        self.ax = self.figure.add_subplot(111)  # 创建新的子图
        plt.axis('off')

        self.ax.pie(data, labels=labels, explode=explode, autopct='%1.1f%%', startangle=90)
        self.ax.axis('equal')  # 保证饼图是一个圆
        self.canvas.draw()

        self.CaptionLabel_4.setText( "寻访统计：共计 {}  抽".format(len(self.a)))

        self.BodyLabel.setText("6 星角色的寻访概率为： {:.2%}<br><br>5 星角色的寻访概率为： {:.2%}<br><br>4 星角色的寻访概率为： {:.2%}<br><br>3 星角色的寻访概率为： {:.2%}".format(data[3] / len(self.a), data[2] / len(self.a), data[1] / len(self.a), data[0] / len(self.a)))  #设置Html文本

        self.BodyLabel_2.setText("6 星角色的寻访数量为： {}<br><br>5 星角色的寻访数量为： {}<br><br>4 星角色的寻访数量为： {}<br><br>3 星角色的寻访数量为： {}".format(data[3], data[2], data[1], data[0]))


    def pool_clear(self):
        clearLayout(self.layout1)
        clearLayout(self.layout2)
        clearLayout(self.layout3)
        clearLayout(self.layout4)
        clearLayout(self.layout5)
        self.CaptionLabel.setText("")
        self.CaptionLabel_2.setText("")
        self.CaptionLabel_3.setText("")
        self.CaptionLabel_5.setText("")
        self.CaptionLabel_6.setText("")
        return
    

    def show_table(self):
        i = 0
        self.pool_clear()

        pool_num, pool_name, char5_list_pool, char6_list_pool, char_num_list, char_list, color_list = self.get_pool(i)

        # 卡池1统计结束，进行显示 
        if (len(char6_list_pool) == 0):
            char6 = pool_num
        else:
            char6 = char6_list_pool[0] - 1
        if (len(char5_list_pool) == 0):
            char5 = pool_num
        else:
            char5 = char5_list_pool[0] - 1
        self.CaptionLabel.setText(pool_name + "[共{}抽]<br>本卡池内已有 {} 抽未出6星角色<br>本卡池内已有 {} 抽未出5星角色".format(pool_num, char6, char5))

        for k in range(len(char_num_list)):
            content = char_list[k] + '[' + str(pool_num - char_num_list[k] + 1) + ']'
            t = QPushButton(content)
            t. setStyleSheet(color_list[k])
            self.layout1.addWidget(t)
                    
        
        # 判断是否需要进行下一个卡池的显示
        i = 0
        while (i in self.s):
            i = i + 1
        ti = i
        if ((i >= len(self.a)) or (i == -1)):
            return
        else:
            pool_num, pool_name, char5_list_pool, char6_list_pool, char_num_list, char_list, color_list = self.get_pool(i)

        # 卡池2统计结束，进行显示 
        if (len(char6_list_pool) == 0):
            char6 = pool_num
        else:
            char6 = char6_list_pool[0] - 1
        if (len(char5_list_pool) == 0):
            char5 = pool_num
        else:
            char5 = char5_list_pool[0] - 1
        self.CaptionLabel_2.setText(pool_name + "[共{}抽]<br>本卡池内已有 {} 抽未出6星角色<br>本卡池内已有 {} 抽未出5星角色".format(pool_num, char6, char5))

        for k in range(len(char_num_list)):
            content = char_list[k] + '[' + str(pool_num - char_num_list[k] + 1) + ']'
            t = QPushButton(content)
            t. setStyleSheet(color_list[k])
            self.layout2.addWidget(t)


        # 判断是否需要进行下一个卡池的显示
        i = ti
        while (i in self.s):
            i = i + 1
        ti = i
        if ((i >= len(self.a)) or (i == -1)):
            return
        else:
            pool_num, pool_name, char5_list_pool, char6_list_pool, char_num_list, char_list, color_list = self.get_pool(i)

        # 卡池3统计结束，进行显示 
        if (len(char6_list_pool) == 0):
            char6 = pool_num
        else:
            char6 = char6_list_pool[0] - 1
        if (len(char5_list_pool) == 0):
            char5 = pool_num
        else:
            char5 = char5_list_pool[0] - 1
        self.CaptionLabel_3.setText(pool_name + "[共{}抽]<br>本卡池内已有 {} 抽未出6星角色<br>本卡池内已有 {} 抽未出5星角色".format(pool_num, char6, char5))

        for k in range(len(char_num_list)):
            content = char_list[k] + '[' + str(pool_num - char_num_list[k] + 1) + ']'
            t = QPushButton(content)
            t. setStyleSheet(color_list[k])
            self.layout3.addWidget(t)


        # 判断是否需要进行下一个卡池的显示
        i = ti
        while (i in self.s):
            i = i + 1
        ti = i
        if ((i >= len(self.a)) or (i == -1)):
            return
        else:
            pool_num, pool_name, char5_list_pool, char6_list_pool, char_num_list, char_list, color_list = self.get_pool(i)

        # 卡池4统计结束，进行显示 
        if (len(char6_list_pool) == 0):
            char6 = pool_num
        else:
            char6 = char6_list_pool[0] - 1
        if (len(char5_list_pool) == 0):
            char5 = pool_num
        else:
            char5 = char5_list_pool[0] - 1
        self.CaptionLabel_5.setText(pool_name + "[共{}抽]<br>本卡池内已有 {} 抽未出6星角色<br>本卡池内已有 {} 抽未出5星角色".format(pool_num, char6, char5))

        for k in range(len(char_num_list)):
            content = char_list[k] + '[' + str(pool_num - char_num_list[k] + 1) + ']'
            t = QPushButton(content)
            t. setStyleSheet(color_list[k])
            self.layout4.addWidget(t)


        # 判断是否需要进行下一个卡池的显示
        i = ti
        while (i in self.s):
            i = i + 1
        ti = i
        if ((i >= len(self.a)) or (i == -1)):
            return
        else:
            pool_num, pool_name, char5_list_pool, char6_list_pool, char_num_list, char_list, color_list = self.get_pool(i)

        # 卡池5统计结束，进行显示 
        if (len(char6_list_pool) == 0):
            char6 = pool_num
        else:
            char6 = char6_list_pool[0] - 1
        if (len(char5_list_pool) == 0):
            char5 = pool_num
        else:
            char5 = char5_list_pool[0] - 1
        self.CaptionLabel_6.setText(pool_name + "[共{}抽]<br>本卡池内已有 {} 抽未出6星角色<br>本卡池内已有 {} 抽未出5星角色".format(pool_num, char6, char5))

        for k in range(len(char_num_list)):
            content = char_list[k] + '[' + str(pool_num - char_num_list[k] + 1) + ']'
            t = QPushButton(content)
            t. setStyleSheet(color_list[k])
            self.layout5.addWidget(t)


        return
    
    

            

        



        
        




