#!/usr/bin/python

from pathlib import Path

import json, os, glob, shutil, requests, posixpath

dgrey="\033[30;48m"
red="\033[31;48m"
green="\033[32;48m"
yel="\033[33;48m"
blue="\033[34;48m"
vio="\033[35;48m"
lblue="\033[36;48m"
lgrey="\033[37;48m"
nc="\033[0m"

		
class Get_confs():

	def __init__(self, src='api', conf_path=''):
		self.headers={"Content-Type": "application/json"}
		self.urlbase = 'http://localhost:4242/stations/'
		self.url_summary = 'http://localhost:4242/summary/stations'
		self.src=src
		self.conf_dir=conf_path
		self.chaninfo=[]
		self.chanlist=[]
		self.selected_chan=''
		if src=='file':
			self.get_file_list()
		else:
			self.urlbase=f"{conf_path}/stations/"
			self.url_summary=f"{conf_path}/summary/stations"
			self.get_api_list()
				
	def get_api_list(self):
		try:
			response = requests.get(self.url_summary, headers=self.headers)
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Is your fs42 running?{nc}\n\n")
			exit()
		temp=response.json()
		self.chanlist=temp['network_names']
		print(self.chanlist)

   		
	def get_file_list(self):
		temp=[]
		#print("get file list")
		for conf_file in Path(self.conf_dir).glob('*.json'):
			if conf_file != os.path.join(self.conf_dir, "main_config.json"):
				ret=self.get_network_name(conf_file)
				if ret!=None:
					temp.append({'name': ret, 'path': conf_file})
		#print("temp", type(temp), temp)		
		self.chanlist=temp
	
	def get_api_conf(self, fyl):
		try:
			response = requests.get(f"{self.urlbase}{fyl}", headers=self.headers)
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Is your fs42 running?{nc}\n\n")
			exit()
		temp=response.json()
		return temp['station_config']['station_conf']

	def set_api_conf(self, fyl):
		try:
			response = requests.put(f"{self.urlbase}{fyl['path']}",data=fyl['data'], headers=self.headers) 
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Is your fs42 running?{nc}\n\n")
			exit()
		temp=response.json()
		if 'success' in temp:
			return "Saved"
		
	def get_network_name(self, file):
		with open( file) as conf:
			data = json.load(conf)
		try:
			network_name=data['station_conf']['network_name']
		except:
			network_name=None
		return network_name
	
	def get_file_conf(self, fyl):
		#print("get file", type(fyl), fyl)
		with open(fyl['path']) as conf:
			data = json.load(conf)
		return data['station_conf']


	def set_file_conf(self, fyl):
		#print(type(fyl['path']), fyl['path'])
		try:
			with open(fyl['path'], "w") as conf:
				json.dump(fyl['data'], conf, indent=4)
		except OSError:
			print(f"{red}OS error{nc}")
			return "Not Saved"
		return "Saved"

	def get_snipp_file(self, fyl):
		try:
			with open(fyl['path']) as conf:
				data = json.load(conf)
		except:
			data=None
		#print(" in get confs show me type of data", type(data))
		return data
	
	def set_snipp_file(self, fyl):
		with open(fyl['path'], "w") as conf:
			json.dump({'data':fyl['data']}, conf)

		
	def make_backup(self):
		
		if self.src=='file':
			backup_dir=os.path.join(self.conf_dir, 'edit42-backup')
			Path(backup_dir).mkdir(exist_ok=True)
			#print("Make backup - self.conf_dir",self.conf_dir)
			for src in Path(self.conf_dir).glob('*.json'):
				#print("src and backup dir", src, backup_dir)
				shutil.copy2(src, backup_dir, follow_symlinks=True)
			
		else:
			Path('./edit42-backup').mkdir(exist_ok=True)
			for chan in self.chanlist:
				chan_data=self.get_api_conf(chan)
				Path(f"./edit42-backup/{chan}.json").touch()
				with Path(f"./edit42-backup/{chan}.json").open("w") as newfile:
					json.dump(chan_data, newfile, indent=4)
			
		
			
			
			
	
		
			
					
					
					
					
			
