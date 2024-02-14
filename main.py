import sys
from utils import logger
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from qfluentwidgets import SplitFluentWindow, FluentIcon

from page_token import Page_token
from page_total import Page_total



class F(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('明日方舟抽卡记录') #PyQt-Fluent-Widget
        # self.setWindowIcon(QIcon(''))

        # 添加子页面
        self.Page_token = Page_token(self) 
        self.Page_total = Page_total(self)

        self.Page_token.signal_str.connect(self.Page_total.get_data_str)

        self.addSubInterface(self.Page_token, FluentIcon.RINGER, '登录凭证')
        self.addSubInterface(self.Page_total, FluentIcon.STOP_WATCH, '寻访统计')

        # 设置窗口大小
        desktop = QDesktopWidget().availableGeometry()
        self.resize(int(desktop.width() * 0.76), int(desktop.height() * 0.76))

        # 将窗口位置位于屏幕中心
        self.move(desktop.center() - self.rect().center())

    

if __name__ == "__main__":

    logger.info("生成GUI界面")

    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = F()
    w.show()
    app.exec_()


    

    








