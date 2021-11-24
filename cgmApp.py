from typing import Tuple
import shutil
import numpy as np
import time, datetime
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QGridLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
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
from pandas.core.reshape.concat import concat


class CustomTableWidget(QTableWidget):
    def __init__(self, type, parent=None):
        super(CustomTableWidget, self).__init__(parent)

    def dropEvent(self, event):
        destinationCell = self.itemAt(event.pos())
        if isinstance(destinationCell, QTableWidgetItem):
            if destinationCell.column() == 2 or destinationCell.column() == 4:
                self.dragHandler(event)
                super().dropEvent(event)
            else:
                event.ignore()

    def dragHandler(self, event):
        event.source().currentItem().setBackground(QColor.fromRgbF(0.5, 0.5, 0.5))


class FormClass(QWidget):
    fat = 0
    protein = 0
    carb = 0
    fiber = 0
    calories = 0
    mealType = " "
    mealName = " "
    window_closed = QtCore.pyqtSignal()

    def __init__(self, entryData):
        super().__init__()
        self.resize(400, 300)
        self.show()
        self.layoutInit()
        self.componentCreator(entryData)

    def layoutInit(self):
        self.verticalLayoutLabel = QVBoxLayout()
        self.verticalLayoutText = QVBoxLayout()
        self.horizontalLayoutButton = QHBoxLayout()
        self.gridLayout = QGridLayout()
        self.gridLayout.addLayout(self.verticalLayoutLabel, 0, 0)
        self.gridLayout.addLayout(self.verticalLayoutText, 0, 1)
        self.gridLayout.addLayout(self.horizontalLayoutButton, 1, 0)

        self.setWindowTitle("Modify Entry")
        self.setLayout(self.gridLayout)

    def componentCreator(self, entryData):
        newLabel = QLabel("Carb:")
        self.verticalLayoutLabel.addWidget(newLabel)

        newLabel = QLabel("Fat:")
        self.verticalLayoutLabel.addWidget(newLabel)

        newLabel = QLabel("Protein:")
        self.verticalLayoutLabel.addWidget(newLabel)

        newLabel = QLabel("Fiber:")
        self.verticalLayoutLabel.addWidget(newLabel)

        newLabel = QLabel("Calories:")
        self.verticalLayoutLabel.addWidget(newLabel)

        newLabel = QLabel("Meal Type:")
        self.verticalLayoutLabel.addWidget(newLabel)

        newLabel = QLabel("Meal Name:")
        self.verticalLayoutLabel.addWidget(newLabel)

        # ----------------Textbox
        if entryData["Carbs"] != 0:
            self.carbTB = QLineEdit(str(entryData["Carbs"]))
        else:
            self.carbTB = QLineEdit("0")
        self.verticalLayoutText.addWidget(self.carbTB)

        if entryData["Fat"] != 0:
            self.fatTB = QLineEdit(str(entryData["Fat"]))
        else:
            self.fatTB = QLineEdit("0")
        self.verticalLayoutText.addWidget(self.fatTB)

        if entryData["Protein"] != 0:
            self.proteinTB = QLineEdit(str(entryData["Protein"]))
        else:
            self.proteinTB = QLineEdit("0")
        self.verticalLayoutText.addWidget(self.proteinTB)

        if entryData["Fiber"] != 0:
            self.fiberTB = QLineEdit(str(entryData["Fiber"]))
        else:
            self.fiberTB = QLineEdit("0")
        self.verticalLayoutText.addWidget(self.fiberTB)

        if entryData["Calories"] != 0:
            self.caloriesTB = QLineEdit(str(entryData["Calories"]))
        else:
            self.caloriesTB = QLineEdit("0")
        self.verticalLayoutText.addWidget(self.caloriesTB)

        self.mealTypeTB = QLineEdit(entryData["meal_type"])
        self.verticalLayoutText.addWidget(self.mealTypeTB)

        self.mealNameTB = QLineEdit(entryData["meal_name"])
        self.verticalLayoutText.addWidget(self.mealNameTB)

        self.doneBut = QPushButton("Done")
        self.horizontalLayoutButton.addWidget(self.doneBut)
        self.doneBut.clicked.connect(self.actionDoneBut)

    def actionDoneBut(self):
        try:
            FormClass.carb = float(self.carbTB.text())
        except ValueError:
            print("Carb is not flot")
            return

        try:
            FormClass.fat = float(self.fatTB.text())
        except ValueError:
            print("Fat is not flot")
            return

        try:
            FormClass.protein = float(self.proteinTB.text())
        except ValueError:
            print("Protein is not flot")
            return

        try:
            FormClass.fiber = float(self.fiberTB.text())
        except ValueError:
            print("Fiber is not flot")
            return

        try:
            FormClass.calories = float(self.caloriesTB.text())
        except ValueError:
            print("Calories is not flot")
            return

        FormClass.mealType = self.mealTypeTB.text()
        FormClass.mealName = self.mealNameTB.text()

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("The values are successfully saved")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
        self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.layoutMaker()  # the general layout is initiated
        self.controlButtonMaker()
        self.dailyButtonMaker()
        self.openExportButtonMaker()

        self.show()

    def modifyContent(self, rowCounter):
        entryIndex = self.tableWidget.item(rowCounter, 0).text()
        entryIndex = int(entryIndex)
        entryData = self.model.iloc[entryIndex, :]
        self.modifyRecord = FormClass(entryData)
        self.modifyRecord.window_closed.connect(lambda: self.modifyAux(entryIndex))

    # --------------------------Setting the model
    def modifyAux(self, entryIndex):
        self.actionUpdateButton()
        self.model["Calories"].iloc[entryIndex] = self.modifyRecord.calories
        self.model["Carbs"].iloc[entryIndex] = self.modifyRecord.carb
        self.model["Protein"].iloc[entryIndex] = self.modifyRecord.protein
        self.model["Fat"].iloc[entryIndex] = self.modifyRecord.fat
        self.model["Fiber"].iloc[entryIndex] = self.modifyRecord.fiber

        self.model["meal_type"].iloc[entryIndex] = self.modifyRecord.mealType
        self.model["meal_name"].iloc[entryIndex] = self.modifyRecord.mealName
        self.tableWidgetRefresher()

    def modelInit(self):
        os.chdir(self.baseAdd)
        if not os.path.exists(os.path.join(self.baseAdd, "ProcessedFile.csv")):
            shutil.copyfile(self.mealCSVAdd, os.path.join(self.baseAdd, "ProcessedFile.csv"))
        self.model = pd.read_csv(os.path.join(self.baseAdd, "ProcessedFile.csv"))

    def modelChecker(self):
        headers = self.model.columns.tolist()
        checkLists = [
            "Date",
            "start_time",
            "end_time",
            "meal_type",
            "meal_name",
            "start_photo",
            "finish_photo",
            "mfp_entry",
            "Calories",
            "Carbs",
            "Protein",
            "Fat",
            "Fiber",
            "ratio",
            "notes",
        ]
        for element in checkLists:
            if not element in headers:
                print("Error, please check your csv file because the headers is not right***********")
                sys.exit()

    def modelCorrector(self):
        returningModel = False
        headers = self.model.columns
        for counter in range(len(headers)):
            if headers[counter] == "user_id":
                self.model.drop(headers[counter], axis=1, inplace=True)
            if headers[counter] == "RecordIndex":
                returningModel = True
        if not returningModel:
            self.model.insert(0, "RecordIndex", 0)
            self.model.insert(len(self.model.columns), "start_photo_address", " ")
            self.model.insert(len(self.model.columns), "finish_photo_address", " ")
            # self.model['start_photo_address'] = self.model['start_photo_address'].astype(str)
            # self.model['finish_photo_address'] = self.model['finish_photo_address'].astype(str)
            self.model["ratio"] = 100

        for counter in range(len(self.model)):
            if not returningModel:  # the first time that the application is processing the CSV
                self.model.iloc[counter, 0] = counter
                self.model["mfp_entry"].iloc[counter] = 1
            if self.model["start_photo_address"].iloc[counter] == " ":
                self.model["start_time"].iloc[counter] = " "
                self.model["start_photo"].iloc[counter] = 0
            if self.model["finish_photo_address"].iloc[counter] == " ":
                self.model["end_time"].iloc[counter] = " "
                self.model["finish_photo"].iloc[counter] = 0

    def todayReader(self, today):
        todayCSV = self.model
        todayMask = todayCSV["Date"] == today
        todayCSV = todayCSV.loc[todayMask]
        return todayCSV

    def mealPicReader(self):
        photoDir = os.path.join(self.participantAdd, "whatsapp_photos")
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
        self.openExportButtonLayout = QHBoxLayout()
        self.controlButtonLayout = QHBoxLayout()
        self.dateLayout = QHBoxLayout()
        self.appGridLayout = QGridLayout()

        self.dateLabel = QLabel(" ")
        self.dateLayout.addStretch()
        self.dateLayout.addWidget(self.dateLabel)
        self.dateLayout.addStretch()

        self.tableWidget = CustomTableWidget(self)
        self.listLayout.addWidget(self.tableWidget, 70)
        self.sorttedPicturesLayout()

        self.listWidget = QListWidget()
        self.listLayout.addWidget(self.listWidget, 30)
        self.listWidgetLayout()

        self.appGridLayout.addLayout(self.dateLayout, 0, 0)
        self.appGridLayout.addLayout(self.listLayout, 1, 0)
        self.appGridLayout.addLayout(self.controlButtonLayout, 2, 0)
        self.appGridLayout.addLayout(self.dailyButtonLayout, 3, 0)
        self.appGridLayout.addLayout(self.openExportButtonLayout, 4, 0)
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
        # self.listWidget.setViewMode(QListWidget.IconMode)
        self.listWidget.setAcceptDrops(False)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setIconSize(QSize(200, 200))
        self.listWidget.setDragDropOverwriteMode(True)

    def listWidgetRefresher(self):
        today = self.dates[self.todayCounter]
        photoDir = os.path.join(self.participantAdd, "whatsapp_photos")
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
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Index", "Meal", "Start Pic", "Start Time", "End Pic", "End Time", "Ratio (%)", "Note", "Modify"]
        )
        myFont = self.font()
        myFont.setPointSize(18)
        self.tableWidget.horizontalHeader().setFont(myFont)
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.setFont(myFont)
        self.tableWidget.setColumnWidth(1, 300)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(4, 150)

        headers = self.tableWidget.horizontalHeader()
        headers.setSectionResizeMode(7, QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)

    def tableWidgetRefresher(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        self.tableWidget.update()

        todayRec = self.todayReader(self.dates[self.todayCounter])
        for rowCounter in range(len(todayRec)):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidgetItemFormatter(self.tableWidget.rowCount() - 1)

        self.tableWidget.setIconSize(QSize(100, 100))
        self.tableWidget.setDragDropOverwriteMode(False)

        for counter in range(len(todayRec)):
            tempRec = todayRec["RecordIndex"].iloc[counter]
            self.tableWidget.item(counter, 0).setText(str(tempRec))

            tempRec = todayRec["meal_type"].iloc[counter] + "\n" + todayRec["meal_name"].iloc[counter]
            self.tableWidget.item(counter, 1).setText(tempRec)
        self.tableWidget.update()
        self.tableWidgetItemAdder()

    def tableWidgetItemFormatter(self, currentRow):
        for columnCounter in range(self.tableWidget.columnCount()):
            if columnCounter == 6:
                newItem = QComboBox()
                newItem.addItems(["100%", "75%", "50%", "25%", "0%"])
                self.tableWidget.setCellWidget(currentRow, columnCounter, newItem)
            elif columnCounter == 8:
                newItem = QPushButton()
                newItem.setText("Modify")
                newItem.setMaximumHeight(30)
                newItem.setMaximumWidth(100)
                newItem.clicked.connect(lambda: self.modifyContent(currentRow))
                self.tableWidget.setCellWidget(currentRow, columnCounter, newItem)
            else:
                newItem = QTableWidgetItem(" ", 0)
                newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                newItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                if columnCounter <= 1:
                    newItem.setFlags(newItem.flags())  # name and record number
                if columnCounter == 2 or columnCounter == 4:  # pic columns
                    newItem.setFlags(newItem.flags() | QtCore.Qt.ItemIsDropEnabled)
                if columnCounter == 7:
                    newItem.setFlags(newItem.flags() | QtCore.Qt.ItemIsEditable)
                self.tableWidget.setItem(currentRow, columnCounter, newItem)
        self.tableWidget.setRowHeight(currentRow - 1, 100)
        self.tableWidget.setColumnHidden(3, True)
        self.tableWidget.setColumnHidden(5, True)

    def tableWidgetItemAdder(self):
        if self.tableWidget.rowCount() == 0:
            return
        photoDir = os.path.join(self.participantAdd, "whatsapp_photos")
        os.chdir(photoDir)
        for counter in range(self.tableWidget.rowCount()):
            indexEntry = self.tableWidget.item(counter, 0).text()
            indexEntry = int(indexEntry)
            itemFileName = self.model["start_photo_address"].iloc[indexEntry]
            if itemFileName != " ":
                widgetItem = QTableWidgetItem(QIcon(itemFileName), itemFileName)
                self.tableWidget.setItem(counter, 2, widgetItem)

            itemFileName = self.model["finish_photo_address"].iloc[indexEntry]
            if itemFileName != " ":
                widgetItem = QTableWidgetItem(QIcon(itemFileName), itemFileName)
                self.tableWidget.setItem(counter, 4, widgetItem)

            itemData = self.model["ratio"].iloc[indexEntry]
            widgetItem = QComboBox()
            widgetItem.addItems(["0", "25", "50", "75", "100"])
            if itemData == 0:
                widgetItem.setCurrentIndex(0)
            elif itemData == 25:
                widgetItem.setCurrentIndex(1)
            elif itemData == 50:
                widgetItem.setCurrentIndex(2)
            elif itemData == 75:
                widgetItem.setCurrentIndex(3)
            elif itemData == 100:
                widgetItem.setCurrentIndex(4)
            else:
                print("MAYDAY.The ratio of the food is not among the set values.", itemData)
                sys.exit()
            self.tableWidget.setCellWidget(counter, 6, widgetItem)

            itemData = self.model["notes"].iloc[indexEntry]
            if not pd.isnull(itemData):
                widgetItem = QTableWidgetItem(itemData)
                self.tableWidget.setItem(counter, 7, widgetItem)

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

    def openExportButtonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)

        openButton = QPushButton("Open")
        openButton.setFont(myFont)        

        exportButton = QPushButton("Export")
        exportButton.setFont(myFont)       

        openButton.setMaximumWidth(150)
        self.openExportButtonLayout.addWidget(openButton)
        openButton.clicked.connect(self.actionOpenButton)

        exportButton.setMaximumWidth(150)
        self.openExportButtonLayout.addWidget(exportButton)
        exportButton.clicked.connect(self.actionExportButton)

    # -------------------------Button actions
    def actionOpenButton(self):
        self.modelFileDialog=QFileDialog()
        self.modelFileDialog.setFileMode(QFileDialog.AnyFile)
        self.modelFileDialog.setNameFilters(["Comma-separated value (*.csv)"])

        self.modelFileDialog.exec_()
        self.mealCSVAdd=self.modelFileDialog.selectedFiles()
        self.mealCSVAdd=self.mealCSVAdd[0]
        if('.csv' not in self.mealCSVAdd):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("The address file does not contain csv.")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return
        self.baseAdd=os.path.dirname(self.mealCSVAdd)
        self.participantAdd=os.path.dirname(self.baseAdd)

        self.modelInit()
        self.modelChecker()
        self.modelCorrector()
        self.mealPicReader()

        self.tableWidgetRefresher()
        self.listWidgetRefresher()

    def actionExportButton(self):
        self.actionUpdateButton()
        self.model.to_csv(os.path.join(self.baseAdd, "ProcessedFile.csv"), index=False)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("The file is successfully saved")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def actionAddButton(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidgetItemFormatter(self.tableWidget.rowCount() - 1)

        newRow = []
        newRow.append(len(self.model))  # record number
        newRow.append(self.dates[self.todayCounter])  # Date
        newRow.append(" ")  # start time
        newRow.append(" ")  # end time
        newRow.append("Custom Entry")  # meal type
        newRow.append("Custom Meal")  # meal name
        newRow.append(0)  # start photo flag
        newRow.append(0)  # end photo flag
        newRow.append(0)  # myfitnesspal flag
        newRow.append(0)  # calories
        newRow.append(0)  # carbs
        newRow.append(0)  # protein
        newRow.append(0)  # fat
        newRow.append(0)  # fiber
        newRow.append(0)  # ratio
        newRow.append(" ")  # notes
        newRow.append(" ")  # start photo pic
        newRow.append(" ")  # finish photo pic
        newRow = [newRow]

        newPd = pd.DataFrame(newRow, columns=self.model.columns.tolist())
        # newPd["Date"] = pd.to_datetime(newPd["Date"])
        newPd["start_photo_address"] = newPd["start_photo_address"].astype(str)
        newPd["finish_photo_address"] = newPd["finish_photo_address"].astype(str)
        frames = [self.model, newPd]
        self.model = pd.concat(frames)
        self.tableWidgetRefresher()

    def actionCleanButton(self):
        for element in self.tableWidget.selectedItems():
            cleanedColumn = element.column()
            cleanedRow = element.row()
            if cleanedColumn == 2:
                element.setIcon(QIcon())
                element.setText(" ")
                entryIndex = self.tableWidget.item(cleanedRow, 0).text()
                entryIndex = int(entryIndex)
                self.model["start_time"].iloc[entryIndex] = " "
                self.model["start_photo_address"].iloc[entryIndex] = " "
            if cleanedColumn == 4:
                element.setIcon(QIcon())
                element.setText(" ")
                entryIndex = self.tableWidget.item(cleanedRow, 0).text()
                entryIndex = int(entryIndex)
                self.model["end_time"].iloc[entryIndex] = " "
                self.model["finish_photo_address"].iloc[entryIndex] = " "
            if cleanedColumn == 7:
                element.setIcon(QIcon())
                element.setText(" ")
                entryIndex = self.tableWidget.item(cleanedRow, 0).text()
                entryIndex = int(entryIndex)
                self.model["notes"].iloc[entryIndex] = " "

            self.actionUpdateButton()

    def actionUpdateButton(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            entryIndex = self.tableWidget.item(rowCounter, 0).text()
            entryIndex = int(entryIndex)
            if self.tableWidget.item(rowCounter, 2).text() != " ":
                entryTemp = self.tableWidget.item(rowCounter, 2).text()
                self.model["start_photo_address"].iloc[entryIndex] = entryTemp
                self.tableWidget.item(rowCounter, 3).setText(entryTemp)
                if entryTemp.rindex("_") == -1 or entryTemp.rindex(".") == -1:
                    print("MAYDAY in actionUpdateButton function the file name is not right")
                    sys.exit()
                entryTemp = entryTemp[: entryTemp.rindex(".")]
                try:
                    entryTemp = datetime.datetime.strptime(entryTemp, "%Y-%m-%d__%H-%M")
                    entryTemp = entryTemp.strftime("%Y-%m-%d_%H:%M")
                except ValueError:
                    print("MAYDAY in actionUpdateButton function the file name is not in time format")
                    sys.exit()
                self.model["start_time"].iloc[entryIndex] = entryTemp
                self.model["start_photo"].iloc[entryIndex] = 1

            if self.tableWidget.item(rowCounter, 4).text() != " ":
                entryTemp = self.tableWidget.item(rowCounter, 4).text()
                self.model["finish_photo_address"].iloc[entryIndex] = entryTemp
                self.tableWidget.item(rowCounter, 5).setText(entryTemp)
                if entryTemp.rindex("_") == -1 or entryTemp.rindex(".") == -1:
                    print("MAYDAY in actionUpdateButton function the file name is not right")
                    sys.exit()
                entryTemp = entryTemp[: entryTemp.rindex(".")]
                try:
                    entryTemp = datetime.datetime.strptime(entryTemp, "%Y-%m-%d__%H-%M")
                    entryTemp = entryTemp.strftime("%Y-%m-%d_%H:%M")
                except ValueError:
                    print("MAYDAY in actionUpdateButton function the file name is not in time format")
                    sys.exit()
                self.model["end_time"].iloc[entryIndex] = entryTemp
                self.model["finish_photo"].iloc[entryIndex] = 1

            entryTemp = self.tableWidget.cellWidget(rowCounter, 6).currentText()
            self.model["ratio"].iloc[entryIndex] = int(entryTemp)

            if self.tableWidget.item(rowCounter, 7).text() != " ":
                entryTemp = self.tableWidget.item(rowCounter, 7).text()
                self.model["notes"].iloc[entryIndex] = entryTemp

    def actionPrevButton(self):
        self.todayCounter -= 1
        if self.todayCounter < 0:
            self.todayCounter = len(self.dates) - 1
        today = self.dates[self.todayCounter]
        print(today)
        self.listWidgetRefresher()
        self.tableWidgetRefresher()
        self.actionUpdateButton()

    def actionNextButton(self):
        self.todayCounter += 1
        if self.todayCounter >= len(self.dates):
            self.todayCounter = 0
        today = self.dates[self.todayCounter]
        print(today)
        self.listWidgetRefresher()
        self.tableWidgetRefresher()
        self.actionUpdateButton()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())