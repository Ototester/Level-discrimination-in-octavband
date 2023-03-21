#Importing relevant libraries
import sys
import csv
from datetime import datetime
from PyQt5.QtMultimedia import (
	QMediaPlayer,
	QMediaPlaylist,
	QMediaContent,
)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QRadioButton,
    QLabel,
    QVBoxLayout,
    QFrame,
    QGridLayout,
    QLineEdit,
	QMainWindow,
	QMessageBox,
	QButtonGroup,
	
)
from PyQt5.QtCore import (
	Qt, 
	QUrl,
	QDirIterator,
	QDir,
)
from PyQt5.QtGui import (
    QFont,
    QIntValidator,
    
)
import random
from random import(
	choice
)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		onlyInt = QIntValidator(18,99)
		
		#Class variables
		self.indexLogg = []
		self.playlistNumber = -1
		self.testNumber = 0
		self.sex = ""
		self.CSVfilename = ""

		#Layout items that needs access from multiple functions
		self.lTestInfo = QLabel(text=" ")
		self.bBeginTesting = QPushButton(
			text="Starta en ny undersökningen")
		self.bBeginTesting.setStyleSheet(
			"background-color:lightgray")
		self.bEndTesting = QPushButton(
			text="Avsluta undersökningen")
		self.bEndTesting.setStyleSheet(
			"background-color:lightgray")
		self.bEndTesting.hide()
		self.lTestingOffline = QLabel(
			text="\n Undersökningen är inte igång\n")
		self.lTestingOnline = QLabel(
			text="\n Undersökningen är nu igång\n")
		self.lTestingOnline.hide()
		self.bTryOutStart = QPushButton(
			text="Prova på att göra testet\n")
		self.bTryOutEnd = QPushButton(
			text="Ljudet upplevs naturligt.\nSe resultatet för prova-på testet")
		self.bTryOutEnd.hide()
		self.bTestEnd = QPushButton(
			text="Ljudet upplevs naturligt.\nAvsluta testet och spara resultatet")
		self.bTestEnd.hide()
		self.bTestStart = QPushButton(
			text="Starta ett nytt test\n")
		self.bTestStart.hide()
		self.r1 = QRadioButton("Man")
		self.r2 = QRadioButton("Kvinna")
		self.r3 = QRadioButton("Ej angivit")
		self.group = QButtonGroup()
		self.group.addButton(self.r1)
		self.group.addButton(self.r2)
		self.group.addButton(self.r3)
		self.age = QLineEdit()
		self.age.setStyleSheet("background-color:white")
		self.age.setFixedWidth(50)
		self.age.setValidator(onlyInt)

		#Soundfiles that isnt to be used because of clipping
		self.removeItemsFromStart = [
			125, 119, 82, 70, 59, 49, 29, 23, 22, 10]
		self.removeItem = self.removeItemsFromStart.copy()
		#Specific playlist information, 
		#needs to be changed if playlists are changed
		self.playlistNumberMax = 15
		self.playlistStartLow = 6
		self.playlistStartHigh = 14
		self.orginalIndex = 10
        #Important to change if number of files per playlist is changed
		self.numberOfFiles = 153

		self.currentPlaylist = QMediaPlaylist()
		self.twoItemList = QMediaPlaylist()
		self.player = QMediaPlayer()
		self.createLayout()
	
	#Creates the main layout
	def createLayout(self):
		layout = self.layout()
		window = QWidget()
		window.setLayout(layout)
		self.setCentralWidget(window)
		self.resize(500,650)
		self.setWindowTitle('Nivåbedömning i oktavband')
		self.show()
	
	#Creates the inputbox, returns the inputframe
	def inputBoxLayout(self):
		inputFrame = QFrame()
		inputVbox = QVBoxLayout(inputFrame)
		grid = QGridLayout()
		lInstruction = QLabel(
			text="Skriv i informationen innan du börjar undersökningen")
		lInstruction.setAlignment(Qt.AlignCenter)
		lGender = QLabel(text="Kön:")
		lAge = QLabel(text="Ålder:")
		lGender.setFont(QFont("Times",weight=QFont.Bold))
		lAge.setFont(QFont("Times",weight=QFont.Bold))
		inputFrame.setStyleSheet("background-color:skyblue")
		self.lTestingOnline.setAlignment(Qt.AlignCenter)
		self.lTestingOnline.setStyleSheet("background-color: lightgreen")
		self.lTestingOffline.setAlignment(Qt.AlignCenter)
		self.lTestingOffline.setStyleSheet("background-color: red")
		
		inputVbox.addWidget(lInstruction)
		grid.addWidget(lGender,1,1,Qt.AlignLeft)
		grid.addWidget(self.r1,1,2,Qt.AlignLeft)
		grid.addWidget(self.r2,1,3,Qt.AlignLeft)
		grid.addWidget(self.r3,1,4,Qt.AlignLeft)
		grid.addWidget(lAge,1,5,Qt.AlignRight)
		grid.addWidget(self.age,1,6,Qt.AlignRight)
		inputVbox.addLayout(grid)
		inputVbox.addWidget(self.lTestingOnline)
		inputVbox.addWidget(self.lTestingOffline)
		inputVbox.addWidget(self.bBeginTesting)
		inputVbox.addWidget(self.bEndTesting)

		return inputFrame
	
	#Creates vbox layout, returns vbox
	def layout(self):
		lTitel = QLabel(
			text="Test för nivåbedömning i oktavband")	
		lInstruction = QLabel(
			text="Korrigera nivån i oktavbandet 4000 Hz")
		bIncrease = QPushButton(
			text="Ljudet upplevs otydligt/dovt \u25B2")
		bDecrease = QPushButton(
			text="Ljudet upplevs metalliskt/skarpt \u25BC")
		
		self.lTestInfo.setFont(QFont('Arial', 13))
		self.lTestInfo.setAlignment(Qt.AlignCenter)
		lInstruction.setFont(QFont('Arial', 11))
		lInstruction.setAlignment(Qt.AlignCenter)
		lTitel.setFont(QFont('Arial', 15))
		lTitel.setAlignment(Qt.AlignCenter)
		self.bTryOutStart.setFont(QFont('Arial', 13))
		self.bTestEnd.setFont(QFont('Arial', 13))
		self.bTestStart.setFont(QFont('Arial', 13))
		self.bTryOutEnd.setFont(QFont('Arial', 13))
		bIncrease.setFont(QFont('Arial', 13))
		bDecrease.setFont(QFont('Arial', 13))
		
		topBox = self.inputBoxLayout()
		vbox = QVBoxLayout()
		vbox.addWidget(lTitel)
		vbox.addWidget(topBox)
		vbox.addWidget(self.lTestInfo)
		vbox.addWidget(self.bTryOutStart)
		vbox.addWidget(self.bTryOutEnd)
		vbox.addWidget(self.bTestEnd)
		vbox.addWidget(self.bTestStart)
		vbox.addWidget(lInstruction)
		vbox.addWidget(bIncrease)
		vbox.addWidget(bDecrease)
		vbox.addSpacing(15)

		#Assigning functions to different buttons
		self.bBeginTesting.clicked.connect(self.beginTest)
		self.bEndTesting.clicked.connect(self.endTest)
		self.bTryOutStart.clicked.connect(self.tryOut)
		self.bTestEnd.clicked.connect(self.avslutaSpara)
		self.bTestStart.clicked.connect(self.newTest)
		self.bTryOutEnd.clicked.connect(self.displayResult)
		bIncrease.clicked.connect(self.increase)
		bDecrease.clicked.connect(self.decrease)
		return vbox
	
	#Adds all files from the folder with 
	#the same name as the playlistNumber to the playlist.
	#Folders added are located in the parent directory /Ljud 
	def loadPlaylist(self):
		self.currentPlaylist.clear()
		self.twoItemList.clear()
		folder = "Ljud/" + str(100 + self.playlistNumber) + "/"
		it = QDirIterator(folder, QDir.Files)
		
		while it.hasNext():
			it.next()
			self.currentPlaylist.addMedia(
				QMediaContent(QUrl.fromLocalFile(it.filePath())))
			print(it.filePath())

		if len(self.removeItem) == self.numberOfFiles:
			self.removeItem.clear()
			self.removeItem = self.removeItemsFromStart.copy()
		
		firstSentence = choice(
			[i for i in range(
			0,self.numberOfFiles) if i not in self.removeItem])
		print(firstSentence)
		self.removeItem.append(firstSentence)
		self.twoItemList.addMedia(self.currentPlaylist.media(firstSentence))
		self.player.setPlaylist(self.twoItemList)
		print(self.removeItem)

	#Before the test begins its possible to tryOut how it works
	def	tryOut(self):
		self.player.stop()
		self.playlistNumber = random.randint(
			self.playlistStartLow, self.playlistStartHigh)
		self.loadPlaylist()
		self.lTestInfo.setText("")
		self.indexLogg.clear()
		self.indexLogg.append(self.playlistNumber)
		self.player.play()
		self.bTryOutStart.hide()
		self.bTryOutEnd.show()

	#Begins the testing, checks that all input information is given
	#Changes all layout items
	#Creates a csv file with the input data and date + time as filename
	def beginTest(self):
		self.player.stop()

		if self.r1.isChecked():
			self.sex = "Man"
		elif self.r2.isChecked():
			self.sex = "Kvinna"
		elif self.r3.isChecked():
			self.sex = "EjAngivit"
		else:
			QMessageBox.about(
				self, "Viktigt", "Ange först kön och ålder")
			return
		
		age = self.age.text()
		if age == "":
			QMessageBox.about(
				self, "Viktigt", "Ange först kön och ålder")
			return
		
		self.bBeginTesting.hide()
		self.bEndTesting.show()
		self.lTestingOnline.show()
		self.lTestingOffline.hide()
		self.bTryOutStart.hide()
		self.bTryOutEnd.hide()
		self.bTestStart.show()
		self.lTestInfo.setText("")
		self.indexLogg.clear()
		self.playlistNumber = -1	

		now = datetime.now()
		dt_string = now.strftime("%Y%m%d%H%M%S")
		self.CSVfilename = dt_string + ".csv"
		
		with open(self.CSVfilename, 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([self.sex, age])

	#Ends the test, saves the data, resets all items and information
	def endTest(self):
		self.player.stop()

		self.bBeginTesting.show()
		self.bEndTesting.hide()
		self.lTestingOnline.hide()
		self.lTestingOffline.show()
		self.bTryOutStart.show()
		self.bTestStart.hide()
		self.bTestEnd.hide()
		self.removeItem.clear()
		self.removeItem = self.removeItemsFromStart.copy()
		self.lTestInfo.setText("")
		self.indexLogg.clear()
		self.currentPlaylist.clear()
		self.testNumber = 0
		self.lTestInfo.setText("")
		self.group.setExclusive(False)
		self.r1.setChecked(False)
		self.r2.setChecked(False)
		self.r3.setChecked(False)
		self.group.setExclusive(True)
		self.age.clear()
		self.playlistNumber = -1

	#Starts the next test
	#Loads a random playlist
	def newTest(self):
		if self.testNumber == 0:
			self.bTestEnd.show()
			
		self.playlistNumber = random.randint(
			self.playlistStartLow, self.playlistStartHigh)
		self.loadPlaylist()
		self.indexLogg.clear()
		self.indexLogg.append(self.playlistNumber)
		self.player.play()

		self.testNumber += 1
		self.lTestInfo.setText("Test: " + str(self.testNumber))
		self.bTestStart.hide()
		self.bTestEnd.show()
	
	#Ends Saves the test
	def avslutaSpara(self):
		self.player.stop()
		if self.indexLogg:
			decibel = [
				3*(x - self.orginalIndex) for x in self.indexLogg]
			with open(self.CSVfilename, 'a', newline='') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(decibel)
		self.indexLogg.clear()
		self.bTestStart.show()
		self.bTestEnd.hide()
		self.playlistNumber = -1

	#Displays the result in the program from the trying out test
	def displayResult(self):
		self.player.stop()
		decibel = [3*(x - self.orginalIndex) for x in self.indexLogg]
		indexLoggStr = ', '.join(str(y) for y in decibel)
		self.lTestInfo.setText("Resultat: " + indexLoggStr + " dB")
		self.bTryOutEnd.hide()
		self.bTryOutStart.show()
		self.playlistNumber = -1

	#Changes the current file in the playlist by -1
	def decrease(self):
		if self.playlistNumber > 0:
			self.player.stop()
			self.playlistNumber -=1
			self.loadPlaylist()
			self.indexLogg.append(self.playlistNumber)
			self.player.play()
		elif self.playlistNumber == 0:
			self.player.stop()
			self.loadPlaylist()
			self.indexLogg.append(self.playlistNumber)
			self.player.play()
		elif self.playlistNumber == -1:
			return
	
	#Changes the current file in the playlist by +1
	def increase(self):
		if self.playlistNumber < self.playlistNumberMax and self.playlistNumber != -1:
			self.player.stop()
			self.playlistNumber +=1
			self.loadPlaylist()
			self.indexLogg.append(self.playlistNumber)
			self.player.play()
		elif self.playlistNumber == self.playlistNumberMax:
			self.player.stop()
			self.loadPlaylist()
			self.indexLogg.append(self.playlistNumber)
			self.player.play()
		elif self.playlistNumber == -1:
			return

if __name__ == '__main__':
	app = QApplication(sys.argv)
	GUI = MainWindow()
	sys.exit(app.exec_())