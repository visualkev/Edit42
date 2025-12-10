#!/usr/bin/python

from PySide6.QtCore import QSize, Qt, QTimer, QRect
from PySide6.QtGui import (
	QAction, 
	QIcon, 
	QKeySequence, 
	QFont, 
	QTextCursor, 
	QColor,
	QTextFormat, 
	QScreen)
from PySide6.QtWidgets import (
    QApplication,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QCheckBox,
    QLabel,
    QPushButton,
    QRadioButton,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QComboBox,
    QPlainTextEdit,
    QTextEdit,
    QMenu,
    QLineEdit,
    QMessageBox,
    QFileDialog
)
from Edit42 import edit42
from custom_palette import custom_palette
from do_insert_form import Insert_form


dgrey="\033[30;48m"
red="\033[31;48m"
green="\033[32;48m"
yel="\033[33;48m"
blue="\033[34;48m"
vio="\033[35;48m"
lblue="\033[36;48m"
lgrey="\033[37;48m"
nc="\033[0m"


class edit42_win(QMainWindow):
	def __init__(self, appname, appversion, data, rect):
		super().__init__()
		self.appname=appname
		icon=QIcon('./application42icon32.png')
		self.setWindowTitle(appname)
		self.setWindowIcon(icon)
		self.win_width=770
		self.screen_rect=rect
		self.set_wingeom()
		self.appversion=appversion
		self.appconf=data
		self.last_search_cursor=None
		self.appclass42=None
		self.setup_stack()
		self.custom_palette=custom_palette()
		self.setPalette(self.custom_palette)
		self.setup_part1()
		print("init win")
		self.previous_page=self.edit42_stack.currentIndex()

		
		if self.appconf is None:
			self.setup_initial()
			self.edit42_stack.setCurrentIndex(0)			
		else:
			
			self.edit42_stack.setCurrentIndex(1)
		
		
	

	def set_wingeom(self):
		screen_width=self.screen_rect.width()
		screen_height=self.screen_rect.height()
		self.win_height=int(screen_height*.9)
		x=int((screen_width - self.win_width)/2)
		self.setGeometry(x, 30, self.win_width, self.win_height)
		
	def do_insert(self):
		self.insert_form.setup(self.insert_list.currentText())
		self.edit42_stack.setCurrentIndex(2)

	def setup_initial(self):
		from setup_initial import setup_initial
		self.setup_setup=setup_initial(self)

	def setup_stack(self):
		self.setup_page= QWidget()
		self.editor_page= QWidget()
		self.insert_page= QWidget()
		self.advanced_page= QWidget()
		self.edit42_stack = QStackedWidget()
		self.edit42_stack.addWidget(self.setup_page)
		self.edit42_stack.addWidget(self.editor_page)
		self.edit42_stack.addWidget(self.insert_page)
		self.edit42_stack.addWidget(self.advanced_page)
		self.edit42_stack.currentChanged.connect(self.on_changed_stack)
		self.layout42 = QVBoxLayout()        
		self.layout42.addWidget(self.edit42_stack)
		self.setLayout(self.layout42)
		self.setCentralWidget(self.edit42_stack)
		
		
	def setup_part1(self):
		self.currentLineNumber=None
		self.currentLineColor = QColor("#5D417F")
		
		#self.setFont(self.mainfont)
		self.setMinimumSize(QSize(650, 400))#1a053a
		self.setBaseSize(QSize(750, 900))
		#self.setStyleSheet('color: "#32fbe2"; background-color:"#1a053a"; selection-color: rgb(255, 255, 255); selection-background-color: "#5e5c64"; font: 16px Tahoma, sans-serif;')
		self.setStyleSheet('font: 16px Tahoma, sans-serif;')
		
	def setup_part2(self):
		print("setup part2")
		self.setup_actions()
		self.setup_menubar()
		self.setup_comboboxes()
		self.setup_toolbar()
		self.setup_editbox()
		self.statusbar42=QStatusBar(self)
		self.setStatusBar(self.statusbar42)
		self.statusbar42.setPalette(self.custom_palette)
		statuslbl_style='color: "#bfb6cd"; padding: 5px;'
		self.statusJ_lbl=QPushButton(self, text="Json: --")
		self.statusJ_lbl.setStyleSheet('color: "#bfb6cd"; background-color: "#442b69"; font-weight: bold;')
		self.statusS_lbl=QLabel(self, text="<b>Schema</b>: --")
		self.statusS_lbl.setStyleSheet(statuslbl_style)
		self.statusS_lbl.setWordWrap(False)
		self.statusBar().addPermanentWidget(self.statusJ_lbl)
		self.statusBar().addPermanentWidget(self.statusS_lbl)
		self.list2top=QTimer(self)
		self.list2top.setInterval(1000)
		self.list2top.setSingleShot(True)
		
		
	def setup_editbox(self):
		self.vertmain=QVBoxLayout(self.editor_page)
		self.editbox = QPlainTextEdit(self.editor_page)
		self.vertmain.addWidget(self.editbox)
		self.editbox.setStyleSheet('color: "#decce5"; background-color: #382b52; font: 18px Tahoma, sans-serif;')
		#self.editbox.setPalette(self.custom_palette)
		
	
	def setup_actions(self):
		self.open_action = QAction("&Open", self)
		self.open_action.setStatusTip("Click to open")
		self.open_action.triggered.connect(self.on_open_button_clicked)
		self.open_action.setShortcut(QKeySequence.Open)
		
		self.save_action = QAction("&Save", self)
		self.save_action.setStatusTip("Click to save")
		self.save_action.triggered.connect(self.on_save_button_clicked)
		self.save_action.setShortcut(QKeySequence.Save)
		
		self.quit_action = QAction("&Quit", self)
		self.quit_action.setStatusTip("Click to quit")
		self.quit_action.triggered.connect(self.on_quit_action)
		self.quit_action.setShortcut(QKeySequence.Quit)
		
		self.new_action=QAction("&New Station", self)
		self.new_action.setStatusTip("Create new Station")
		self.new_action.setShortcut(QKeySequence.New)
		
	def setup_menubar(self):
		menu = self.menuBar()
		menu.setPalette(self.custom_palette)
		file_menu = menu.addMenu("&File")
		file_menu.addAction(self.open_action)
		file_menu.addAction(self.new_action)
		file_menu.addAction(self.save_action)
		file_menu.addSeparator()
		file_menu.addAction(self.quit_action)


	def setup_comboboxes(self):
		qsize_min=QSize(150, 30)
		qsize_max=QSize(250, 40)
		qsize_base=QSize(150, 30)
		combo_style='margin: 3px; padding:1px;'
		self.chan_listbox=QComboBox(self.editor_page)
		self.override_indexes_listbox=QComboBox(self.editor_page)
		self.daytemp_indexes_listbox=QComboBox(self.editor_page)
		self.indexes_listbox=QComboBox(self.editor_page)
		
		self.chan_listbox.setStyleSheet(combo_style)
		self.chan_listbox.setPalette(self.custom_palette)
		self.chan_listbox.setMinimumSize(qsize_min)
		self.chan_listbox.setMaximumSize(qsize_max)
		self.chan_listbox.setBaseSize(qsize_base)
		self.chan_listbox.setStatusTip("Channels Configured")
				
		self.override_indexes_listbox.setStyleSheet(combo_style)
		self.override_indexes_listbox.setPalette(self.custom_palette)
		self.override_indexes_listbox.setMinimumSize(qsize_min)
		self.override_indexes_listbox.setMaximumSize(qsize_max)
		self.override_indexes_listbox.setBaseSize(qsize_base)
		self.override_indexes_listbox.setStatusTip("Slot Overrides Configured")
		
		self.daytemp_indexes_listbox.setStyleSheet(combo_style)
		self.daytemp_indexes_listbox.setPalette(self.custom_palette)
		self.daytemp_indexes_listbox.setMinimumSize(qsize_min)
		self.daytemp_indexes_listbox.setMaximumSize(qsize_max)
		self.daytemp_indexes_listbox.setBaseSize(qsize_base)
		self.daytemp_indexes_listbox.setStatusTip("Day Templates Configured")
		
		self.indexes_listbox.setStyleSheet(combo_style)
		self.indexes_listbox.setPalette(self.custom_palette)
		self.indexes_listbox.setMinimumSize(qsize_min)
		self.indexes_listbox.setMaximumSize(qsize_max)
		self.indexes_listbox.setBaseSize(qsize_base)
		#self.indexes_listbox.setFont(self.mainfont)
		self.indexes_listbox.setStatusTip("Other Config and Days")
	
	def setup_event_slots(self):
		print("setup events")
		self.indexes_listbox.currentIndexChanged.connect(self.on_index_changed)
		self.daytemp_indexes_listbox.currentIndexChanged.connect(self.on_daytemp_changed)
		self.override_indexes_listbox.currentIndexChanged.connect(self.on_override_changed)
		self.chan_listbox.currentIndexChanged.connect(self.on_chan_changed)
		self.editbox.cursorPositionChanged.connect(self.on_position_changed_editbox)
		self.editbox.textChanged.connect(self.on_text_changed_editbox)
		self.insert_list.currentIndexChanged.connect(self.on_insert_select)
		self.statusBar().showMessage("Ready", 5000)
		

	def disconnect_event_slots(self):
		self.indexes_listbox.currentIndexChanged.disconnect()
		self.daytemp_indexes_listbox.currentIndexChanged.disconnect()
		self.override_indexes_listbox.currentIndexChanged.disconnect()
		self.chan_listbox.currentIndexChanged.disconnect()
		self.editbox.cursorPositionChanged.disconnect()
		self.editbox.textChanged.disconnect()
		self.insert_list.currentIndexChanged.disconnect()

	def setup_toolbar(self):
		searchbox_style='color: "#decce5"; background-color: "#382b52"; margin: 1px 5px; padding: 1px;'
		self.toolbar = QToolBar("Primary toolbar")
		self.toolbar.setPalette(self.custom_palette)
		self.toolbar2= QToolBar("Secondary toolbar")
		self.toolbar2.setPalette(self.custom_palette)
		self.addToolBar(self.toolbar)
		self.addToolBarBreak()
		self.addToolBar(self.toolbar2)
		self.toolbar.setIconSize(QSize(32, 32))
		self.toolbar.addAction(self.save_action)
		toolButton = self.toolbar.widgetForAction(self.save_action)
		toolButton.setStyleSheet('color: "#decce5"; background-color: #382b52;')
		
		self.insert_list=QComboBox(self.editor_page)
		self.insert_list.setStatusTip("Insert Objects")
		insertlist=['Insert...', 'Day Template', 'Slot Override', 'Tag Override'] #, 'Time Slot']
		self.insert_list.clear()
		self.insert_list.addItems(insertlist)
		self.insert_list.setPalette(self.custom_palette)
		self.toolbar.addWidget(self.insert_list)
		
		self.toolbar2.addWidget(self.chan_listbox)
		self.toolbar2.addWidget(self.override_indexes_listbox)
		self.toolbar2.addWidget(self.daytemp_indexes_listbox)
		self.toolbar2.addWidget(self.indexes_listbox)
		self.searchbox=QLineEdit(self.editor_page)
		self.searchbox.textChanged.connect(self.on_search_txt)
		self.searchbox.returnPressed.connect(self.on_searchbox_enterkey)
		self.searchbox.editingFinished.connect(self.on_searchbox_click)
		self.searchbox.setStatusTip("Search for Text")
		self.searchbox.setPalette(self.custom_palette)
		self.searchbox.setClearButtonEnabled(True)
		self.toolbar2.addWidget(self.searchbox)

