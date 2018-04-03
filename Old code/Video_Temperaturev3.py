from __future__ import unicode_literals
import sys
from PyQt4 import QtGui, QtCore
import youtube_dl
x = ''
#x = 'Hi!'
# Youtube Downloader logger
"""
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
"""
def refresh_text_box(self,MYSTRING): 
    GUI.e2.append(x) #append string
    QtGui.QApplication.processEvents() #update gui for pyqt

class MyLogger(QtCore.QObject):
	messageSignal = QtCore.pyqtSignal(str)



	def debug(self, msg):
		self.messageSignal.emit(msg)

	def warning(self, msg):
		self.messageSignal.emit(msg)

	def error(self, msg):
		self.messageSignal.emit(msg)
    



class YoutubeDownload(QtCore.QThread):
	def __init__(self, url, ydl_opts, *args, **kwargs):
		QtCore.QThread.__init__(self, *args, **kwargs)
		self.url = url
		self.ydl_opts = ydl_opts

	def run(self):
		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			ydl.download([self.url])

    


class Window(QtGui.QMainWindow): # inherit all aspects of the object

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__() # super returns the parent object
		self.setGeometry(50, 50, 1500, 500) # left, top, width, height
		self.setWindowTitle("What You Want!")
		self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

		extractAction = QtGui.QAction("&Do Nothing!!", self) # Label for the menu object
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip('Leave the App') # status tip info msg
		extractAction.triggered.connect(self.close_application)

		mainMenu = self.menuBar() # create menuBar object
		fileMenu = mainMenu.addMenu('&File') # add a file menu object to menubar
		fileMenu.addAction(extractAction) #add menu item created earlier


		self.home()


	def home(self):
		btn = QtGui.QPushButton("Quit", self) # button object with "quit" text
		btn.clicked.connect(self.close_application) # custom function definition
		btn.resize(btn.minimumSizeHint()) #sizeHint code will return what QT thinks is the best side for your button
		btn.move(0,100)
		""" add check boxes for format (video+audio,audio)
		self.audioOnlyCheck = QtGui.QCheckBox('Audio only', self)
		self.audioOnlyCheck.move(200,25)
		"""

		# radio buttons
		#layout = QtGui.QHBoxLayout()
		self.b1 = QtGui.QRadioButton("Video+Audio")
		self.b1.setChecked(True)
		#layout.addWidget(self.b1)

		self.b2 = QtGui.QRadioButton("Audio Only")
		#layout.addWidget(self.b2)
		#self.setLayout(layout)


		flo = QtGui.QFormLayout()

		self.e1 = QtGui.QLineEdit()
		self.e2 = QtGui.QTextEdit()
		self.e2.setText(x)
		#self.e2 = QtGui.QTextEdit()
		self.e2.setReadOnly(True)
		#self.e1.editingFinished.connect(self.enterPress)
		flo.addRow("Video URL:",self.e1)
		flo.addRow("Status of download:", self.e2)
		flo.addWidget(self.b1)
		flo.addWidget(self.b2)

		win = QtGui.QWidget(self)
		win.setLayout(flo)
		win.move(50,150)
		win.resize(1200,1200)
		win.show()

		# add push button for start video of download
		self.startVideoButton = QtGui.QPushButton("Start Download", self)
		self.startVideoButton.clicked.connect(self.enterPress)
		self.startVideoButton.move(400,400)
		# add text box which displays the status of download


		self.show()


	def enterPress(self):
		url = str(self.e1.text())
		if url != "":
			logger = MyLogger()
			logger.messageSignal.connect(self.e2.append)
			ydl_opts = {'format':'140','logger': logger}
			self.thread = YoutubeDownload(url, ydl_opts)
			self.thread.start()


	"""
	def enterPress(self):
		url = str(self.e1.text())
		#ydl_opts = {'listformats':'-F'}
		if self.b2.isChecked() == True:
			ydl_opts = {'format':'140','logger':MyLogger()}
			#ydl_opts = {'format':'140','progress_hooks': [my_hook]}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
				#ydl._write_string('Hi!',out=GUI.e2.setText())
				#text = str(ydl.download([url]))
				#self.e2.setText(text)

		elif self.b1.isChecked() == True:
			try:
			#ydl_opts = {'listformats':'-F'}
				ydl_opts = {'format':'137+140'}
				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([url])
			except:
				try:
					ydl_opts = {'format':'135+140'}
					with youtube_dl.YoutubeDL(ydl_opts) as ydl:
						ydl.download([url])

				except:
					try:
						ydl_opts = {'format':'134+140'}
						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download([url])
					except:
						ydl_opts = {'format':'133+140'}
						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							ydl.download([url])

		"""




	def close_application(self):
		# Pop up
	    choice = QtGui.QMessageBox.question(self, 'Extract!',
	                                        "Get into the chopper?",
	                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
	    if choice == QtGui.QMessageBox.Yes:
	        print("Extracting Naaaaaaoooww!!!!")
	        self.close()
	        sys.exit()
	    else:
	        pass



#GUI = Window(
#def run():
app = QtGui.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())

#run()