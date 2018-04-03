"""
	Youtube video (or audio) downloader
		Just paste url and get the video!
"""


#from __future__ import unicode_literals # for porting and back-porting between Python 2 and Python 3
from PyQt4 import QtGui, QtCore
import sys
import ydDesign # python file containing design
import os

# modules needed for getting temperature data
import youtube_dl



# Helper classes
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

###########



# Main class
class ExampleApp(QtGui.QMainWindow, ydDesign.Ui_MainWindow):
	# used to integrate all thats in design.py with functions or code implemented here
		def __init__(self, parent=None):
			super(ExampleApp, self).__init__(parent)
			self.setupUi(self) # defined in ydDesign.py

			self.searchBtn.clicked.connect(self.enterPress)
			self.vid_aud.setChecked(True)


		def enterPress(self):
			# function to execute when the download ('Go!') button is pressed
			url = str(self.urlBox.text())
			if url != "":
				logger = MyLogger()
				logger.messageSignal.connect(self.statusBox.append)
				if self.aud_only.isChecked() == True: # download audio only
					ydl_opts = {'format':'140','logger': logger}
					self.thread = YoutubeDownload(url, ydl_opts)
					self.thread.start()

				elif self.vid_aud.isChecked() == True: # video + audio	
					# start by trying to download highest quality, then progressively lower quality till match found

					try:
						ydl_opts = {'format':'137+140','logger': logger}
						self.thread = YoutubeDownload(url, ydl_opts)
						self.thread.start()

					except:
						try:
							ydl_opts = {'format':'135+140','logger': logger}
							self.thread = YoutubeDownload(url, ydl_opts)
							self.thread.start()
						except:
							try:
								ydl_opts = {'format':'134+140','logger': logger}
								self.thread = YoutubeDownload(url, ydl_opts)
								self.thread.start()	
							except:
								try:
									ydl_opts = {'format':'133+140','logger': logger}
									self.thread = YoutubeDownload(url, ydl_opts)
									self.thread.start()
								except: # no corresponding format found, skip
									pass




def main():
	app = QtGui.QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()


if __name__ == '__main__':
	main()
