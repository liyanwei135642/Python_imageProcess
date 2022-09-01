import os
from PySide2.QtCore import QSize
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
from datetime import datetime
import cv2 as cv
import matplotlib.pyplot as plt
import time
import sys
import shutil
import cv2 as cv

def video():
    avi = cv.VideoCapture("123.avi")
    while avi.isOpened():
        open, I = avi.read()
        if not open:
            break
        if I is None:
            break
        I = cv.resize(I, (600, 400))
        cv.imshow("", I)
        cv.moveWindow("", 350, 150)
        if (cv.waitKey(300)) == 27:
            break
    cv.destroyAllWindows()

class mytree(QTreeWidget):
    def __init__(self,parent):
        super().__init__(parent)
    def mouseDoubleClickEvent(self, event:QMouseEvent) -> None:
        usr_win.menu1_show()

class NewWindow:
    def __init__(self):
        # 下载ui窗体
        self.window = QUiLoader().load("new_win.ui")
        self.window.lineEdit_2.setText(os.getcwd())
        name = str(datetime.now())
        name = name.replace("-", "")
        name = name.replace(":", "")
        name = name.replace(" ", "")
        name=name.split('.')[0]
        self.window.lineEdit.setText("Project-" + name)
        # 注册单击信号
        self.window.pushButton.clicked.connect(self.pb)

        self.window.pushButton_2.clicked.connect(self.pb_2)

        self.window.lineEdit.returnPressed.connect(self.le_rp)

        self.window.lineEdit_2.returnPressed.connect(self.pb_2)

    def pb(self):
        dirname=QFileDialog.getExistingDirectory(self.window, "选择项目路径","c:\\")
        self.window.lineEdit_2.setText(dirname)

    def pb_2(self):
        proname=self.window.lineEdit.text()
        if len(proname)==0:
            QMessageBox.about(None,"错误提示","项目名称不能为空！\n\t请重新输入：")
            self.window.lineEdit.setFoucs()
            return
        if proname in pro_mes:
            QMessageBox.about(None,"错误提示","项目名称已经存在！\n\t请重新输入：")
            self.window.lineEdit.clear()
            self.window.lineEdit.setFoucs()
            return
        prodir=self.window.lineEdit_2.text()
        if not os.path.exists(prodir):
            QMessageBox.about(None, "错误提示", "项目位置不存在！\n\t请重新输入：")
            self.window.lineEdit_2.clear()
            self.window.lineEdit_2.setFoucs()
            return
        if os.path.exists(prodir+"\\"+proname):
            QMessageBox.about(None, "错误提示", "项目名称冲突！\n\t请重新输入：")
            self.window.lineEdit.clear()
            self.window.lineEdit.setFoucs()
            return
        pro_mes[proname]=prodir
        self.newpro(proname,prodir)
        usr_win.window.tableWidget.clearContents()
        usr_win.window.tableWidget_2.clearContents()
        usr_win.window.label_6.setText("  当前项目："+proname)
        name=str(datetime.now())
        name=name.replace("-","")
        name = name.replace(":", "")
        name = name.replace(" ", "")
        name = name.split('.')[0]
        self.window.lineEdit.setText("Project-"+name)
        self.window.close()

    def le_rp(self):
        if len(self.window.lineEdit_2.text())==0:
            self.window.lineEdit_2.setFocus()
            return
        self.pb_2()

    def newpro(self,proname,prodir):
        item1 = QTreeWidgetItem(usr_win.window.treeWidget)
        usr_win.window.treeWidget.setCurrentItem(item1)
        usr_win.cur_item=item1
        item1.setText(0, proname)
        item1.setIcon(0, QIcon("dir.png"))
        item1_1 = QTreeWidgetItem(item1)
        item1_1.setText(0, "image")
        item1_1.setIcon(0, QIcon("dir.png"))
        item1_2 = QTreeWidgetItem(item1)
        item1_2.setText(0, "file")
        item1_2.setIcon(0, QIcon("dir.png"))
        item1_1_1 = QTreeWidgetItem(item1_1)
        item1_1_1.setText(0, "left")
        item1_1_1.setIcon(0, QIcon("dir.png"))
        item1_1_2 = QTreeWidgetItem(item1_1)
        item1_1_2.setText(0, "middle")
        item1_1_2.setIcon(0, QIcon("dir.png"))
        item1_1_3 = QTreeWidgetItem(item1_1)
        item1_1_3.setText(0, "right")
        item1_1_3.setIcon(0, QIcon("dir.png"))
        item1_1_4 = QTreeWidgetItem(item1_1)
        item1_1_4.setText(0, "result")
        item1_1_4.setIcon(0, QIcon("dir.png"))
        item1_2_1 = QTreeWidgetItem(item1_2)
        item1_2_1.setText(0, "source")
        item1_2_1.setIcon(0, QIcon("dir.png"))
        item1_2_2 = QTreeWidgetItem(item1_2)
        item1_2_2.setText(0, "result")
        item1_2_2.setIcon(0, QIcon("dir.png"))
        os.makedirs(prodir+"\\"+proname+"\\image\\left")
        os.makedirs(prodir + "\\" + proname + "\\image\\middle")
        os.makedirs(prodir + "\\" + proname + "\\image\\right")
        os.makedirs(prodir + "\\" + proname + "\\image\\result")
        os.makedirs(prodir + "\\" + proname + "\\file\\source")
        os.makedirs(prodir + "\\" + proname + "\\file\\result")