################################################################################
###########################----- Callbacks -----################################
################################################################################
	def on_position_changed_editbox(self):
		self.highlightCurrentLine(self.editbox)

	def on_searchbox_click(self):
		self.searchbox.selectAll()

	def on_search_txt(self):
		self.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		if self.editbox.find(self.searchbox.text()):
			self.editbox.centerCursor()
			self.last_search_cursor=self.editbox.textCursor()

	def on_quit_action(self):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Icon.Warning)
		msgBox.setWindowTitle(self.appclass42.app_name)
		msgBox.setText("The document has been modified.")
		msgBox.setInformativeText("Do you want to save your changes?")
		msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.StandardButton.Cancel)
		msgBox.setDefaultButton(QMessageBox.Save)
		
		if self.appclass42.is_changed:
			print("unsaved changes")
			ret = msgBox.exec()
			if ret == QMessageBox.Save:
				self.on_save_button_clicked()
				self.close()
			elif ret == QMessageBox.Discard:
				self.close()
			
			elif ret == QMessageBox.StandardButton.Cancel:
				# Cancel was clicked
				return
			else:
				# should never be reached
				return
		else:
			self.close()

	def on_searchbox_enterkey(self):
		print("Enter")
		if self.editbox.find(self.searchbox.text()):
			self.editbox.centerCursor()
			self.last_search_cursor=self.editbox.textCursor()

	def on_insert_select(self):
		self.list2top.timeout.connect(self.reset_text3)
		self.list2top.start()
		self.do_insert()
		

	def highlightCurrentLine(self, thebox):
		newCurrentLineNumber = thebox.textCursor().blockNumber()
		if newCurrentLineNumber != self.currentLineNumber:                
			self.currentLineNumber = newCurrentLineNumber
			hi_selection = QTextEdit.ExtraSelection() 
			hi_selection.format.setBackground(self.currentLineColor)
			hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			hi_selection.cursor = thebox.textCursor()
			hi_selection.cursor.clearSelection() 
			thebox.setExtraSelections([hi_selection])    
	
	
	def on_text_changed_editbox(self):
		print("Changed!")
		self.appclass42.check_content_change()

	def on_save_button_clicked(self):
		print("click save")
		self.appclass42.do_save()

	def on_open_button_clicked(self, s):
		print("click", s)
		self.appclass42.open_cfg()

	def on_index_changed(self, s):
		self.list2top.timeout.connect(self.reset_text)
		self.list2top.start()
		print(f"indexes clicked {s} {self.indexes_listbox.currentText()}")
		
		if 'Now Slot'==self.indexes_listbox.currentText():
			self.appclass42.hili_now_slot()
			return
		self.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		if self.editbox.find(self.indexes_listbox.currentText()):
			self.editbox.centerCursor()
			self.qts=self.editbox.textCursor()
			
		
	def reset_text(self):
		self.indexes_listbox.currentIndexChanged.disconnect()
		self.indexes_listbox.setCurrentIndex(0)
		self.indexes_listbox.currentIndexChanged.connect(self.on_index_changed)
	def reset_text1(self):
		self.daytemp_indexes_listbox.currentIndexChanged.disconnect()
		self.daytemp_indexes_listbox.setCurrentIndex(0)
		self.daytemp_indexes_listbox.currentIndexChanged.connect(self.on_daytemp_changed)
	def reset_text2(self):
		self.override_indexes_listbox.currentIndexChanged.disconnect()
		self.override_indexes_listbox.setCurrentIndex(0)
		self.override_indexes_listbox.currentIndexChanged.connect(self.on_override_changed)
	def reset_text3(self):
		
		self.insert_list.currentIndexChanged.disconnect()
		self.insert_list.setCurrentIndex(0)
		self.insert_list.currentIndexChanged.connect(self.on_insert_select)
		
	def on_daytemp_changed(self, s):
		self.list2top.timeout.connect(self.reset_text1)
		self.list2top.start()
		print(f"daytemp clicked {s} {self.daytemp_indexes_listbox.currentText()}")
		self.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		if self.editbox.find(self.daytemp_indexes_listbox.currentText()):
			self.editbox.centerCursor()
			self.qts=self.editbox.textCursor()
			print("found it")
			
	def on_override_changed(self, s):
		self.list2top.timeout.connect(self.reset_text2)
		self.list2top.start()
		print(f"override clicked {s} {self.override_indexes_listbox.currentText()}")
		self.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		if self.editbox.find(self.override_indexes_listbox.currentText()):
			self.editbox.centerCursor()
			self.qts=self.editbox.textCursor()
			print("found it")

	def on_chan_changed(self, s):
		print(f"chan clicked {s} {self.chan_listbox.currentText()}")
		self.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		self.appclass42.switch_channel_data(self.chan_listbox.currentText())


################################################################################
######################----- Callbacks   -----------########################
################################################################################	
		
	def on_changed_stack(self,index):
		print("+-+-+-+-+-+-CCHanged from", self.previous_page, "to", index)
		#return
		if index==1:
			
			if self.previous_page==2:
				print("already initialized", self.previous_page)
				self.toolbar.show()
				self.toolbar2.show()
				self.statusJ_lbl.clicked.connect(self.appclass42.mark_error_pos)
				
			elif self.previous_page==0:
				print("initialize", index)
				self.appclass42=edit42(self.appname, self.appversion, self.appconf)
				self.setup_part2()
				self.appclass42.initialize_win(self)
				self.toolbar.show()
				self.toolbar2.show()
				self.statusJ_lbl.clicked.connect(self.appclass42.mark_error_pos)
				self.appclass42.open_cfg()
				self.appclass42.configs.make_backup()
				self.insert_form=Insert_form(self.appclass42, self)
				self.editbox.setFocus()
				
		if index==2:
			self.statusJ_lbl.clicked.connect(self.insert_form.mark_error_pos)
			self.toolbar.hide()
			self.toolbar2.hide()
		self.previous_page=index
		











