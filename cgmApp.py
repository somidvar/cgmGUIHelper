from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtWidgets import QApplication, QGridLayout, QHeaderView, QLabel, QPushButton, QTabBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon
import sys
import os
import pandas as pd


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.meals = []
        self.layoutMaker()

        self.unsorttedUnusedPic()
        self.todayCounter = 0
        today = self.dates[self.todayCounter]
        self.mealReader(today)

        self.sorttedPictures()
        self.controlButtonMaker()
        self.dailyButtonMaker()
        self.exportButtonMaker()

        self.show()

    def mealReader(self, today):
        mealDir = os.path.join(baseDir, 'meals')
        os.chdir(mealDir)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if '.csv' in name:
                    mealCSV = pd.read_csv(name)
                    break
        mealCSV = mealCSV[mealCSV['Date'].str.contains(today)]
        mealType = mealCSV['meal_type'].to_list()
        mealName = mealCSV['meal_name'].to_list()
        meals = []
        for counter in range(len(mealName)):
            temp = mealType[counter]
            temp = temp.capitalize()
            temp += "\n"+mealName[counter]
            meals.append(temp)
        self.meals = meals

    def layoutMaker(self):
        self.setGeometry(10, 10, 2000, 2000)
        self.listLayout = QHBoxLayout()
        self.dailyButtonLayout = QHBoxLayout()
        self.exportButtonLayout = QHBoxLayout()
        self.controlButtonLayout = QHBoxLayout()
        self.dateLayout = QHBoxLayout()
        self.appGridLayout = QGridLayout()

        self.dateLabel = QLabel("")
        self.dateLayout.addStretch()
        self.dateLayout.addWidget(self.dateLabel)
        self.dateLayout.addStretch()

        self.tableWidget = QTableWidget()
        self.tableWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.listLayout.addWidget(self.tableWidget)

        self.sorttedPicturesLayout()

        self.appGridLayout.addLayout(self.dateLayout, 0, 0)
        self.appGridLayout.addLayout(self.listLayout, 1, 0)
        self.appGridLayout.addLayout(self.controlButtonLayout, 2, 0)
        self.appGridLayout.addLayout(self.dailyButtonLayout, 3, 0)
        self.appGridLayout.addLayout(self.exportButtonLayout, 4, 0)
        self.setWindowTitle('CGM Application')
        self.setLayout(self.appGridLayout)

    def unsorttedUnusedPic(self):
        self.unsortedUnusedListWidget = QListWidget()
        self.unsortedUnusedListWidget.setViewMode(QListWidget.IconMode)
        self.unsortedUnusedListWidget.setAcceptDrops(True)
        self.unsortedUnusedListWidget.setDragEnabled(True)
        self.unsorttedUnusedPicDateExt()

        today = self.dates[0]

        self.unsorttedUnusedPicRefresher(today)
        self.unsortedUnusedListWidget.setIconSize(QSize(200, 200))
        self.unsortedUnusedListWidget.setDragDropOverwriteMode(True)
        self.listLayout.addWidget(self.unsortedUnusedListWidget)

    def unsorttedUnusedPicDateExt(self):
        photoDir = os.path.join(baseDir, 'whatsapp_photos')
        os.chdir(photoDir)

        self.dates = []
        self.photos = []
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if '.jpg' not in name and '.jpeg' not in name and '.png' not in name:
                    continue
                self.photos.append(name)
                myDate = name
                myDate = myDate[:myDate.index('_')]
                self.dates.append(myDate)

        self.dates = list(set(self.dates))
        self.dates.sort()

    def unsorttedUnusedPicRefresher(self, today):
        photoDir = os.path.join(baseDir, 'whatsapp_photos')
        os.chdir(photoDir)

        self.dateSetter(today)
        self.widgetItems = []
        self.unsortedUnusedListWidget.clear()

        todayPhotos = []
        for element in self.photos:
            if today in element:
                todayPhotos.append(element)

        for photo in todayPhotos:
            widgetItem = QListWidgetItem(QIcon(photo), photo)
            self.widgetItems.append(widgetItem)

        for count, element in enumerate(self.widgetItems):
            self.unsortedUnusedListWidget.insertItem(count, element)
        self.unsortedUnusedListWidget.update()

    def sorttedPictures(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)

        self.tableWidget.update()
        self.sorttedPicturesLayout()
        if (len(self.meals) == 0):
            return

        for rowCounter in range(len(self.meals)):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for columnCounter in range(6):
                newItem = QTableWidgetItem("", 0)
                newItem.setTextAlignment(
                    QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                newItem.setFlags(QtCore.Qt.ItemIsSelectable)
                if(columnCounter == 1 or columnCounter == 3):
                    newItem.setFlags(
                        QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowCounter, columnCounter, newItem)
            self.tableWidget.setRowHeight(self.tableWidget.rowCount()-1, 100)
        self.tableWidget.setIconSize(QSize(100, 100))
        self.tableWidget.setDragDropOverwriteMode(False)

        for counter in range(len(self.meals)):
            self.tableWidget.item(counter, 0).setText(self.meals[counter])

    def sorttedPicturesLayout(self):
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Meal", "Start Pic", "Start Time", "End Pic", "End Time", "Note"])

        myFont = self.font()
        myFont.setPointSize(18)
        self.tableWidget.setAcceptDrops(True)

        self.tableWidget.setFont(myFont)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(3, 100)

        headers = self.tableWidget.horizontalHeader()
        headers.setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)

    def dailyButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)
        prevButton = QPushButton("<< Prev Day")
        updateButton = QPushButton("Update Today")
        nextButton = QPushButton("Next Day>>")

        prevButton.setFont(myFont)
        updateButton.setFont(myFont)
        nextButton.setFont(myFont)

        self.dailyButtonLayout.addWidget(prevButton)
        self.dailyButtonLayout.addWidget(updateButton)
        self.dailyButtonLayout.addWidget(nextButton)
        updateButton.clicked.connect(self.actionUpdateButton)
        nextButton.clicked.connect(self.actionNextButton)
        prevButton.clicked.connect(self.actionPrevButton)

    def controlButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)
        addButton = QPushButton("Add Row")
        cleanButton = QPushButton("Clean Row")
        removeButton = QPushButton("Remove Row")

        addButton.setFont(myFont)
        cleanButton.setFont(myFont)
        removeButton.setFont(myFont)

        self.controlButtonLayout.addWidget(addButton)
        self.controlButtonLayout.addWidget(cleanButton)
        self.controlButtonLayout.addWidget(removeButton)
        addButton.clicked.connect(self.actionAddButton)
        cleanButton.clicked.connect(self.actionCleanButton)
        removeButton.clicked.connect(self.actionRemoveButton)

    def exportButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)
        exportButton = QPushButton("Export")
        exportButton.setFont(myFont)

        exportButton.setMaximumWidth(150)
        self.exportButtonLayout.addWidget(exportButton)
        exportButton.clicked.connect(self.actionExportButton)

    def actionExportButton(self):
        print("fix me-------------")

    def actionAddButton(self):
        print("fix me-------------")

    def actionCleanButton(self):
        print("fix me-------------")

    def actionRemoveButton(self):
        print("mamad")
        # for counter in range(self.unsortedUnusedListWidget.count()):
        #     myIcon=self.unsortedUnusedListWidget.item(counter).icon()
        #     self.unsortedUnusedListWidget.item(counter).se
        #     print(self.unsortedUnusedListWidget.item(counter).setIcon(QIcon.addPixmap(myIcon,QIcon.Disabled,mode=)))

    def actionUpdateButton(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            tempVal = self.tableWidget.item(rowCounter, 1).text()
            self.tableWidget.item(rowCounter, 2).setText(tempVal)

        for rowCounter in range(self.tableWidget.rowCount()):
            tempVal = self.tableWidget.item(rowCounter, 3).text()
            self.tableWidget.item(rowCounter, 4).setText(tempVal)

    def actionPrevButton(self):
        self.todayCounter -= 1
        if(self.todayCounter < 0):
            self.todayCounter = len(self.dates)-1
        today = self.dates[self.todayCounter]
        print(today)
        self.unsorttedUnusedPicRefresher(today)
        self.mealReader(today)
        self.sorttedPictures()

    def actionNextButton(self):
        self.todayCounter += 1
        if(self.todayCounter >= len(self.dates)):
            self.todayCounter = 0
        today = self.dates[self.todayCounter]
        self.unsorttedUnusedPicRefresher(today)
        print(today)
        self.mealReader(today)
        self.sorttedPictures()

    def dateSetter(self, currDate):
        currDateStr = "Date: "+currDate
        myFont = self.font()
        myFont.setPointSize(30)
        self.dateLabel.setFont(myFont)
        self.dateLabel.setText(currDate)


baseDir = "/Users/sorush/Github/cgmGUIHelper/caM01-001/"
os.chdir(baseDir)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