class mytable(QTableWidget):
    def __init__(self,parent):
        super().__init__(parent)

    def resizeEvent(self, event:QResizeEvent) -> None:
        cols=self.columnCount()
        width=self.width()
        rows=self.rowCount()
        for k in range(cols):
            self.setColumnWidth(k,width//cols)
        for i in range(rows):
            self.setRowHeight(i,width*2//(cols*3))


    def mouseDoubleClickEvent(self, event:QMouseEvent) -> None:
        n=self.currentRow()
        if not usr_win.cur_item:
            return
        name=usr_win.cur_item.text(0)
        dir=pro_mes[name]+"\\"+name+"\\image\\result\\"
        images=os.listdir(dir)
        image=images[n]
        dir=dir+image
        print(dir)
        I=plt.imread(dir)
        plt.imshow(I)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.title(image)
        plt.show()





class UserWindow:
    def __init__(self):
        #下载ui窗体
        #Qtdesigner 注册自定义类 提升方法
        loader=QUiLoader()
        loader.registerCustomWidget(mytree)
        loader.registerCustomWidget(mytable)
        self.window = loader.load("usr_win.ui")
        #注册单击信号
        self.set_signal()
        #设置表格宽度自适应
        self.window.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.window.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.window.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #设置某个控件不可见
        #self.window.tableWidget_2.setVisible(False)
        self.set_table2_visible(False)
        #设置表格垂直头标题不可见
        #self.window.tableWidget.verticalHeader().setVisible(False)
        #设置不允许编辑
        self.window.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #设置单击选中一行
        #self.window.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.right_menu()
        self.ss=self.window.treeWidget.styleSheet()
        self.cur_item=None
        #self.show=False


    def right_menu_table2(self):
        self.window.tableWidget_2.customContextMenuRequested.connect(self.menu1_clicked)
        self.menu1 = QMenu(self.window.treeWidget)
        self.action1_1 = self.menu1.addAction("Delete")
        self.action1_1.triggered.connect(self.menu1_del)
        self.action1_2 = self.menu1.addAction("Remove")
        self.action1_2.triggered.connect(self.menu1_rem)
        self.menu1_3 = self.menu1.addMenu("Color")
        self.action1_3_1 = self.menu1_3.addAction("Red")
        self.action1_3_1.triggered.connect(self.menu1_red)
        self.action1_3_2 = self.menu1_3.addAction("Blue")
        self.action1_3_2.triggered.connect(self.menu1_blu)
        self.action1_3_3 = self.menu1_3.addAction("Green")
        self.action1_3_3.triggered.connect(self.menu1_gre)
        self.action1_3_4 = self.menu1_3.addAction("White")
        self.action1_3_4.triggered.connect(self.menu1_whi)
        self.action1_3_5 = self.menu1_3.addAction("Black")
        self.action1_3_5.triggered.connect(self.menu1_bla)
        self.menu1_4 = self.menu1.addMenu("BlackgroundColor")
        self.action1_4_1 = self.menu1_4.addAction("Red")
        self.action1_4_1.triggered.connect(self.menu1_bred)
        self.action1_4_2 = self.menu1_4.addAction("Blue")
        self.action1_4_2.triggered.connect(self.menu1_bblu)
        self.action1_4_3 = self.menu1_4.addAction("Green")
        self.action1_4_3.triggered.connect(self.menu1_bgre)
        self.action1_4_4 = self.menu1_4.addAction("White")
        self.action1_4_4.triggered.connect(self.menu1_bwhi)
        self.action1_4_5 = self.menu1_4.addAction("Black")
        self.action1_4_5.triggered.connect(self.menu1_bbla)
        self.menu1_5 = self.menu1.addMenu("Font")
        self.action1_5_1 = self.menu1_5.addAction("9")
        self.action1_5_1.triggered.connect(self.menu1_f5)
        self.action1_5_2 = self.menu1_5.addAction("13")
        self.action1_5_2.triggered.connect(self.menu1_f7)
        self.action1_5_3 = self.menu1_5.addAction("17")
        self.action1_5_3.triggered.connect(self.menu1_f9)
        self.action1_5_4 = self.menu1_5.addAction("21")
        self.action1_5_4.triggered.connect(self.menu1_f11)
        self.action1_5_5 = self.menu1_5.addAction("25")
        self.action1_5_5.triggered.connect(self.menu1_f13)
        self.action1_6= self.menu1.addAction("Default")
        self.action1_6.triggered.connect(self.menu1_df)
        self.action1_7 = self.menu1.addAction("update")
        self.action1_7.triggered.connect(self.up_image)

    def right_menu(self):
        self.window.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.window.treeWidget.customContextMenuRequested.connect(self.menu1_clicked)
        self.menu1 = QMenu(self.window.treeWidget)
        self.action1_1 = self.menu1.addAction("Delete")
        self.action1_1.triggered.connect(self.menu1_del)
        self.action1_2 = self.menu1.addAction("Remove")
        self.action1_2.triggered.connect(self.menu1_rem)
        self.menu1_3 = self.menu1.addMenu("Color")
        self.action1_3_1 = self.menu1_3.addAction("Red")
        self.action1_3_1.triggered.connect(self.menu1_red)
        self.action1_3_2 = self.menu1_3.addAction("Blue")
        self.action1_3_2.triggered.connect(self.menu1_blu)
        self.action1_3_3 = self.menu1_3.addAction("Green")
        self.action1_3_3.triggered.connect(self.menu1_gre)
        self.action1_3_4 = self.menu1_3.addAction("White")
        self.action1_3_4.triggered.connect(self.menu1_whi)
        self.action1_3_5 = self.menu1_3.addAction("Black")
        self.action1_3_5.triggered.connect(self.menu1_bla)
        self.menu1_4 = self.menu1.addMenu("BlackgroundColor")
        self.action1_4_1 = self.menu1_4.addAction("Red")
        self.action1_4_1.triggered.connect(self.menu1_bred)
        self.action1_4_2 = self.menu1_4.addAction("Blue")
        self.action1_4_2.triggered.connect(self.menu1_bblu)
        self.action1_4_3 = self.menu1_4.addAction("Green")
        self.action1_4_3.triggered.connect(self.menu1_bgre)
        self.action1_4_4 = self.menu1_4.addAction("White")
        self.action1_4_4.triggered.connect(self.menu1_bwhi)
        self.action1_4_5 = self.menu1_4.addAction("Black")
        self.action1_4_5.triggered.connect(self.menu1_bbla)
        self.menu1_5 = self.menu1.addMenu("Font")
        self.action1_5_1 = self.menu1_5.addAction("9")
        self.action1_5_1.triggered.connect(self.menu1_f5)
        self.action1_5_2 = self.menu1_5.addAction("13")
        self.action1_5_2.triggered.connect(self.menu1_f7)
        self.action1_5_3 = self.menu1_5.addAction("17")
        self.action1_5_3.triggered.connect(self.menu1_f9)
        self.action1_5_4 = self.menu1_5.addAction("21")
        self.action1_5_4.triggered.connect(self.menu1_f11)
        self.action1_5_5 = self.menu1_5.addAction("25")
        self.action1_5_5.triggered.connect(self.menu1_f13)
        self.action1_6= self.menu1.addAction("Default")
        self.action1_6.triggered.connect(self.menu1_df)
        self.action1_7 = self.menu1.addAction("update")
        self.action1_7.triggered.connect(self.up_image)

    def menu1_rem(self):
        item = self.window.treeWidget.currentItem()
        if not item:
            item = self.cur_item
            if not item:
                return
        while item.parent():
            item = item.parent()
        pr = self.window.treeWidget.invisibleRootItem()
        if self.cur_item==item:
            self.window.tableWidget.clearContents()
            self.window.tableWidget_2.clearContents()
            self.cur_item=None
            self.window.label_6.setText("  项目名称：")
        pro_mes.pop(item.text(0))
        pr.removeChild(item)


    def menu1_del(self):
        rf = self.window.treeWidget.invisibleRootItem()
        for item in self.window.treeWidget.selectedItems():
            itemcp=item
            dir=item.text(0)
            while item.parent():
                name=item.parent().text(0)
                dir=name+"\\"+dir
                item=item.parent()
            dir=pro_mes[item.text(0)]+"\\"+dir
            if os.path.isfile(dir):
                os.remove(dir)
            elif os.path.basename(dir)==item.text(0):
                shutil.rmtree(dir)
            pr = itemcp.parent()
            if pr:
                pr.removeChild(itemcp)
            else:
                rf.removeChild(itemcp)
                pro_mes.pop(itemcp.text(0))
        if not self.cur_item:
            return
        name=self.cur_item.text(0)
        if name not in pro_mes:
            self.window.tableWidget.clearContents()
            self.window.tableWidget_2.clearContents()
            self.cur_item=None
            self.window.label_6.setText("  项目名称：")
            return
        dir=pro_mes[name]+"\\"+name
        self.load(dir)

    def menu1_clicked(self):
        self.menu1.move(QCursor().pos())
        self.menu1.show()

    def menu1_show(self):
        item=self.window.treeWidget.currentItem()
        if not item:
            item=self.cur_item
            if not item:
                return
        while item.parent():
            item=item.parent()
        name=item.text(0)
        pr = self.window.treeWidget.invisibleRootItem()
        index = pr.indexOfChild(item)
        pr.removeChild(item)
        self.create_task(name, pro_mes[name] + "\\" + name, index)
        dir=pro_mes[name]+"\\"+name
        self.window.label_6.setText("  当前项目："+name)
        self.load(dir)
        self.window.treeWidget.expandAll()

    def menu1_df(self):
        self.window.treeWidget.setStyleSheet(self.ss)

    def menu1_red(self):
        ss=self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss+"\ncolor:rgb(255,0,0);")

    def menu1_bla(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss+"\ncolor:rgb(0,0,0);")

    def menu1_blu(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\ncolor:rgb(0,0,255);")

    def menu1_gre(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\ncolor:rgb(0,255,0);")

    def menu1_whi(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\ncolor:rgb(255,255,255);")

    def menu1_bred(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss+"\nbackground-color:rgb(255,0,0);")

    def menu1_bbla(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nbackground-color:rgb(0,0,0);")

    def menu1_bblu(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nbackground-color:rgb(0,0,255);")

    def menu1_bgre(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nbackground-color:rgb(0,255,0);")

    def menu1_bwhi(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nbackground-color:rgb(255,255,255);")


    def menu1_f5(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss+"\nfont-size:9px;")

    def menu1_f7(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nfont-size:13px;")

    def menu1_f9(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nfont-size:17px;")

    def menu1_f11(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nfont-size:21px;")

    def menu1_f13(self):
        ss = self.window.treeWidget.styleSheet()
        self.window.treeWidget.setStyleSheet(ss + "\nfont-size:25px;")

    def tb(self):
        new_win.window.show()

    def tb_2(self):
        dir=QFileDialog.getExistingDirectory(self.window, "选择项目", "c:\\")
        if len(dir)<5:
            return
        prodir=os.path.dirname(dir)
        proname=os.path.basename(dir)
        if proname in pro_mes:
            QMessageBox.about(None, "错误提示", "您要打开的项目已经在任务列表中存在了！\n\t请修改项目名称继续：")
            return
        if not(os.path.exists(dir+"\\"+"image"+"\\"+"middle") and os.path.exists(dir+"\\"+"image"+"\\"+"result") and os.path.exists(dir+"\\"+"file"+"\\"+"source") and os.path.exists(dir+"\\"+"file"+"\\"+"source")):
            QMessageBox.about(None, "错误提示", "您要打开的目录不是标准项目！\n\t请修改项目名称继续：")
            return
        pro_mes[proname]=prodir
        self.create_task(proname,dir)
        self.load(dir)

    def create_task(self,proname,dir,index:int=0):
        self.window.label_6.setText("  当前项目："+proname)
        item1 = QTreeWidgetItem()
        self.window.treeWidget.invisibleRootItem().insertChild(index,item1)
        item1.setText(0, proname)
        self.window.treeWidget.setCurrentItem(item1)
        self.cur_item=item1
        item1.setIcon(0, QIcon("dir.png"))
        item1_1 = QTreeWidgetItem(item1)
        item1_1.setText(0, "image")
        item1_1.setIcon(0, QIcon("dir.png"))
        item1_2 = QTreeWidgetItem(item1)
        item1_2.setText(0, "file")
        item1_2.setIcon(0, QIcon("dir.png"))
        item1_1_1 = QTreeWidgetItem(item1_1)
        item1_1_1.setText(0, "left")
        item1_1_1.setIcon(0, QIcon("dir.png"))
        item1_1_2 = QTreeWidgetItem(item1_1)
        item1_1_2.setText(0, "middle")
        item1_1_2.setIcon(0, QIcon("dir.png"))
        item1_1_3 = QTreeWidgetItem(item1_1)
        item1_1_3.setText(0, "right")
        item1_1_3.setIcon(0, QIcon("dir.png"))
        item1_1_4 = QTreeWidgetItem(item1_1)
        item1_1_4.setText(0, "result")
        item1_1_4.setIcon(0, QIcon("dir.png"))
        item1_2_1 = QTreeWidgetItem(item1_2)
        item1_2_1.setText(0, "source")
        item1_2_1.setIcon(0, QIcon("dir.png"))
        item1_2_2 = QTreeWidgetItem(item1_2)
        item1_2_2.setText(0, "result")
        item1_2_2.setIcon(0, QIcon("dir.png"))
        prodir=[]
        items=[item1_1_1,item1_1_2,item1_1_3,item1_1_4,item1_2_1,item1_2_2]
        prodir.append(dir+"\\image\\left")
        prodir.append(dir + "\\image\\middle")
        prodir.append(dir + "\\image\\right")
        prodir.append(dir + "\\image\\result")
        prodir.append(dir + "\\file\\source")
        prodir.append(dir + "\\file\\result")
        for i in range(6):
            for j in os.listdir(prodir[i]):
                item=QTreeWidgetItem(items[i])
                item.setText(0,j)
                if i<4:
                    item.setIcon(0,QIcon("img_file.png"))
                else:
                    item.setIcon(0,QIcon("word_file.png"))

    def load_image(self,dir,des:QTableWidget,column:int=0):
        images=os.listdir(dir)
        n=len(images)
        rows=des.rowCount()
        #cols=des.columnCount()
        #width=des.width()
        #height=width*2//(cols*3)
        if n>rows:
            des.setRowCount(n)
        # for i in range(rows):
        #     des.setRowHeight(i,height)
        for k in range(n):
            label = QLabel()
            label.setPixmap(dir + "\\" + images[k])
            label.setScaledContents(True)
            label.setMargin(4)
            label.setStyleSheet("background-color:rgb(255,255,255)")
            des.setCellWidget(k, column, label)

    def resize(self,des:QTableWidget):
        cols = des.columnCount()
        width=des.width()
        rows=des.rowCount()
        for k in range(cols):
            des.setColumnWidth(k,(width)//(cols))
        for i in range(rows):
            des.setRowHeight(i,(width)*2//(3*(cols)))

    def load(self,dir):
        self.window.tableWidget.clearContents()
        self.window.tableWidget_2.clearContents()
        self.window.tableWidget.setRowCount(4)
        self.load_image(dir + "\\image\\left", self.window.tableWidget, 0)
        self.load_image(dir + "\\image\\middle", self.window.tableWidget, 1)
        self.load_image(dir + "\\image\\right", self.window.tableWidget, 2)
        self.load_image(dir + "\\image\\result", self.window.tableWidget_2,0)
        self.resize(self.window.tableWidget)
        self.resize(self.window.tableWidget_2)

    def tb_3(self):
        print("")

    def tb_4(self):
        self.set_table2_visible(True)
        self.set_table_visible(True)
        item = self.window.treeWidget.currentItem()
        if not item:
            if self.window.treeWidget.invisibleRootItem().childCount() == 0:
                QMessageBox.information(None, "提示信息", "任务列表目前没有项目！")
                return
            if self.cur_item:
                item = self.cur_item
            else:
                item = self.window.treeWidget.invisibleRootItem().child(0)
        while item.parent():
            item = item.parent()
        name = item.text(0)
        dir = pro_mes[name] + "\\" + name+"\\image"
        images = os.listdir("tmp")
        for image in images:
            shutil.copyfile("tmp\\" + image, dir + "\\result\\" + image)
        shutil.copyfile("裂缝参数计算结果.txt", pro_mes[name] + "\\" + name + "\\file\\result\\" + "裂缝参数计算结果.txt")
        pr = self.window.treeWidget.invisibleRootItem()
        index = pr.indexOfChild(item)
        pr.removeChild(item)
        self.create_task(name, pro_mes[name] + "\\" + name, index)
        self.load(pro_mes[name] + "\\" + name)
        video();

    def tb_5(self):
        print("")

    def tb_6(self):
        print("")

    def tb_7(self):
        print("")

    def up_image(self):
        if not self.cur_item:
            return
        name=self.cur_item.text(0)
        pr=self.window.treeWidget.invisibleRootItem()
        index=pr.indexOfChild(self.cur_item)
        pr.removeChild(self.cur_item)
        self.create_task(name,pro_mes[name]+"\\"+name,index)
        dir=pro_mes[name]+"\\"+name
        self.window.label_6.setText("  当前项目："+name)
        self.load(dir)

    def pb(self):
        self.set_table4_visible(False)
        self.set_table2_visible(False)
        self.set_table_visible(False)
        self.set_tree_visible(True)
        self.window.verticalLayout.setStretch(0, 1)
        self.window.verticalLayout.setStretch(1, 10)
        item = self.window.treeWidget.currentItem()
        if not item:
            if self.window.treeWidget.invisibleRootItem().childCount() == 0:
                QMessageBox.information(None, "提示信息", "任务列表目前没有项目！")
                return
            if self.cur_item:
                item = self.cur_item
            else:
                item = self.window.treeWidget.invisibleRootItem().child(0)
        while item.parent():
            item = item.parent()
        name = item.text(0)
        dir = pro_mes[name] + "\\" + name + "\\file\\result\\"
        files=os.listdir((dir))
        self.window.plainTextEdit.clear()
        for file in files:
            f=open(dir+file,"r")
            str=f.read()
            str=self.window.plainTextEdit.toPlainText()+"\n\n\n\r"+str
            self.window.plainTextEdit.setPlainText(str)


    def pb_2(self):
        print("")

    def pb_3(self):
        print("")

    def pb_4(self):
        item = self.window.treeWidget.currentItem()
        if not item:
            if self.window.treeWidget.invisibleRootItem().childCount() == 0:
                QMessageBox.information(None, "提示信息", "任务列表目前没有项目！")
                return
            if self.cur_item:
                item = self.cur_item
            else:
                item = self.window.treeWidget.invisibleRootItem().child(0)
        while item.parent():
            item = item.parent()
        name = item.text(0)
        dir = pro_mes[name] + "\\" + name + "\\image"
        self.set_table2_visible(True)
        shutil.copyfile("拼接结果.png",dir+"\\result\\拼接结果.png")
        pr = self.window.treeWidget.invisibleRootItem()
        index = pr.indexOfChild(item)
        pr.removeChild(item)
        self.create_task(name, pro_mes[name] + "\\" + name, index)
        self.load(pro_mes[name] + "\\" + name)

    def pb_5(self):
        self.set_table2_visible(False)
        self.set_table_visible(True)
        item=self.window.treeWidget.currentItem()
        if not item:
            if self.window.treeWidget.invisibleRootItem().childCount()==0:
                QMessageBox.information(None,"提示信息","任务列表目前没有项目！")
                return
            if self.cur_item:
                item=self.cur_item
            else:
                item=self.window.treeWidget.invisibleRootItem().child(0)
        while item.parent():
            item=item.parent()
        name=item.text(0)
        dir=pro_mes[name]+"\\"+name+"\\image"
        images = QFileDialog.getOpenFileNames(self.window, "请选择需要加载的图片文件", os.getcwd(), "图片文件(*.jpg *.png *.bmp)")
        m = len(images[0])
        n=0
        for image in images[0]:
            if n%3==0:
                shutil.copyfile(image, dir + "\\left\\" + os.path.basename(image))
            elif n%3==1:
                shutil.copyfile(image, dir + "\\middle\\" + os.path.basename(image))
            elif n%3==2:
                shutil.copyfile(image, dir + "\\right\\" + os.path.basename(image))
            n=n+1
        pr = self.window.treeWidget.invisibleRootItem()
        index=pr.indexOfChild(item)
        pr.removeChild(item)
        self.create_task(name,pro_mes[name]+"\\"+name,index)
        self.load(pro_mes[name]+"\\"+name)

    def pb_6(self):
        text=self.window.pushButton_6.text()
        if text[0]=='<':
            self.window.horizontalLayout_3.setStretch(0, 1)
            self.window.horizontalLayout_3.setStretch(1, 2)
            self.window.pushButton_6.setText("->|||<-")
            self.window.treeWidget.expandAll()
        else:
            self.window.horizontalLayout_3.setStretch(0, 1)
            self.window.horizontalLayout_3.setStretch(1, 5)
            self.window.pushButton_6.setText("<-|||->")
            self.window.treeWidget.collapseAll()


    def pb_7(self):
        text = self.window.pushButton_7.text()
        if text[0] == '<':
            self.window.pushButton_7.setText("->|||<-")
            self.set_table2_visible(False)
            self.set_dock_visible(False)
            self.set_tree_visible(False)
            self.set_table4_visible(False)
        else:
            self.window.pushButton_7.setText("<-|||->")
            self.set_table2_visible(True)
            self.set_dock_visible(True)
            self.set_tree_visible(True)
            self.set_table4_visible(True)

    def pb_8(self):
        self.set_table_visible(True)
        self.set_table2_visible(True)
        self.set_table4_visible(True)
        self.set_tree_visible(True)
        self.set_dock_visible(True)
        self.window.verticalLayout.setStretch(0, 6)
        self.window.verticalLayout.setStretch(1, 1)

    def pb_9(self):
        self.window.pushButton_7.setText("<-|||->")
        self.set_table_visible(False)
        self.set_table2_visible(True)
        self.set_dock_visible(True)
        self.set_tree_visible(True)
        self.set_table4_visible(True)

    def pb_10(self):
        text = self.window.pushButton_10.text()
        if text[0] == '<':
            self.window.pushButton_10.setText("->|||<-")
            self.set_table_visible(False)
            self.set_dock_visible(False)
            self.set_tree_visible(False)
            self.set_table4_visible(False)
        else:
            self.window.pushButton_10.setText("<-|||->")
            self.set_table_visible(True)
            self.set_dock_visible(True)
            self.set_tree_visible(True)
            self.set_table4_visible(True)

    def pb_12(self):
        self.window.pushButton_10.setText("<-|||->")
        self.set_table2_visible(False)
        self.set_table_visible(True)
        self.set_dock_visible(True)
        self.set_tree_visible(True)
        self.set_table4_visible(True)

    def pb_13(self):
        self.window.frame_2.setVisible(False)

    def pb_14(self):
        text = self.window.pushButton_14.text()
        if text[0] == '<':
            self.window.horizontalLayout_4.setStretch(0, 2)
            self.window.horizontalLayout_4.setStretch(1, 1)
            self.window.pushButton_14.setText("->|||<-")
        else:
            self.window.horizontalLayout_4.setStretch(0, 5)
            self.window.horizontalLayout_4.setStretch(1, 1)
            self.window.pushButton_14.setText("<-|||->")

    def pb_15(self):
        self.set_table4_visible(False)

    def set_table_visible(self,visible:bool):

        self.window.tableWidget.setVisible(visible)
        self.window.widget_4.setVisible(visible)

    def set_table2_visible(self,visible:bool):
        self.window.tableWidget_2.setVisible(visible)
        self.window.widget_5.setVisible(visible)

    def set_table4_visible(self,visible:bool):
        self.window.widget_3.setVisible(visible)

    def set_tree_visible(self,visible:bool):
        self.window.frame_2.setVisible(visible)

    def set_dock_visible(self,visible:bool):
        self.window.dockWidget.setVisible(visible)

    def tree_clicked(self):
        item=usr_win.window.treeWidget.currentItem();
        if not item:
            return
        pitem=item.parent()
        if not pitem:
            return
        ppr=pitem.parent()
        if not ppr:
            return
        if ppr.text(0)!="image":
            return
        n = pitem.indexOfChild(item)
        if pitem.text(0)=="result":
            usr_win.set_table2_visible(True)
            usr_win.set_table_visible(False)
            usr_win.window.tableWidget_2.verticalScrollBar().setSliderPosition(n)
        else:
            usr_win.set_table_visible(True)
            usr_win.set_table2_visible(False)
            usr_win.window.tableWidget.verticalScrollBar().setSliderPosition(n)




    def set_signal(self):
        self.window.treeWidget.clicked.connect(self.tree_clicked)
        self.window.toolButton.clicked.connect(self.tb)
        self.window.toolButton_2.clicked.connect(self.tb_2)
        self.window.toolButton_3.clicked.connect(self.tb_3)
        self.window.toolButton_4.clicked.connect(self.tb_4)
        self.window.toolButton_5.clicked.connect(self.tb_5)
        self.window.toolButton_6.clicked.connect(self.tb_6)
        self.window.toolButton_7.clicked.connect(self.tb_7)
        self.window.pushButton.clicked.connect(self.pb)
        self.window.pushButton_2.clicked.connect(self.pb_2)
        self.window.pushButton_3.clicked.connect(self.pb_3)
        self.window.pushButton_4.clicked.connect(self.pb_4)
        self.window.pushButton_5.clicked.connect(self.pb_5)
        self.window.pushButton_6.clicked.connect(self.pb_6)
        self.window.pushButton_7.clicked.connect(self.pb_7)
        self.window.pushButton_8.clicked.connect(self.pb_8)
        self.window.pushButton_9.clicked.connect(self.pb_9)
        self.window.pushButton_10.clicked.connect(self.pb_10)
        self.window.pushButton_12.clicked.connect(self.pb_12)
        self.window.pushButton_13.clicked.connect(self.pb_13)
        self.window.pushButton_14.clicked.connect(self.pb_14)
        self.window.pushButton_15.clicked.connect(self.pb_15)


currentdir = os.path.dirname(sys.argv[0])
libdir = os.path.join(currentdir, "lib")
sys.path.append(libdir)
os.environ['path'] += ';./lib'
pro_mes={}
app=QApplication([])
new_win =NewWindow()
usr_win=UserWindow()
usr_win.window.show()
app.exec_()
