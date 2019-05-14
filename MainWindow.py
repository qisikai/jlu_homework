# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(786, 725)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(480, 140, 248, 197))
        self.calendarWidget.setObjectName("calendarWidget")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(480, 360, 251, 71))
        self.timeEdit.setObjectName("timeEdit")
        self.loadCourseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadCourseBtn.setGeometry(QtCore.QRect(470, 30, 111, 61))
        self.loadCourseBtn.setObjectName("loadCourseBtn")
        self.loadConfigBtn = QtWidgets.QPushButton(self.centralwidget)
        self.loadConfigBtn.setGeometry(QtCore.QRect(610, 30, 111, 61))
        self.loadConfigBtn.setObjectName("loadConfigBtn")
        self.goBtn = QtWidgets.QPushButton(self.centralwidget)
        self.goBtn.setGeometry(QtCore.QRect(610, 560, 131, 101))
        self.goBtn.setObjectName("goBtn")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 421, 701))
        self.widget.setObjectName("widget")
        self.tableView = QtWidgets.QTableView(self.widget)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 421, 671))
        self.tableView.setObjectName("tableView")
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel.setGeometry(QtCore.QRect(480, 470, 241, 51))
        self.infoLabel.setObjectName("infoLabel")
        self.room_ids = QtWidgets.QComboBox(self.centralwidget)
        self.room_ids.setGeometry(QtCore.QRect(470, 580, 101, 41))
        self.room_ids.setObjectName("room_ids")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 786, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadCourseBtn.setText(_translate("MainWindow", "Load Course"))
        self.loadConfigBtn.setText(_translate("MainWindow", "Load Config"))
        self.goBtn.setText(_translate("MainWindow", "Go"))
        self.infoLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">第 xx 周 xx 节</span></p></body></html>"))

