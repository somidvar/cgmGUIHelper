from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtWidgets import QApplication, QGridLayout, QHeaderView, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QListWidget, QHBoxLayout,QListWidgetItem
from PyQt5.QtGui import QIcon
import sys,os
import pandas as pd
 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.meals=[]
        self.layoutMaker()      
        
        self.unsorttedPictures()
        self.todayCounter=0
        today=self.dates[self.todayCounter]
        self.mealReader(today)

        self.sorttedPictures()
        self.buttonMaker()
        
        self.show()

    def mealReader(self,today):
        mealDir=os.path.join(baseDir,'meals')
        os.chdir(mealDir)
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:                
                if '.csv' in name:
                    mealCSV=pd.read_csv(name)  
                    break
        mealCSV=mealCSV[mealCSV['Date'].str.contains(today)]
        mealType=mealCSV['meal_type'].to_list()
        mealName=mealCSV['meal_name'].to_list()
        meals=[]
        for counter in range(len(mealName)):
            temp=mealType[counter]
            temp=temp.capitalize()
            temp+="\n"+mealName[counter]
            meals.append(temp)
        self.meals=meals

    def layoutMaker(self):
        self.setGeometry(100, 100, 2000, 2000)
        self.listLayout = QHBoxLayout()
        self.buttonLayout=QHBoxLayout()
        self.dateLayout=QHBoxLayout()
        self.appGridLayout=QGridLayout()

        self.dateLabel=QLabel("")
        self.dateLayout.addStretch()
        self.dateLayout.addWidget(self.dateLabel)
        self.dateLayout.addStretch()

        self.tableWidget=QTableWidget()
        self.listLayout.addWidget(self.tableWidget)

        self.sorttedPicturesLayout()

        self.appGridLayout.addLayout(self.dateLayout,0,0)
        self.appGridLayout.addLayout(self.listLayout,1,0)
        self.appGridLayout.addLayout(self.buttonLayout,2,0)
        self.setWindowTitle('CGM Application')
        self.setLayout(self.appGridLayout)
    
    def unsorttedPictures(self):
        self.unsortedListWidget = QListWidget()    
        self.unsortedListWidget.setViewMode(QListWidget.IconMode)
        self.unsortedListWidget.setAcceptDrops(True)
        self.unsortedListWidget.setDragEnabled(True)
        self.unsorttedPicturesDateExt()
        
        today=self.dates[0]

        self.unsorttedPicturesRefresher(today)
        self.unsortedListWidget.setIconSize(QSize(200,200))
        self.unsortedListWidget.setDragDropOverwriteMode(True)   
        self.listLayout.addWidget(self.unsortedListWidget)

    def unsorttedPicturesDateExt(self):
        photoDir=os.path.join(baseDir,'whatsapp_photos')
        os.chdir(photoDir)
        
        self.dates=[]
        self.photos=[]
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:                
                if '.jpg' not in name and '.jpeg' not in name and '.png' not in name:
                    continue
                self.photos.append(name)
                myDate=name
                myDate=myDate[:myDate.index('_')]
                self.dates.append(myDate)

        self.dates=list(set(self.dates))      
        self.dates.sort()


    def unsorttedPicturesRefresher(self,today):
        photoDir=os.path.join(baseDir,'whatsapp_photos')
        os.chdir(photoDir)

        self.dateSetter(today)
        self.widgetItems=[]
        self.unsortedListWidget.clear()

        todayPhotos=[]
        for element in self.photos:
            if today in element:
                todayPhotos.append(element)

        for photo in todayPhotos:
            widgetItem=QListWidgetItem(QIcon(photo), photo)
            self.widgetItems.append(widgetItem)
        
        for count, element in enumerate(self.widgetItems):
            self.unsortedListWidget.insertItem(count,element)
        self.unsortedListWidget.update()

    def sorttedPictures(self):
        for rowCounter in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)

        self.tableWidget.update()
        self.sorttedPicturesLayout()
        if (len(self.meals)==0):
            return
        for meal in self.meals:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            newItem=QTableWidgetItem(meal,0)
            newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            newItem.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,0,newItem)

            newItem=QTableWidgetItem("",0)
            newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            newItem.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,2,newItem)            

            newItem=QTableWidgetItem("",0)
            newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            newItem.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget.setItem(self.tableWidget.rowCount()-1,4,newItem)

            self.tableWidget.setRowHeight(self.tableWidget.rowCount()-1,200)
            self.tableWidget.setIconSize(QSize(200,200))
        
    def sorttedPicturesLayout(self):
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Meal","Start Pic","Start Time","End Pic","End Time"])

        myFont = self.font()
        myFont.setPointSize(18)
        self.tableWidget.setAcceptDrops(True)

        self.tableWidget.setFont(myFont)
        self.tableWidget.setColumnWidth(1,300)
        self.tableWidget.setColumnWidth(3,300)

        headers = self.tableWidget.horizontalHeader()
        headers.setSectionResizeMode(0,QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)


    def buttonMaker(self):
        myFont = self.font()
        myFont.setPointSize(18)
        prevButton=QPushButton("<< Prev")
        doneButton=QPushButton("Done")
        nextButton=QPushButton("Next >>")
        
        prevButton.setFont(myFont)
        doneButton.setFont(myFont)
        nextButton.setFont(myFont)

        self.buttonLayout.addWidget(prevButton)
        self.buttonLayout.addWidget(doneButton)
        self.buttonLayout.addWidget(nextButton)
        doneButton.clicked.connect(self.actionDoneButton)
        nextButton.clicked.connect(self.actionNextButton)
        prevButton.clicked.connect(self.actionPrevButton)

    def actionDoneButton(self):
        print("FIX ME-----------")
        print(self.dates)

    def actionPrevButton(self):
        self.todayCounter-=1
        if(self.todayCounter<0):
            self.todayCounter=len(self.dates)-1
        today=self.dates[self.todayCounter]
        print(today)
        self.unsorttedPicturesRefresher(today)
        self.mealReader(today)
        self.sorttedPictures()

    def actionNextButton(self):
        self.todayCounter+=1
        if(self.todayCounter>=len(self.dates)):
            self.todayCounter=0
        today=self.dates[self.todayCounter]
        self.unsorttedPicturesRefresher(today)
        print(today)
        self.mealReader(today)
        self.sorttedPictures()

        
    def dateSetter(self,currDate):
        currDateStr="Date: "+currDate
        
        myFont = self.font()
        myFont.setPointSize(30)
        self.dateLabel.setFont(myFont)
        self.dateLabel.setText(currDate)


    
    



    


 
 
baseDir="/Users/sorush/Desktop/cgmAPP/caM01-001/" 
os.chdir(baseDir)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())