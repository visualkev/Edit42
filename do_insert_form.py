#!/usr/bin/python

import json
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QTextCharFormat , QColor, QTextCursor
from PySide6.QtWidgets import (
	QSizePolicy,
	QVBoxLayout,
	QHBoxLayout,
	QComboBox,
	QPlainTextEdit,
	QLabel,
	QPushButton,
	QCheckBox,
	QLineEdit
	)
	
from json_valid import json_valid
from Highlighter import Highlighter	
	
class Insert_form():
	def __init__(self, ac42, ac42_win):
		self.appclass42=ac42
		self.w42=ac42_win
		self.create=None
		#self.snipps_obj={'slot_overrides': {}, 'day_templates': {}}
		self.snipps_obj={}
		self.do_setup()
		self.valid_json=json_valid()
		self._highlighter = Highlighter()
	
	def setup(self, start):
		self.get_snipp_data()
		self.merge_lists()

		self.insert=start
		self.w42.ip_name_lbl.setText(f"{start} Name:")
		
		self.setup_status_tips(self.insert)
		
		
		self.setup_highlight_rules()
		self.w42.ip_list_of.clear()
		
		if self.insert=='Slot Override':
			if self.mso:

				self.w42.ip_list_of.addItems(self.mso)
				self.w42.ip_list_of.insertItem(0, "Select Override")
				self.w42.ip_list_of.setCurrentText("Select Override")
			else:
				self.w42.ip_fr_new_chk.setChecked(True)
		elif self.insert=='Day Template':
			if self.mdt:

				self.w42.ip_list_of.addItems(self.mdt)
				self.w42.ip_list_of.insertItem(0, "Select Template")
				self.w42.ip_list_of.setCurrentText("Select Template")
			else:
				self.w42.ip_fr_new_chk.setChecked(True)
