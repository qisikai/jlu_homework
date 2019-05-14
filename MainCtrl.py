#encoding=utf-8
import sys
import os
import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QPushButton,QTabWidget,QWidget,QHBoxLayout,QMessageBox,QListWidgetItem,QListWidget
from MainWindow import Ui_MainWindow

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl,QThread,QTimer,pyqtSignal,QCoreApplication,QDate,QTime
import time
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEngineSettings,QWebEngineProfile
from PyQt5.QtGui import QIcon,QStandardItemModel,QStandardItem,QBrush,QColor
import json
import random
import math

import utils

class Cal_thread(QThread):
    #实例化一个信号对象
    trigger_info = pyqtSignal(str)
    trigger_status = pyqtSignal(str)

    def __init__(self,classes,students,time_table,date_obj,rooms,room_id):
        super(Cal_thread, self).__init__()
        self.classes = classes
        self.students=students
        self.time_table=time_table
        self.date_obj=date_obj
        self.rooms=rooms
        self.room_id=room_id

    def run(self):
        try:
            #self.trigger_status.emit("started")
            #self.date_obj = datetime.datetime.now()
            self.date_start_obj = datetime.datetime(2018,9,3)
            #星期 ，周一是 0 --》 周一是 1
            dayOfWeek = self.date_obj.weekday() + 1
            week_ind = 1
            while self.date_start_obj  < self.date_obj:
                if self.date_start_obj.weekday() == 0:
                    week_ind+=1
                self.date_start_obj += datetime.timedelta(days=1)
            self.trigger_status.emit("info:第%d周,阅览室_%s" % (week_ind,self.room_id))
            students = self.rooms[self.room_id]
            for student in students:
                if len(student["name"]) == 0:
                    student['status'] = "未分配"
                    continue
                student['status'] = "占用中"
                cls = student['class']
                if cls in self.classes:
                    for course_name in self.classes[cls]:
                        for course in self.classes[cls][course_name]:
                            if week_ind in course['weeks'] and dayOfWeek == course['week_day']:
                                course_ind = str(course['course_ind'] * 2)
                                start_h = self.time_table[course_ind]['start_h']
                                start_m = self.time_table[course_ind]['start_m']
                                end_h = self.time_table[course_ind]['end_h']
                                end_m = self.time_table[course_ind]['end_m']
                                start_tm_obj = datetime.datetime(self.date_obj.year, self.date_obj.month,
                                                                 self.date_obj.day, start_h, start_m)
                                end_tm_obj = datetime.datetime(self.date_obj.year, self.date_obj.month,
                                                               self.date_obj.day, end_h, end_m)
                                if self.date_obj >= start_tm_obj and self.date_obj <= end_tm_obj:
                                    student['status'] = "空闲 %d 分钟" % (
                                        int((end_tm_obj - self.date_obj).seconds / 60))


        except Exception as e:
            print(e)
            raise(e)

        self.trigger_status.emit("finished_%s" % self.room_id)



