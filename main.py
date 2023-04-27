# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import psutil
import time
from PySide6.QtCharts import QChart, QLineSeries
from PySide6.QtWidgets import QFileDialog
import json
# from modules.function.test import Test

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class NewThread(QThread):
    # 自定义信号声明
    # 使用自定义信号和 UI 主线程通讯，参数是发送信号时附带参数的数据类型，可以是 str，int，list 等
    finishSignal = Signal(str)

    # 带一个参数 t
    def __init__(self, parent=None):
        super(NewThread, self).__init__(parent)

    # run 函数是子线程中的操作，线程启动后开始执行
    if os.path.exists(f"./computer_info.csv"):
        pass
    else:
        with open(r"./computer_info.csv", "w") as f:
            pass
    
    def run(self):
        timer = 0
        while True:
            timer += 1
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_info = cpu_percent
            virtual_memory = psutil.virtual_memory()
            memory_percent = virtual_memory.percent
            with open(r"./computer_info.csv", "a") as f:
                f.write(f"{timer},{cpu_info},{memory_percent}\n")
            time.sleep(1)
            # 发射自定义信号
            # 通过 emit 函数将参数 i 传递给主线程，触发自定义信号
            self.finishSignal.emit("1")

class ComicThread(QThread):
    def __init__(self, model, oropic_pic):
        super(ComicThread, self).__init__()
        self.model = model
        self.oropic_pic = oropic_pic
    
    def run(self):
        import sys
        sys.path.append(os.path.join(os.path.abspath('.'), 'AnimeGANv2'))
        from AnimeGANv2 import test
        # 是否要冻结路径
        checkpoint_dir = "./AnimeGANv2/checkpoint/" + self.model
        style_name = "./images/comic"
        # test_dir = "./images/oripic"
        sample_file = "./images/oripic/" + self.oropic_pic
        if_adjust_brightness = True
        test.test(checkpoint_dir, style_name, sample_file, if_adjust_brightness)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "自由"
        description = "基于人工智能的图片动漫化"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        # widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(lambda: self.close())
        # 新增功能：切换主题
        widgets.btn_message.clicked.connect(self.buttonClick)
        widgets.btn_share.clicked.connect(self.buttonClick)
        # 新增功能：查看论文
        widgets.btn_adjustments.clicked.connect(self.open_paper)
        widgets.btn_print.clicked.connect(self.open_paper)
        # 新增功能：查看项目
        widgets.btn_more.clicked.connect(self.open_github)
        widgets.btn_logout.clicked.connect(self.open_github)
        # 新增功能：选择模型
        self.model = "generator_Hayao_weight"
        widgets.checkBox_2.setChecked(True)
        widgets.checkBox_2.stateChanged.connect(self.on_checkbox_state_changed_2)
        widgets.checkBox_3.stateChanged.connect(self.on_checkbox_state_changed_3)
        widgets.checkBox_4.stateChanged.connect(self.on_checkbox_state_changed_4)
        # 新增功能：查看电脑信息
        widgets.btn_computer.clicked.connect(self.buttonClick)
        widgets.pushButton.clicked.connect(self.show_computer_info)
        # 测试功能：图片动漫化
        # widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_oripic.clicked.connect(self.reveal_pic)
        # start_transform【高配置】和 python_comic【低配置】
        widgets.btn_start.clicked.connect(self.start_transform) # self.python_comic
        widgets.btn_comic.clicked.connect(self.reveal_comic)
        

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        # 开始修改
        # 路径冻结，防止打包成 exe 后路径错乱
        if getattr(sys, 'frozen', False):
            absPath = os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath = os.path.dirname(os.path.abspath(__file__))
        useCustomTheme = True
        self.useCustomTheme = useCustomTheme
        self.absPath = absPath
        themeFile = os.path.abspath(os.path.join(absPath, "themes\py_dracula_light.qss"))
        # 结束修改

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # SHOW NEW PAGE
        if btnName == "btn_computer":
            widgets.stackedWidget.setCurrentWidget(widgets.computer_info) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        # if btnName == "btn_save":
        #     # print("Save BTN clicked!")
        #     QMessageBox.information(self, "提示", "该功能暂未实现", QMessageBox.Yes)
        
        # 切换主题
        if btnName == "btn_message" or btnName == "btn_share":
            if self.useCustomTheme:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_dark.qss"))
                # 跟着原先的代码走
                UIFunctions.theme(self, themeFile, True)
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = False
            else:
                themeFile = os.path.abspath(os.path.join(self.absPath, "themes\py_dracula_light.qss"))
                # 跟着原先的代码走
                UIFunctions.theme(self, themeFile, True)
                AppFunctions.setThemeHack(self)
                self.useCustomTheme = True
        
        # 图片动画化
        if btnName == "btn_save":
            widgets.stackedWidget.setCurrentWidget(widgets.comic)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def open_paper(self):
        import webbrowser
        webbrowser.open("https://tachibanayoshino.github.io/AnimeGANv2/")

    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/TachibanaYoshino/AnimeGANv2")
    
    def on_checkbox_state_changed_2(self):
        if widgets.checkBox_2.isChecked():
            widgets.checkBox_3.setChecked(False)
            widgets.checkBox_4.setChecked(False)
            self.model = "generator_Shinkai_weight"
    
    def on_checkbox_state_changed_3(self):
        if widgets.checkBox_3.isChecked():
            widgets.checkBox_2.setChecked(False)
            widgets.checkBox_4.setChecked(False)
            self.model = "generator_Hayao_weight"
    
    def on_checkbox_state_changed_4(self):
        if widgets.checkBox_4.isChecked():
            widgets.checkBox_2.setChecked(False)
            widgets.checkBox_3.setChecked(False)
            self.model = "generator_Paprika_weight"
    
    def show_computer_info(self):
        """
        获取电脑信息
        """
        with open('./info.json', 'r', encoding='utf-8') as f:
            # data 为数组或者字典形式
            data = json.load(f)
        widgets.label_9.setText("显卡信息：" + data["Card_Information"])
        widgets.label_8.setText("操作系统的名称及版本号：" + data["OS_Version"])
        widgets.label_10.setText("CUDA 版本：" + data["CUDA_Version"])
        widgets.label_11.setText("Python 版本：" + data["Python_Version"])
        widgets.label_18.setText("Pytorch 的版本：" + data["Pytorch_Version"])
        widgets.label_19.setText("Pytorch 是否可用 CUDA：" + data["Pytorch_CUDA"])
        widgets.label_20.setText("Tensorflow 的版本：" + data["Tensorflow_Version"])
        widgets.label_21.setText("Tensorflow 是否可用 CUDA：" + data["Tensorflow_CUDA"])
        widgets.label_12.setText("计算机的处理器架构：" + data["PC_Framework"])
        widgets.label_13.setText("计算机的处理器信息：" + data["PC_Information"])
        widgets.label_22.setText("CPU 的逻辑数量：" + data["CPU_logic"])
        widgets.label_23.setText("CPU 的物理核心数量：" + data["CPU_core"])
        widgets.label_24.setText("CPU 使用率：" + data["CPU_Use"])
        widgets.label_25.setText("内存使用情况：" + data["Memory"])

    def reveal_pic(self):
        """
        显示原始图片，图片的路径是 images/oropic，如果没有则显示没有图片
        """
        label_oripic = widgets.label_oripic
        # 打开文件框，并获取文件路径
        filePath, _ = QFileDialog.getOpenFileName(
            None,
            None,
            './images/oripic/', # 起始目录
            "图片类型 (*.png *.jpg *.bmp)" # 可选择文件类型
        )
        url = filePath
        self.oropic_pic = os.path.basename(url)
        # 如果没有则显示没有图片
        pix = QPixmap(url).scaled(label_oripic.size(), aspectMode=Qt.KeepAspectRatio)
        label_oripic.setPixmap(pix)
        label_oripic.repaint()
    
    def start_transform(self):
        """
        开始图片动漫化，转换后的图片的路径是 images/comic【适合高配置】
        """
        QMessageBox.information(self, "提示", "动漫化过程需要等待约半分钟", QMessageBox.Yes)
        self.comic_thread = ComicThread(self.model, self.oropic_pic)
        self.comic_thread.start()
        if self.comic_thread.isRunning():
            pass
            # self.comic_thread.terminate()
            # del self.comic_thread
        """
        显示动漫化图片，但期间不能进行其他操作，不建议使用【PASS】
        """
        # self.comic_thread.wait() # 等待线程跑完
        # label_comic = widgets.label_comic
        # url = "./images/comic/" + self.oropic_pic
        # pix = QPixmap(url).scaled(label_comic.size(), aspectMode=Qt.KeepAspectRatio)
        # label_comic.setPixmap(pix)
        # label_comic.repaint()
    
    def python_comic(self):
        """
        调用 python 文件，该文件再调用 AnimeGANv2 项目【适合低配置】
        """
        import os
        QMessageBox.information(self, "提示", "动漫化过程需要等待约半分钟", QMessageBox.Yes)
        checkpoint_dir = "./AnimeGANv2/checkpoint/" + self.model
        style_name = "./images/comic"
        sample_file = "./images/oripic/" + self.oropic_pic
        if_adjust_brightness = True
        sys_argv = f" {checkpoint_dir} {style_name} {sample_file} {if_adjust_brightness}"
        os.system("comic.bat" + sys_argv)


    def reveal_comic(self):
        """
        显示动漫化图片，图片的路径是 images/comic，如果没有则显示没有图片
        """
        import os
        label_comic = widgets.label_comic
        url = "./images/comic/" + self.oropic_pic
        if os.path.exists(url) == False:
            QMessageBox.information(self, "提示", "图片还在动漫化中，请耐心等待哦~", QMessageBox.Yes)
        else:
            pix = QPixmap(url).scaled(label_comic.size(), aspectMode=Qt.KeepAspectRatio)
            label_comic.setPixmap(pix)
            label_comic.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
