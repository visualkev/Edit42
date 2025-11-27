#!/usr/bin/python

import json
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

from Edit42_win import edit42_win

#from initial_startup import initial_startup
appname="Edit 42"
appversion="0.1"

if __name__ == '__main__':
	app = QApplication([])
	data=None
	rect=app.primaryScreen().geometry()  #devicePixelRatio
	def load_conf():
		try:
			with open("./edit42.conf") as conf:
				data=json.load(conf)
		except:
			data=None
		return data
	appconf=load_conf()
		
	
	print("main: data", appconf)
	ed42_window = edit42_win(appname, appversion, appconf, rect)
	ed42_window.show()
	#print("++++++dpr:", ed42_window.devicePixelRatio())

	app.exec()
	
	
	
