#!/usr/bin/python

import re, os, json
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QRadioButton,
	QLineEdit,
	QMessageBox,
	QFileDialog,
)

class setup_initial():
	def __init__(self,win):
		self.w42=win
		
		self.setup_initial()
		self.setup_states()
		

	def setup_states(self):
		radios=[self.w42.su_access1_btn, self.w42.su_access2_btn]
		if self.w42.su_access1_btn.isChecked():
			self.w42.su_host_txt.setReadOnly(False)
			self.w42.su_path_txt.setReadOnly(True)
		if self.w42.su_access2_btn.isChecked():
			self.w42.su_host_txt.setReadOnly(True)
			self.w42.su_path_txt.setReadOnly(False)	
		

	def setup_initial(self):
		print("setup")
		self.w42.su_vertL1 = QVBoxLayout(self.w42.setup_page)
		self.w42.su_question_lbl = QLabel(self.w42.setup_page)
		self.w42.su_question_lbl.setText("How would you like to access your config files?")
		self.w42.su_question_lbl.setMaximumSize(QSize(16777215, 43))
		self.w42.su_question_lbl.setBaseSize(QSize(0, 43))
		self.w42.su_question_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.w42.su_question_lbl.setPalette(self.w42.custom_palette)
		self.w42.su_vertL1.addWidget(self.w42.su_question_lbl)
		self.w42.su_access2_btn = QRadioButton(self.w42.setup_page)
		self.w42.su_access2_btn.setText("Direct, file system")
		self.w42.su_access2_btn.setMaximumSize(QSize(16777215, 43))
		self.w42.su_access2_btn.setStyleSheet("padding-left: 20px;")
		self.w42.su_access2_btn.setPalette(self.w42.custom_palette)
		self.w42.su_access2_btn.setChecked(True)
		self.w42.su_access2_btn.toggled.connect(self.on_radio_clicked)
		self.w42.su_vertL1.addWidget(self.w42.su_access2_btn)
		self.w42.su_hl_direct = QHBoxLayout()
		self.w42.su_path_lbl = QLabel(self.w42.setup_page)
		self.w42.su_path_lbl.setText("Path to your confs folder:")
		self.w42.su_path_lbl.setMaximumSize(QSize(16777215, 43))
		self.w42.su_path_lbl.setPalette(self.w42.custom_palette)
		self.w42.su_path_lbl.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
		self.w42.su_hl_direct.addWidget(self.w42.su_path_lbl)
		self.w42.su_path_txt = QLineEdit(self.w42.setup_page)
		#self.w42.su_path_txt.setStyleSheet("background-color:rgb(93, 65, 127)")
		self.w42.su_path_txt.setPalette(self.w42.custom_palette)
		self.w42.su_hl_direct.addWidget(self.w42.su_path_txt)
		self.w42.su_btn_filedialog = QPushButton(self.w42.setup_page)
		self.w42.su_btn_filedialog.setText("...")
		self.w42.su_btn_filedialog.setMinimumSize(QSize(30, 25))
		self.w42.su_btn_filedialog.setMaximumSize(QSize(30, 30))
		self.w42.su_btn_filedialog.setBaseSize(QSize(30, 25))
		self.w42.su_btn_filedialog.setPalette(self.w42.custom_palette)
		self.w42.su_hl_direct.addWidget(self.w42.su_btn_filedialog)
		self.w42.su_vertL1.addLayout(self.w42.su_hl_direct)
		self.w42.su_access1_btn = QRadioButton(self.w42.setup_page)
		self.w42.su_access1_btn.setText("API")
		self.w42.su_access1_btn.setMaximumSize(QSize(16777215, 43))
		self.w42.su_access1_btn.setStyleSheet("padding-left: 20px;")
		self.w42.su_access1_btn.setPalette(self.w42.custom_palette)
		self.w42.su_access1_btn.setPalette(self.w42.custom_palette)
		self.w42.su_access1_btn.setChecked(False)
		self.w42.su_access1_btn.toggled.connect(self.on_radio_clicked)
		self.w42.su_vertL1.addWidget(self.w42.su_access1_btn)
		self.w42.su_hl_api = QHBoxLayout()
		self.w42.su_host_lbl = QLabel(self.w42.setup_page)
		self.w42.su_host_lbl.setText("Host Address:")
		self.w42.su_host_lbl.setMaximumSize(QSize(16777215, 43))
		self.w42.su_host_lbl.setPalette(self.w42.custom_palette)
		self.w42.su_host_lbl.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
		self.w42.su_hl_api.addWidget(self.w42.su_host_lbl)
		self.w42.su_host_txt = QLineEdit(self.w42.setup_page)
		self.w42.su_host_txt.setText("http://localhost:4242")
		#self.w42.su_host_txt.setStyleSheet("background-color:rgb(93, 65, 127)")
		self.w42.su_hl_api.addWidget(self.w42.su_host_txt)
		self.w42.su_vertL1.addLayout(self.w42.su_hl_api)
		self.w42.su_btn_continue = QPushButton(self.w42.setup_page)
		self.w42.su_btn_continue.setText("Continue")
		self.w42.su_btn_continue.setPalette(self.w42.custom_palette)
		self.w42.su_vertL1.addWidget(self.w42.su_btn_continue)
		self.w42.su_btn_continue.clicked.connect(self.on_continue_clicked)
		QWidget.setTabOrder(self.w42.su_access2_btn, self.w42.su_path_txt)
		QWidget.setTabOrder(self.w42.su_path_txt, self.w42.su_btn_filedialog)
		QWidget.setTabOrder(self.w42.su_btn_filedialog, self.w42.su_access1_btn)
		QWidget.setTabOrder(self.w42.su_access1_btn, self.w42.su_host_txt)
		QWidget.setTabOrder(self.w42.su_host_txt, self.w42.su_btn_continue)
		self.w42.su_btn_filedialog.clicked.connect(self.on_click_filedialog)
		
	def on_click_filedialog(self):
		file=QFileDialog()
		file.setFileMode(QFileDialog.FileMode.Directory)
		file.setOptions(QFileDialog.Option.ShowDirsOnly)
		if file.exec():
			theDir = file.selectedFiles()
			self.w42.su_path_txt.setText(theDir[0])
			
		
	def on_radio_clicked(self):
		print("toggled")
		self.setup_states()
		
	def on_continue_clicked(self):
		print("clicked")
		if self.w42.su_access1_btn.isChecked():
			d=self.w42.su_host_txt.text()
			print(d)
			if re.search(r'[Hh][Tt]{2}[Pp][Ss]?:\/\/((\w+[\.-]*)*\w+|(\d{1,3}\.){3}\d{1,3}):\d{3,}', d) is not None:
				print("good")
				self.save_confs({'api': d})
			
		elif self.w42.su_access2_btn.isChecked():
			d=self.w42.su_path_txt.text()
			print(d)
			print(" path" , os.path.exists(d))
			if os.path.exists(d):
				self.save_confs({'file': d})
			else:
				msgBox = QMessageBox()
				msgBox.setIcon(QMessageBox.Icon.Warning)
				msgBox.setWindowTitle("Edit42 - Path not found")
				msgBox.setText(f"{d} Was not found.")
				msgBox.exec()
	
	def save_confs(self, data):
		with open ("./edit42.conf", "w") as conf:
			json.dump(data, conf)
		self.w42.appconf=data
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Icon.Information)
		msgBox.setWindowTitle("Edit42 - Conf created")
		msgBox.setText(f"Edit42 conf has been created.")
		msgBox.exec()
		self.w42.edit42_stack.setCurrentIndex(1)
		
		
			
		