class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon('logo.jpg'))
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("JLU 课程设计")
        self.setFixedSize(self.width(), self.height())
        self._translate = QtCore.QCoreApplication.translate

        self.timeEdit.setEnabled(False)
        self.calendarWidget.setEnabled(False)

        self.timeEdit.setTime(QTime(10, 0, 0))

        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(
            ["座位ID", "姓名", "专业","座位状态"])
        self.tableView.setModel(self.table_model)
        self.tableView.setColumnWidth(0, 50)
        self.tableView.setColumnWidth(2,140)
        self.tableView.setColumnWidth(3, 140)
        self.time_table={
            "1": "08:00-09:40",
            "2": "08:00-09:40",
            "3": "10:00-11:40",
            "4": "10:00-11:40",
            "5": "13:30-15:10",
            "6": "13:30-15:10",
            "7": "15:30-17:10",
            "8": "15:30-17:10",
            "9": "18:00-19:40",
            "10": "18:00-19:40",
        }
        self.time_table_detail={}
        for class_ind in self.time_table:
            start,end = self.time_table[class_ind].split("-")
            start_h,start_m = start.split(":")
            end_h,end_m = end.split(":")
            self.time_table_detail[class_ind]={
                "start_h":int(start_h),
                "start_m":int(start_m),
                "end_h":int(end_h),
                "end_m":int(end_m)
            }
        print(self.time_table_detail)



        self.classes = None
        self.students = None
        self.infoLabel.setVisible(False)
        self.goBtn.setEnabled(False)
        self.loadConfigBtn.setEnabled(False)
        self.loadCourseBtn.clicked.connect(self.doOpenCourseFile)
        self.loadConfigBtn.clicked.connect(self.doOpenConfig)
        self.goBtn.clicked.connect(self.doClickGoBtn)

    def doOpenConfig(self):
        file_, filetype = QFileDialog.getOpenFileName(self,
                                                      "选取文件",
                                                      ".",
                                                      "Excel xls (*.xls);;Excel xlsx (*.xlsx)")  # 设置文件扩展名过滤,注意用双分号间隔
        if not file_ or len(file_) == 0:
            QMessageBox.information(self, "选择文件",
                                    self.tr("未选择文件"))
            return
        res = utils.parse_config(file_)
        if res != None:
            self.rooms = res
            self.goBtn.setEnabled(True)
            start_date = datetime.datetime(2018,9,3)
            max_week = 0
            for room_id in self.rooms:
                students = self.rooms[room_id]
                for student in students:
                    if len(student['name']) == 0:
                        continue
                    cls  =student['class']
                    if cls in self.classes:
                        for course_name in self.classes[cls]:
                            for course in self.classes[cls][course_name]:
                                max_week = max(max_week,max(course['weeks']))

            end_date = start_date + datetime.timedelta(days = max_week * 7)
            self.calendarWidget.setMinimumDate(QDate(start_date.year, start_date.month, start_date.day))
            self.calendarWidget.setMaximumDate(QDate(end_date.year, end_date.month, end_date.day))
            self.calendarWidget.setEnabled(True)
            self.timeEdit.setEnabled(True)
            self.room_ids.clear()
            for room_id in self.rooms.keys():
                self.room_ids.addItem("阅览室_%s" % room_id)

            QMessageBox.information(self, "提示",
                                    self.tr("提取配置 成功"))
            return
        else:
            QMessageBox.information(self, "提示",
                                    self.tr("提取配置 失败"))
            return


    def doOpenCourseFile(self):
        file_, filetype = QFileDialog.getOpenFileName(self,
                                                      "选取文件",
                                                      ".",
                                                      "Excel xls (*.xls);;Excel xlsx (*.xlsx)")  # 设置文件扩展名过滤,注意用双分号间隔
        if not file_ or len(file_) == 0:
            QMessageBox.information(self, "选择文件",
                                    self.tr("未选择文件"))
            return
        res =  utils.parser_class_all(file_)
        if res != None:
            self.classes = res
            self.loadConfigBtn.setEnabled(True)
            self.calendarWidget.setEnabled(False)
            self.timeEdit.setEnabled(False)
            self.goBtn.setEnabled(False)

            QMessageBox.information(self, "提示",
                                    self.tr("提取课程表文件 成功"))
            return
        else:
            QMessageBox.information(self, "提示",
                                    self.tr("提取课程表文件内容失败"))
            return
    def doClickGoBtn(self):
        self.table_model.clear()
        self.table_model.setHorizontalHeaderLabels(
            ["座位ID", "姓名", "专业", "座位状态"])
        self.tableView.setColumnWidth(0, 50)
        self.tableView.setColumnWidth(2, 140)
        self.tableView.setColumnWidth(3, 140)
        room_id = self.room_ids.currentText()
        room_id = room_id[len("阅览室_"):]
        print(room_id)





        qdate_obj = self.calendarWidget.selectedDate()
        year,month,day,week_day = qdate_obj.year(),qdate_obj.month(),qdate_obj.day(),qdate_obj.dayOfWeek()
        qtime_obj = self.timeEdit.time()
        hour,minute =qtime_obj.hour(),qtime_obj.minute()
        print(year,month,day,week_day)
        print(hour,minute)
        date_obj = datetime.datetime(year,month,day,hour,minute,0)
        self.loadConfigBtn.setEnabled(False)
        self.loadCourseBtn.setEnabled(False)
        self.goBtn.setEnabled(False)

        self.cal_thread = Cal_thread(self.classes,self.students,self.time_table_detail,date_obj,self.rooms,room_id)
        self.cal_thread.trigger_status.connect(self.callback)
        self.cal_thread.start()
        QMessageBox.information(self, "提示",
                                self.tr("处理中"))
        return


    def callback(self,res):
        if res.startswith("finished"):
            self.loadConfigBtn.setEnabled(True)
            self.loadCourseBtn.setEnabled(True)
            self.goBtn.setEnabled(True)
            room_id = res[len("finished_"):]
            row_cnt=0
            students = self.rooms[room_id]
            for student in students:
                column_cnt = 0
                for row_item in [str(student['chair_id']),
                                 student['name'],
                                 student['class'],
                                 student['status'],
                                 ]:
                    item = QStandardItem(row_item)
                    if "空闲" in student['status']:
                        item.setBackground(QBrush(QColor(0, 255, 0)))
                    elif "未分配" in student['status']:
                        item.setBackground(QBrush(QColor(0xff,0xff,0x99)))

                    else:
                        item.setBackground(QBrush(QColor(255, 0, 0)))

                    self.table_model.setItem(row_cnt, column_cnt, item)
                    column_cnt += 1
                row_cnt += 1
        elif res == "start":
            pass
        elif res.startswith("info"):
            info = res[5:]
            self.infoLabel.setVisible(True)
            self.infoLabel.setText(self._translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">%s</span></p></body></html>" % info))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainUI()
    md.show()

    sys.exit(app.exec_())
