#!/usr/bin/python

import os, json, copy, locale, hashlib, sys, jsonschema
from datetime import datetime, date
from PySide6.QtGui import (QTextCharFormat, QFont, QColor, QTextCursor)
from PySide6.QtCore import QRegularExpression, QTimer
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from Get_station_confs import Get_confs

from Highlighter import Highlighter
from json_valid import json_valid
#from create42_win import Creator42

dgrey="\033[30;48m"
red="\033[31;48m"
green="\033[32;48m"
yel="\033[33;48m"
blue="\033[34;48m"
vio="\033[35;48m"
lblue="\033[36;48m"
lgrey="\033[37;48m"
nc="\033[0m"


class edit42():
	def __init__(self, appname, appversion, appconf, debug):
		self.app_name=appname
		self.app_version=appversion
		self.appconf=appconf
		self.debug=debug
		if self.appconf is None:
			self.print_debug("No data")
		else: 
			self.print_debug(f"edit42 init, {self.appconf.items()}")
			for k in self.appconf.items():
				self.cfg_src=k[0]   #'file' ## 'api'
				self.cfg_path=k[1]    #"./confs"
		self.print_debug(f"{self.cfg_src}, {self.cfg_path}")
		self.is_changed=False
		schema_file_json="./station_config_schema.json"
		
		self.chanlist=None
		self.channel_selected=None
		self.stations_list=[]
		self.the_week=[]
		self.the_day=[]
		self.current_locale=locale.getlocale()
		weekdays={}
		weekdays[self.current_locale] = [date(2001, 1, i).strftime('%A') for i in range(1, 8)]
		self.weekdays=weekdays
		com='background-color: "#27193c"; padding: 5px; font-weight: bold;'
		self.ok_stylej='color: "#bfb6cd";'+ com
		self.error_stylej='color: red;' + com
		self.ok_style='color: "#bfb6cd"; padding: 5px;'
		self.error_style='color: red; padding: 5px;'
		self.slot_override_opts={'start_bump': "", 
			'end_bump': "", 
			'bump_dir': "", 
			'commercial_dir': "",
			'break_strategy': ['standard', 'center', 'end'], 
			'schedule_increment': 120, 
			'sequence': 'week night', 
			'sequence_start': 0.5, 
			'sequence_end': 1.0, 
			'marathon': {'chance': 0.2 , 'count': 4}, 
			'random_tags': [True, False], 
			'video_scramble_fx': 
				['horizontal_line', 'diagonal_lines', 'static_overlay', 'pixel_block', 'color_inversion', 'severe_noise', 'wavy', 'random_block', 'chunky_scramble'] }
		tmp=copy.deepcopy(self.slot_override_opts)
		self.time_slot_opts={'tags': 'folder'}
		self.time_slot_opts.update(tmp)
		self.tag_override_opts=copy.deepcopy(self.slot_override_opts)
		self.station={"station_conf": {
			"network_name": "New Channel",
			"channel_number": 5,
			"content_dir": "catalog/my_videos",

			"monday": {},
			"tuesday": {},
			"wednesday": {},
			"thursday": {},
			"friday": {},
			"saturday": {},
			"sunday": {}
			}
			}
		self.day_template={}
		for h in range(24):
			if h<=2 or h>=6:
				self.day_template.update({f"{str(h)}" :{"tags": "your folder"}})
			elif h==3:
				self.day_template.update({f"{str(h)}" :{"event": "signoff"}})
		self.reindent=QTimer()
		self.reindent.setInterval(3000)
		self.reindent.setSingleShot(True)
		self.reindent.timeout.connect(self.fresh_indents)
		self.updateListBoxes=QTimer()
		self.updateListBoxes.setInterval(10000)
		self.updateListBoxes.timeout.connect(self.setup_indexes)
		self.print_debug("edit 42 init")


	def hili_now_slot(self):
		current=datetime.now()
		
		thedow=current.strftime("%A").lower()
		thehour=current.strftime("%-H")
		self.win42.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
		if type (self.chan_data[thedow]) is str:
			dt=self.chan_data[thedow]
			self.print_debug(f"{thedow}: {dt}")
			self.win42.editbox.find('day_templates')
			self.win42.editbox.find(dt)
			#self.win42.editbox.find(thehour)
			
		elif type (self.chan_data[thedow]) is dict:
			self.print_debug(self.chan_data[thedow][thehour])
			self.win42.editbox.find(thedow)
		
		regstr=f'\\"{thehour}\\"\\s*:'
		reg=QRegularExpression(regstr)
		self.print_debug(f"the reg {regstr}")
		self.win42.editbox.find(reg)
		self.win42.editbox.centerCursor()
		
	def setup_editor(self):
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

		self._highlighter.setDocument(self.win42.editbox.document())
		
	def print_debug(self, msg, lvl=1):
		if lvl==1:
			txt_color=lgrey
		elif lvl==2:
			txt_color=yel
		else:
			txt_color=red
		if self.debug:	
			print(f"{txt_color}{msg}{nc}")
		
	def initialize_win(self, w42):
		self.print_debug(f"edit 42.initialize_win. type {type(w42)}")
		self.win42=w42
		self.configs=Get_confs(src=self.cfg_src, conf_path=self.cfg_path)
		self.chanlist=self.configs.chanlist
		

	def setup_indexes(self):
		self.toggleBoxBlock()
		commons=['Select Element', 'Now Slot', 'channel_number', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
		other_settings=['autobump', 'tag_overrides', 'slot_overrides', 'day_templates', 'clip_shows']
		for other in other_settings:
			if other in self.chan_data:
				commons.insert(2, other)
		
		indexes_lb= self.win42.indexes_listbox
		daytemp_lb=self.win42.daytemp_indexes_listbox
		overrides_lb=self.win42.override_indexes_listbox
		
		indexes_lb.clear()
		daytemp_lb.clear()
		overrides_lb.clear()
		
		indexes_lb.addItems(commons)
		indexes_lb.setCurrentText('Select Element')
		
		if 'slot_overrides' in self.chan_data:
			overrides_lst=[]
			overrides_lst.append("Select Override")
			for so in self.chan_data['slot_overrides']:
				overrides_lst.append(so)
			overrides_lb.addItems(overrides_lst)
			overrides_lb.setCurrentText("Select Override")

		if 'day_templates' in self.chan_data:
			daytemp_indexes=[]
			daytemp_indexes.append("Select Template")
			for dt in self.chan_data['day_templates']:
				daytemp_indexes.append(dt)
			daytemp_lb.addItems(daytemp_indexes)
			daytemp_lb.setCurrentText("Select Template")
		if not self.updateListBoxes.isActive():
			self.win42.editbox.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
			self.print_debug("not active")
		self.toggleBoxBlock(value=False)
		self.updateListBoxes.start()
		self.print_debug("setup indexes - indexed")

		
	def init_chan_listbox(self):
		self.win42.chan_listbox.blockSignals(True)
		self.win42.chan_listbox.clear()
		#self.print_debug("chan list box",self.chanlist)
		if self.cfg_src=='api':
			self.win42.chan_listbox.addItems(self.chanlist)
			self.win42.chan_listbox.setCurrentText(self.channel_selected)
		else:
			for i in self.chanlist:
				self.win42.chan_listbox.addItem(i['name'])
			self.win42.chan_listbox.setCurrentText(self.channel_selected['name'])
		self.win42.chan_listbox.blockSignals(False)
		#self.win42.setup_event_slots()
		

	def toggleBoxBlock(self, value=True):
		boxen=[self.win42.indexes_listbox, 
			self.win42.daytemp_indexes_listbox, 
			self.win42.override_indexes_listbox, 
			self.win42.chan_listbox, 
			self.win42.editbox, 
			self.win42.insert_list]
		for box in boxen:
			box.blockSignals(value)


	#########---------- Update functions --------###################
	################################################################
	################################################################
			
	def update_wintitle(self, changed=False):
		title=f"{self.app_name} | {self.chan_data['channel_number']}: {self.chan_data['network_name']}"
		if changed:
			title=title+"*"
		self.win42.setWindowTitle(title)	

	def switch_channel_data(self, selected):
		def do_switch():
			self.print_debug(f"clicked: {selected}")
			if self.cfg_src=='api': self.channel_selected=selected
			else:
				for i in self.chanlist:
					if i['name']==selected:
						self.channel_selected=i
			self.open_cfg()
			
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Icon.Warning)
		msgBox.setWindowTitle(self.app_name)
		msgBox.setText("The document has been modified.")
		msgBox.setInformativeText("Do you want to save your changes?")
		msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
		msgBox.setDefaultButton(QMessageBox.Save)
		
		if self.is_changed:
			self.print_debug("unsaved changes")
			ret = msgBox.exec()
			if ret == QMessageBox.Save:
				self.do_save()
				do_switch()
			elif ret == QMessageBox.StandardButton.Discard:
				do_switch()
			elif ret == QMessageBox.StandardButton.Cancel:
				self.win42.chan_listbox.currentIndexChanged.disconnect()
				self.win42.chan_listbox.setCurrentText(self.channel_selected['name'])
				self.win42.chan_listbox.currentIndexChanged.connect(self.win42.on_chan_changed)
				return
			else:
				# should never be reached
				return
		else:
			do_switch()


	def fresh_indents(self):
		self.print_debug("Fresh")
		self.win42.editbox.blockSignals(True)
		obj=json.dumps(self.valid_json.valid_json, indent=4)
		
		self.print_debug(f"object type, {type(obj)}, {len(obj)}")
		tc=self.win42.editbox.textCursor()
		pos=tc.position()
		
		self.win42.editbox.setPlainText(obj)
		self.win42.editbox.blockSignals(False)
		tc.setPosition(pos, QTextCursor.MoveMode.MoveAnchor)
		self.win42.editbox.setTextCursor(tc)
		
		self.win42.editbox.centerCursor()
		

	def check_content_change(self):
		objstr=self.win42.editbox.toPlainText()
		#self.print_debug("check_content - valid_json", type(self.valid_json), self.valid_json)
		retval= self.valid_json.check(content=objstr)
		
		#self.print_debug(f"at check_content_changed - changed: {retval[0]}, syntax: {retval[1]}, schema: {retval[2]}\n chan_data {str(self.chan_data)[:50]}")
		if retval[0]:
			if retval[1]:
				self.win42.statusJ_lbl.setText(f"Json: OK")
				self.win42.statusJ_lbl.setStyleSheet(self.ok_stylej)
				#self.print_debug("valid json", str(self.valid_json.valid_json)[:55])
				self.update_app_json(self.valid_json.valid_json)
				self.is_changed=True
				self.update_wintitle(changed=self.is_changed)
				
			if retval[2]:
				self.win42.statusS_lbl.setText(f"<b>Schema</b>: OK")
				self.win42.statusS_lbl.setStyleSheet(self.ok_style)
				
			if not retval[1]:
				e=retval[3][0]
				#self.print_debug("syntax", e[:50])
				self.win42.statusJ_lbl.setText(f"Json: {e[:50].strip()}")
				self.win42.statusJ_lbl.setStyleSheet(self.error_stylej)
								
			elif not retval[2]:
				e=retval[3][0]
				#self.print_debug("schema", e[:50])
				self.win42.statusS_lbl.setText(f"<b>Schema</b>: {e[:50].strip()}")
				self.win42.statusS_lbl.setStyleSheet(self.error_style)
		elif not  retval[0]:
			e=retval[3][0]
			#self.reindent.start()
			#self.print_debug("no change", e[:50])

	def mark_error_pos(self):
		tc=self.win42.editbox.textCursor()
		cpos=tc.position()
		try:
			temp=json.loads(self.win42.editbox.toPlainText())
		except json.decoder.JSONDecodeError as e:
			e.pos
			tc.setPosition(e.pos-3, QTextCursor.MoveMode.MoveAnchor)
			tc.setPosition(e.pos+3, QTextCursor.MoveMode.KeepAnchor)
			#tc.setPosition(cpos, QTextCursor.MoveMode.MoveAnchor)
			self.win42.editbox.setTextCursor(tc)
			self.win42.editbox.setFocus()
			#tc.setCharFormat(fontWeight(QFont.Bold))
			
	def update_app_json(self, app_json):
		self.print_debug("update editbox to self.chan_data")
		self.chan_data=app_json
	

	def do_save(self):
		name=None
		if self.cfg_src=='api':
			name=self.channel_selected
			payload={'path': self.channel_selected, 'data': json.dumps({'station_conf':self.chan_data}, indent=4)}
			ret=self.configs.set_api_conf(payload)
			if ret=="Saved": self.set_saved_indicate(name)
			else: self.error_save(name)
				
		else:
			name=self.channel_selected['name']
			cfg_file= self.channel_selected['path']
			#self.print_debug(cfg_file, self.chan_data)
			payload={'path': cfg_file, 'data':{'station_conf':self.chan_data}}
			ret=self.configs.set_file_conf(payload)
			if ret=="Saved": self.set_saved_indicate(name)
			else: self.error_save(name)
		self.print_debug("Saved")
		self.is_changed=False
		self.update_wintitle(changed=self.is_changed)
	
	def set_saved_indicate(self, name):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Icon.Information)
		msgBox.setWindowTitle(f"{self.app_name} - Save Message - Ok")
		msgBox.setText(f"{name} has successfully saved.")
		msgBox.exec()

	def error_save(self, name):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Icon.Critical)
		msgBox.setWindowTitle(f"{self.app_name} - Save Message - Error")
		msgBox.setText(f"Error: Problem saving {name}")
		msgBox.exec()

	def open_cfg(self):
#		fileName = QFileDialog.getOpenFileName(self.win42, "Open FS42 Station Config Files", "/home/kkurtz/Documents/bash-scripts/edit42/confs", "Json Files (*json)")
		self.print_debug(self.chanlist)
		self.print_debug("open cfg")
		if self.channel_selected==None:
			self.channel_selected=self.chanlist[0]
		else:	
			self.win42.disconnect_event_slots()
		
		self.valid_json=None
		self.is_changed=False
		
		if self.cfg_src=='file':
			self.chan_data=self.configs.get_file_conf(self.channel_selected)
		else:
			self.chan_data=self.configs.get_api_conf(self.channel_selected)

		self.init_chan_listbox()
		self.update_wintitle()
		self._highlighter = Highlighter()
		self.setup_editor()
				
		txt=json.dumps(self.chan_data, indent=4)
		self.valid_json=json_valid(txt)
		
		self.win42.editbox.setPlainText(txt)
		self.setup_indexes()
		
		self.win42.setup_event_slots()
		
		
	def init_creator(self, item):
		self.creator42=Creator42(self, self.win42)
		#self.creator42.appclass42=self
		#self.creator42.win42=self.win42
		self.creator42.setup(item)
		

		
