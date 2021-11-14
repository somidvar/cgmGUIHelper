from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTabBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QListWidgetItem,
)
from PyQt5.QtGui import QIcon, QColor
import sys
import os
import pandas as pd


class CustomTableWidget(QTableWidget):
    def __init__(self, type, parent=None):
        super(CustomTableWidget, self).__init__(parent)

    def dropEvent(self, event):
        destinationCell = self.itemAt(event.pos())
        if isinstance(destinationCell, QTableWidgetItem):
            if destinationCell.column() == 1 or destinationCell.column() == 3:
                self.dragHandler(event)
                super().dropEvent(event)
            else:
                event.ignore()

    def dragHandler(self, event):
        event.source().currentItem().setBackground(QColor.fromRgbF(0.5, 0.5, 0.5))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.layoutMaker()  # the general layout is initiated
        self.csvReader()  # the csv of the meal is read
        self.mealPicReader()
        self.tableWidgetRefresher()
        self.listWidgetRefresher()
        self.controlButtonMaker()
        self.dailyButtonMaker()
        self.exportButtonMaker()

        self.show()

    # --------------------------Setting the model
    def csvReader(self):
        csvDir = os.path.join(baseDir, "meals")
        os.chdir(csvDir)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if ".csv" in name:
                    mealCSV = pd.read_csv(name)
                    break
        
        self.mealCSV = mealCSV
        self.modelCorrector()
    def modelCorrector(self):
        headers=self.mealCSV.columns
        for counter in range(len(headers)):
            if headers[counter]=='user_id':
                self.mealCSV.drop(headers[counter],axis=1,inplace=True)
                break
        self.mealCSV.insert(0,'RecIndex',0)
        for counter in range(len(self.mealCSV)):
            self.mealCSV.iloc[counter,0]=counter
            self.mealCSV['start_photo']=0
            self.mealCSV['finish_photo']=0
            self.mealCSV['mfp_entry']=1

    def mealReader(self, today):
        mealCSV = self.mealCSV
        mealCSV = mealCSV[mealCSV["Date"].str.contains(today)]
        mealType = mealCSV["meal_type"].to_list()
        mealName = mealCSV["meal_name"].to_list()
        meals = []
        for counter in range(len(mealName)):
            temp = mealType[counter]
            temp = temp.capitalize()
            temp += "\n" + mealName[counter]
            meals.append(temp)
        self.todayMeals = meals

    def mealPicReader(self):
        photoDir = os.path.join(baseDir, "whatsapp_photos")
        os.chdir(photoDir)
        self.todayCounter = 0
        self.dates = []
        self.photos = []
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if ".jpg" not in name and ".jpeg" not in name and ".png" not in name:
                    continue
                self.photos.append(name)
                myDate = name
                myDate = myDate[: myDate.index("_")]
                self.dates.append(myDate)

        self.dates = list(set(self.dates))
        self.dates.sort()

    # ----------------------------General layout setter
    def layoutMaker(self):
        self.setGeometry(10, 10, 1500, 2000)
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

        self.tableWidget = CustomTableWidget(self)
        self.listLayout.addWidget(self.tableWidget)
        self.sorttedPicturesLayout()
        

        self.listWidget = QListWidget()
        self.listLayout.addWidget(self.listWidget)
        self.listWidgetLayout()

        self.appGridLayout.addLayout(self.dateLayout, 0, 0)
        self.appGridLayout.addLayout(self.listLayout, 1, 0)
        self.appGridLayout.addLayout(self.controlButtonLayout, 2, 0)
        self.appGridLayout.addLayout(self.dailyButtonLayout, 3, 0)
        self.appGridLayout.addLayout(self.exportButtonLayout, 4, 0)
        self.setWindowTitle("CGM Application")
        self.setLayout(self.appGridLayout)

    def dateLabelSetter(self, currDate):
        currDateStr = "Date: " + currDate
        myFont = self.font()
        myFont.setPointSize(30)
        self.dateLabel.setFont(myFont)
        self.dateLabel.setText(currDate)

    # ------------------------------ListWidget Item
    def listWidgetLayout(self):
        self.listWidget.setViewMode(QListWidget.IconMode)
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setIconSize(QSize(200, 200))
        self.listWidget.setDragDropOverwriteMode(True)



    def listWidgetRefresher(self):
        today = self.dates[self.todayCounter]       
        photoDir = os.path.join(baseDir, "whatsapp_photos")
        os.chdir(photoDir)

        self.dateLabelSetter(today)
        widgetItems = []
        self.listWidget.clear()

        todayPhotos = []
        for element in self.photos:
            if today in element:
                todayPhotos.append(element)

        for photo in todayPhotos:
            widgetItem = QListWidgetItem(QIcon(photo), photo)
            widgetItems.append(widgetItem)

        for count, element in enumerate(widgetItems):
            self.listWidget.insertItem(count, element)
        self.listWidget.update()

    # ------------------------------TableWidget
    def sorttedPicturesLayout(self):
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            [
                "Meal",
                "Start Pic",
                "Start Time",
                "End Pic",
                "End Time",
                "Completion",
                "Note",
            ]
        )

        myFont = self.font()
        myFont.setPointSize(18)
        self.tableWidget.setAcceptDrops(True)

        self.tableWidget.setFont(myFont)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(3, 100)

        headers = self.tableWidget.horizontalHeader()
        headers.setSectionResizeMode(6, QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)

    def tableWidgetRefresher(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        self.tableWidget.update()

        self.mealReader(self.dates[self.todayCounter])
        for rowCounter in range(len(self.todayMeals)):
            self.actionAddButton()

        self.tableWidget.setIconSize(QSize(100, 100))
        self.tableWidget.setDragDropOverwriteMode(False)

        for counter in range(len(self.todayMeals)):
            self.tableWidget.item(counter, 0).setText(self.todayMeals[counter])

    def tableWidgetItemFormatter(self, currentRow):
        for columnCounter in range(self.tableWidget.columnCount()):
            if columnCounter == 5:
                newItem = QComboBox()
                newItem.addItems(["100%", "75%", "50%", "25%", "0%"])
                self.tableWidget.setCellWidget(currentRow, columnCounter, newItem)
            else:
                newItem = QTableWidgetItem("", 0)
                newItem.setTextAlignment(
                    QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter
                )
                newItem.setFlags(QtCore.Qt.ItemIsSelectable)
                if columnCounter != 0:
                    newItem.setFlags(newItem.flags() | QtCore.Qt.ItemIsEnabled)
                if columnCounter == 1 or columnCounter == 3:
                    newItem.setFlags(
                        newItem.flags()
                        | QtCore.Qt.ItemIsDropEnabled
                        | QtCore.Qt.ItemIsEditable
                    )
                if columnCounter == 6:
                    newItem.setFlags(newItem.flags() | QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(currentRow, columnCounter, newItem)
        self.tableWidget.setRowHeight(currentRow - 1, 100)

    # ---------------------------------Button layout
    def dailyButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)

        prevButton = QPushButton("<< Prev Day")
        updateButton = QPushButton("Update Today")
        nextButton = QPushButton("Next Day>>")

        prevButton.setFont(myFont)
        updateButton.setFont(myFont)
        nextButton.setFont(myFont)

        self.dailyButtonLayout.addStretch()
        self.dailyButtonLayout.addWidget(prevButton)
        self.dailyButtonLayout.addWidget(updateButton)
        self.dailyButtonLayout.addWidget(nextButton)
        self.dailyButtonLayout.addStretch()
        updateButton.clicked.connect(self.actionUpdateButton)
        nextButton.clicked.connect(self.actionNextButton)
        prevButton.clicked.connect(self.actionPrevButton)

    def controlButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)
        addButton = QPushButton("Add Row")
        cleanButton = QPushButton("Clean Cells")

        addButton.setFont(myFont)
        cleanButton.setFont(myFont)

        self.controlButtonLayout.addStretch()
        self.controlButtonLayout.addWidget(addButton)
        self.controlButtonLayout.addWidget(cleanButton)
        self.controlButtonLayout.addStretch()

        addButton.clicked.connect(self.actionAddButton)
        cleanButton.clicked.connect(self.actionCleanButton)

        addButton.setMaximumWidth(150)
        cleanButton.setMaximumWidth(150)

    def exportButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)
        exportButton = QPushButton("Export")
        exportButton.setFont(myFont)

        exportButton.setMaximumWidth(150)
        self.exportButtonLayout.addWidget(exportButton)
        exportButton.clicked.connect(self.actionExportButton)

    # -------------------------Button actions
    def actionExportButton(self):
        print("fix me-------------")

    def actionAddButton(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidgetItemFormatter(self.tableWidget.rowCount() - 1)

    def actionCleanButton(self):
        for element in self.tableWidget.selectedItems():
            element.setIcon(QIcon())
            element.setText("")

    def actionUpdateButton(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            tempVal = self.tableWidget.item(rowCounter, 1).text()
            self.tableWidget.item(rowCounter, 2).setText(tempVal)

        for rowCounter in range(self.tableWidget.rowCount()):
            tempVal = self.tableWidget.item(rowCounter, 3).text()
            self.tableWidget.item(rowCounter, 4).setText(tempVal)

    def actionPrevButton(self):
        self.todayCounter -= 1
        if self.todayCounter < 0:
            self.todayCounter = len(self.dates) - 1
        today = self.dates[self.todayCounter]
        print(today)
        self.listWidgetRefresher()
        self.mealReader(today)
        self.tableWidgetRefresher()

    def actionNextButton(self):
        self.todayCounter += 1
        if self.todayCounter >= len(self.dates):
            self.todayCounter = 0
        today = self.dates[self.todayCounter]
        self.listWidgetRefresher()
        print(today)
        self.mealReader(today)
        self.tableWidgetRefresher()


baseDir = "/Users/sorush/Github/cgmGUIHelper/caM01-001/"
os.chdir(baseDir)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