#			elif self.w42.insert=='Time Slot':
#				for h in range(24):
#					day_template
		self.setup_events()		
	
	def do_setup(self):
		
		self.w42.ip_vertl3 = QVBoxLayout(self.w42.insert_page)
		self.w42.ip_vertl1= QVBoxLayout()
		self.w42.ip_hl_row1 = QHBoxLayout()

		self.w42.ip_name_lbl = QLabel(self.w42.insert_page)
		self.w42.ip_name_lbl.setText("Name:")
		self.w42.ip_name_lbl.setMaximumSize(QSize(250, 43))
		self.w42.ip_name_lbl.setStyleSheet("padding: 5px;")
		self.w42.ip_name_lbl.setPalette(self.w42.custom_palette)
		self.w42.ip_name_lbl.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
		self.w42.ip_hl_row1.addWidget(self.w42.ip_name_lbl)

		self.w42.ip_txtName = QLineEdit(self.w42.insert_page)
		self.w42.ip_txtName.setText("Text")
		self.w42.ip_txtName.setMinimumSize(QSize(300, 30))
		self.w42.ip_txtName.setMaximumSize(QSize(350, 50))
		self.w42.ip_txtName.setBaseSize(QSize(320, 35))
		self.w42.ip_txtName.setStyleSheet('padding: 5px; ')
		self.w42.ip_txtName.setPalette(self.w42.custom_palette)
		self.w42.ip_txtName.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.w42.ip_hl_row1.addWidget(self.w42.ip_txtName)
		self.w42.ip_vertl1.addLayout(self.w42.ip_hl_row1)
		self.w42.ip_horizl3 = QHBoxLayout()

		self.w42.ip_btn_save_snipp = QPushButton(self.w42.insert_page)
		self.w42.ip_btn_save_snipp.setText("Save Item for reuse")
		self.w42.ip_btn_save_snipp.setMaximumSize(QSize(200, 16777215))
		self.w42.ip_btn_save_snipp.setStyleSheet("padding: 5px;")
		self.w42.ip_btn_save_snipp.setPalette(self.w42.custom_palette)
		self.w42.ip_horizl3.addWidget(self.w42.ip_btn_save_snipp)

		self.w42.ip_fr_new_chk = QCheckBox(self.w42.insert_page)
		self.w42.ip_fr_new_chk.setText("Create from New")
		sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.w42.ip_fr_new_chk.sizePolicy().hasHeightForWidth())
		self.w42.ip_fr_new_chk.setSizePolicy(sizePolicy)
		self.w42.ip_fr_new_chk.setMinimumSize(QSize(150, 30))
		self.w42.ip_fr_new_chk.setMaximumSize(QSize(300, 50))
		self.w42.ip_fr_new_chk.setBaseSize(QSize(155, 43))
		self.w42.ip_fr_new_chk.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
		self.w42.ip_fr_new_chk.setAutoFillBackground(False)
		#self.w42.ip_fr_new_chk.setStyleSheet(u"padding: 5px;")
		self.w42.ip_fr_new_chk.setPalette(self.w42.custom_palette)
		self.w42.ip_horizl3.addWidget(self.w42.ip_fr_new_chk)
		self.w42.ip_vertl1.addLayout(self.w42.ip_horizl3)
		self.w42.ip_horizl2 = QHBoxLayout()

		self.w42.ip_copyfr_lbl = QLabel(self.w42.insert_page)
		self.w42.ip_copyfr_lbl.setText("Copy From:")
		sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		sizePolicy1.setHorizontalStretch(0)
		sizePolicy1.setVerticalStretch(0)
		sizePolicy1.setHeightForWidth(self.w42.ip_copyfr_lbl.sizePolicy().hasHeightForWidth())
		#self.w42.ip_copyfr_lbl.setSizePolicy(sizePolicy1)
		self.w42.ip_copyfr_lbl.setPalette(self.w42.custom_palette)
		self.w42.ip_copyfr_lbl.setMaximumSize(QSize(170, 43))
		#self.w42.ip_copyfr_lbl.setStyleSheet(u"padding: 5px")
		self.w42.ip_copyfr_lbl.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
		self.w42.ip_horizl2.addWidget(self.w42.ip_copyfr_lbl)

		self.w42.ip_list_of = QComboBox(self.w42.insert_page)
		sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
		sizePolicy2.setHorizontalStretch(0)
		sizePolicy2.setVerticalStretch(0)
		sizePolicy2.setHeightForWidth(self.w42.ip_list_of.sizePolicy().hasHeightForWidth())
		self.w42.ip_list_of.setSizePolicy(sizePolicy2)
		self.w42.ip_list_of.setMinimumSize(QSize(0, 30))
		self.w42.ip_list_of.setMaximumSize(QSize(300, 16777215))
		self.w42.ip_list_of.setStyleSheet("padding: 5px;")
		self.w42.ip_list_of.setPalette(self.w42.custom_palette)
		self.w42.ip_horizl2.addWidget(self.w42.ip_list_of)
		self.w42.ip_vertl1.addLayout(self.w42.ip_horizl2)
		self.w42.ip_vertl3.addLayout(self.w42.ip_vertl1)

		self.w42.ip_insert_preview = QPlainTextEdit(self.w42.insert_page)
		self.w42.ip_insert_preview.setEnabled(True)
		self.w42.ip_insert_preview.setStyleSheet('color: "#decce5"; background-color: "#382b52"; font: 18px Tahoma, sans-serif;')
		#self.w42.ip_insert_preview.setPalette(self.w42.custom_palette)
		self.w42.ip_insert_preview.setTabStopDistance(4.000000000000000)
		self.w42.ip_vertl3.addWidget(self.w42.ip_insert_preview)
		self.w42.ip_horizl_buttons=QHBoxLayout()

		self.w42.ip_btn_insert = QPushButton(self.w42.insert_page)
		self.w42.ip_btn_insert.setText("Insert")
		self.w42.ip_btn_insert.setPalette(self.w42.custom_palette)
		self.w42.ip_btn_cancel = QPushButton(self.w42.insert_page)
		self.w42.ip_btn_cancel.setText("Cancel")
		self.w42.ip_btn_cancel.setPalette(self.w42.custom_palette)
		self.w42.ip_btn_cancel.clicked.connect(self.on_cancel_click)
		self.w42.ip_horizl_buttons.addWidget(self.w42.ip_btn_cancel)
		self.w42.ip_horizl_buttons.addWidget(self.w42.ip_btn_insert)
		self.w42.ip_vertl3.addLayout(self.w42.ip_horizl_buttons)
			
	def on_cancel_click(self):
		print("cancel")
		self.w42.edit42_stack.setCurrentIndex(1)

	def merge_lists(self):
		self.mso={}
		self.mdt={}
		if 'slot_overrides' in self.appclass42.chan_data:
			self.mso.update(self.appclass42.chan_data['slot_overrides'])
		if 'slot_overrides' in self.snipps_obj: 
			self.mso.update(self.snipps_obj['slot_overrides'])
		if 'day_templates' in self.appclass42.chan_data:
			self.mdt.update(self.appclass42.chan_data['day_templates'])
		if 'day_templates' in self.snipps_obj:
			self.mdt.update(self.snipps_obj['day_templates'])
		
	def setup_events(self):
		print("setup events")
		self.w42.ip_btn_insert.clicked.connect(self.on_btn_insert)
		self.w42.ip_btn_cancel.clicked.connect(self.on_btn_cancel)
		self.w42.ip_list_of.currentIndexChanged.connect(self.on_list_chg)
		self.w42.ip_fr_new_chk.stateChanged.connect(self.on_check_chg)
		self.w42.ip_txtName.returnPressed.connect(self.on_return_pressed)
		self.w42.ip_btn_save_snipp.clicked.connect(self.on_btn_snipp_save)
		self.w42.ip_insert_preview.textChanged.connect(self.on_text_changed)
	
	def disable_events(self):
		print("disable events")
		self.w42.ip_btn_insert.clicked.disconnect()
		self.w42.ip_btn_cancel.clicked.disconnect()
		self.w42.ip_list_of.currentIndexChanged.disconnect()
		self.w42.ip_fr_new_chk.stateChanged.disconnect()
		self.w42.ip_txtName.returnPressed.disconnect()
		self.w42.ip_btn_save_snipp.clicked.disconnect()
		self.w42.ip_insert_preview.textChanged.disconnect()
	
	def setup_status_tips(self, item):
		if 'Slot Override'==item:
			nnote='. All options are shown. You must edit'
		else: nnote=''
		item=item.casefold()
		station_name=self.appclass42.chan_data['network_name']
		self.w42.ip_btn_save_snipp.setStatusTip(f"Click to save your new {item}")
		self.w42.ip_txtName.setStatusTip(f"Type a descriptive name for your new {item}")
		self.w42.ip_fr_new_chk.setStatusTip(f"Click to create your new {item}{nnote}")
		self.w42.ip_list_of.setStatusTip(f"Click to list available {item}s to copy")
		self.w42.ip_btn_insert.setStatusTip(f"Click to insert your {item} into {station_name}")
		self.w42.ip_btn_cancel.setStatusTip("Click to cancel")
		
	def on_btn_insert(self):
		print("insert")
		tmp=self.w42.ip_insert_preview.toPlainText()
		retval= self.valid_json.check(content=tmp, skip_change=True, skip_schema=True)
		if retval[1]:
			print("good")
			self.w42.statusJ_lbl.setText(f"Json: OK")
			#self.w42.statusJ_lbl.setStyleSheet(self.appclass42.ok_styleb)
			tmp=json.dumps(self.valid_json.valid_json, indent=4).strip("{}")+ ","
		elif not retval[1]:
			e=retval[3][0]
			print("syntax", e[:50])
			self.w42.statusJ_lbl.setText(f"Json: {e[:50].strip()}")
			#self.w42.statusJ_lbl.setStyleSheet(self.appclass42.error_styleb)
			return
		
		self.w42.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		if self.insert=='Slot Override':

			if self.w42.editbox.find('"slot_overrides": {'):
				self.w42.editbox.moveCursor(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.MoveAnchor)
				tc=self.w42.editbox.textCursor()
				tc.insertText(tmp)
				self.appclass42.fresh_indents()
				self.w42.editbox.centerCursor()
				
				self.w42.override_indexes_listbox.addItem(self.w42.ip_txtName.text())
				#self.w42.editbox.
			
		elif self.insert=='Day Template':
			if self.w42.editbox.find('"day_templates": {'):
				self.w42.editbox.moveCursor(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.MoveAnchor)
				tc=self.w42.editbox.textCursor()
				tc.insertText(tmp)
				self.w42.editbox.centerCursor()
				self.w42.daytemp_indexes_listbox.addItem(self.w42.ip_txtName.text())
		print("inserted!")
		self.disable_events()
		self.w42.edit42_stack.setCurrentIndex(1)
			
	def on_btn_cancel(self):
		print("cancel")
		self.disable_events()
		self.w42.ip_insert_preview.clear()
		self.w42.edit42_stack.setCurrentIndex(1)
		
	def on_list_chg(self):
		print("--------list")
		self.w42.list2top.timeout.connect(self.reset_text4)
		self.w42.list2top.start()
		copy=self.w42.ip_list_of.currentText()
		self.process(copy)	
		
	def on_check_chg(self):
		print("---------check")
		self.process()

	def on_return_pressed(self):
		print("-----pressed")
		self.process()
		
	def process(self, copy=None):
		match self.insert:
			case 'Slot Override':
				if self.w42.ip_fr_new_chk.isChecked():
					self.set_txt_box(self.appclass42.slot_override_opts)
				else:
					if copy is None:
						return
					
					self.set_txt_box(self.mso[copy])
			case 'Time Slot':
				if self.w42.ip_fr_new_chk.isChecked():
					self.set_txt_box(self.appclass42.time_slot_opts)
				else:
					if copy is None:
						return
					print()
			case 'Day Template':
				if self.w42.ip_fr_new_chk.isChecked():
					self.set_txt_box(self.appclass42.day_template)
				else:
					if copy is None:
						return
					self.set_txt_box(self.mdt[copy])
					
	def set_txt_box(self, templt):
		name=self.w42.ip_txtName.text()
		tmp=json.dumps({name: templt}, indent=4)
		self.w42.ip_insert_preview.setPlainText(str(tmp))

	def on_btn_snipp_save(self):
		print("save snip")
		if self.w42.ip_insert_preview.toPlainText()=='':
			return
		obj=self.w42.ip_insert_preview.toPlainText()
		retval= self.valid_json.check(content=obj, skip_change=True, skip_schema=True)
		 
		if retval[1]:
			print("good", retval)
			obj=self.valid_json.valid_json
		else:
			print("errors", retval[3])
			return
		params={'name': self.w42.ip_txtName.text(), 
			'type': self.insert, 
			'object': obj}
		
		if self.insert=='Slot Override':
			self.snipps_obj['slot_overrides'].update(obj)
		elif self.insert=='Day Template':
			self.snipps_obj['day_templates'].update(obj)
			self.mdt.update(obj)
		self.w42.ip_list_of.addItem(self.w42.ip_txtName.text())
		self.appclass42.configs.set_snipp_file({'data': self.snipps_obj, 'path': './snippfile.json'})

	def on_text_changed(self):
		tmp=self.w42.ip_insert_preview.toPlainText()
		retval= self.valid_json.check(content=tmp, skip_change=True, skip_schema=True)
		if retval[1]:
			print("good")
			self.w42.statusJ_lbl.setText(f"Json: OK")
			#self.w42.statusJ_lbl.setStyleSheet(self.appclass42.ok_styleb)
			tmp=json.dumps(self.valid_json.valid_json, indent=4).strip("{}")+ ","
		elif not retval[1]:
			e=retval[3][0]
			print("syntax", e[:50])
			self.w42.statusJ_lbl.setText(f"Json: {e[:50].strip()}")
			#self.w42.statusJ_lbl.setStyleSheet(self.appclass42.error_styleb)
		
	def reset_text4(self):
		self.w42.ip_list_of.currentIndexChanged.disconnect()
		self.w42.ip_list_of.setCurrentIndex(0)
		self.w42.ip_list_of.currentIndexChanged.connect(self.on_list_chg)
		
	def get_snipp_data(self):
		print("get_snipps appclass42", self.appclass42)
		snipps=self.appclass42.configs.get_snipp_file({'path': './snippfile.json'})
		if snipps==None:
			return
		else:
			self.snipps_obj=snipps['data']
			#print("get snipp d", type(snipps), snipps['data'])

	def mark_error_pos(self):
		tc=self.w42.ip_insert_preview.textCursor()
		cpos=tc.position()
		try:
			temp=json.loads(self.w42.ip_insert_preview.toPlainText())
		except json.decoder.JSONDecodeError as e:
			e.pos
			tc.setPosition(e.pos-4, QTextCursor.MoveMode.MoveAnchor)
			tc.setPosition(e.pos+1, QTextCursor.MoveMode.KeepAnchor)
			
			self.w42.ip_insert_preview.setTextCursor(tc)
			self.w42.ip_insert_preview.setFocus()


	def setup_highlight_rules(self):
		tslot_format = QTextCharFormat()
		#tslot_format.setFontWeight(QFont.Weight.Bold)

