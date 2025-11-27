#!/usr/bin/python

import os, json, hashlib, jsonschema

dgrey="\033[30;48m"
red="\033[31;48m"
green="\033[32;48m"
yel="\033[33;48m"
blue="\033[34;48m"
vio="\033[35;48m"
lblue="\033[36;48m"
lgrey="\033[37;48m"
nc="\033[0m"

class json_valid():
	def __init__(self, content=None):
		if content is not None: self.signature=self.get_signature(self.remove_newlines(content))
		self.json_is_good=False
		self.valid_json=None
		self.station_schema=None
		self.content=None
		self.good_syntax=False
		self.errors=[]
		self.skip_change=False
		self.skip_schema=False
		self.is_changed=False
		self.error_position=None
		self.schema_file_json="./station_config_schema.json"

		
	def check(self, content, skip_change=False, skip_schema=False):
		self.json_is_good=False
		#self.valid_json=None
		self.good_syntax=False
		self.is_changed=False
		self.skip_schema=skip_schema
		self.errors=[]
		self.skip_change=skip_change
		self.content=content
		
		json_str=self.remove_newlines(self.content)
		if not self.skip_change:
			newsig=self.get_signature(json_str)
			#print(newsig)
			#print(self.signature)
			if self.signature is None: 
				self.signature= newsig
				self.is_changed=True
			elif self.signature == newsig:
				self.errors.append("No change")
				return (self.is_changed, self.good_syntax, self.json_is_good, self.errors, self.valid_json)
			else:
				self.is_changed=True
				self.signature = newsig
		
		retval=self.check_json(json_str)
		if type(retval) is dict or type(retval) is tuple or type(retval) is list: 
			self.good_syntax=True	
			json_str=retval
		else: 
			self.errors.append(retval)
			return (self.is_changed, self.good_syntax, self.json_is_good, self.errors, self.valid_json)
		
		if self.skip_schema:
			self.json_is_good=True
			self.valid_json=json_str
		else:
			self.load_schema_from_file(self.schema_file_json)	
			retval=self.check_schema_valid(json_str)
			if type(retval) is bool:
				self.json_is_good=True
				self.valid_json=json_str
			else:
				self.errors.append(retval)
		return (self.is_changed, self.good_syntax, self.json_is_good, self.errors, self.valid_json)
			

	
	def load_schema_from_file(self, filename):
		with open(filename, "r") as file:
			self.station_schema=json.load(file)	

	def get_signature(self, content):
		hasher=hashlib.sha256()
		bcontent=bytes(content, 'utf-8')
		hasher.update(bcontent)
		return hasher.hexdigest()

	def remove_newlines(self, chan_data_dump):
		spc=" " * 20            #"                    " #20 spaces
		chan_data_dump=chan_data_dump.replace("\n", "")
		#chan_data_dump=chan_data_dump.replace("\"", "'")
		chan_data_dump=chan_data_dump.replace(spc[:10], "")
		chan_data_dump=chan_data_dump.replace(spc[:9], "")
		chan_data_dump=chan_data_dump.replace(spc[:8], "")
		chan_data_dump=chan_data_dump.replace(spc[:7], "")
		chan_data_dump=chan_data_dump.replace(spc[:6], "")
		chan_data_dump=chan_data_dump.replace(spc[:5], "")
		chan_data_dump=chan_data_dump.replace(spc[:4], "")
		chan_data_dump=chan_data_dump.replace(spc[:3], "")
		chan_data_dump=chan_data_dump.replace(spc[:2], "")
		chan_data_dump=chan_data_dump.strip("\"'\\")
		return chan_data_dump
		
	def check_json(self, json_str):
		try:
			tempjson=json.loads(json_str)
		except json.decoder.JSONDecodeError as e:
			error_msg=f"{e.msg}  {e.pos}"
			self.error_position=e.pos
			return error_msg
		
		return tempjson
		
	def check_schema_valid(self, good_json):	
		good_json={'station_conf': good_json}
		try:
			jsonschema.validate(instance=good_json, schema=self.station_schema)	
		except jsonschema.exceptions.ValidationError as e:
			error_msg=f"{e.message}    PATH{e.json_path}"
			return error_msg
		return True
			