#########         colors keys white           ############
		tslot_format.setForeground(QColor("#ffffff"))
		pattern=r'\"(.*)\"\s*:'  #'\".*\"\s*:\s*\{'
		self._highlighter.add_mapping(pattern, tslot_format)

########           colors text values yellow          #################		
		tslot_format = QTextCharFormat()
		tslot_format.setForeground(QColor("#f9f06b"))
		pattern=r':\s*\"(.*)\",?'
		self._highlighter.add_mapping(pattern, tslot_format)

###########          colors numeric values red         ################
		tslot_format = QTextCharFormat()
		tslot_format.setForeground(QColor("#f66151"))
		pattern=r':\s*\d{,3}\.?\d?,?'
		self._highlighter.add_mapping(pattern, tslot_format)

###########          colors bool values pink         ################
		tslot_format = QTextCharFormat()
		tslot_format.setForeground(QColor("#dc8add"))
		pattern=r':\s*(true|false),?'
		self._highlighter.add_mapping(pattern, tslot_format)

###########          colors  text list values yellow         ################
		tslot_format = QTextCharFormat()
		tslot_format.setForeground(QColor("#f9f06b"))
		pattern=r'^\s+(\"[/\w-]+\")[^:]'
		self._highlighter.add_mapping(pattern, tslot_format)

		self._highlighter.setDocument(self.w42.ip_insert_preview.document())



