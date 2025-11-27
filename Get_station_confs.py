from pathlib import Path
import json, os, glob, requests

dgrey="\033[30;48m"
red="\033[31;48m"
green="\033[32;48m"
yel="\033[33;48m"
blue="\033[34;48m"
vio="\033[35;48m"
lblue="\033[36;48m"
lgrey="\033[37;48m"
nc="\033[0m"

class get_slots_framework():
	def __init__(self):
		self.conf_file=Path('/home/kkurtz/Documents/bash-scripts/station-ed42/slot-framework.json')
		self.slot_fw=''
		with open(self.conf_file, 'r') as file:
			data = json.load(file)
		self.slot_fw= data
		#print(data['slot_items']['tags'])
		
class Get_confs():

	def __init__(self, src='api', conf_path=''):
		self.headers={"Content-Type": "application/json"}
		self.urlbase = 'http://localhost:4242/stations/'
		self.url_summary = 'http://localhost:4242/summary/stations'
		#self.url=self.urlbase
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
			response = requests.get(self.url_summary, headers=self.headers) #, json=data)
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Tern on yer fekin' server, ye fekin' Fekass!!{nc}\n\n")
			exit()
		temp=response.json()
		self.chanlist=temp['network_names']
		print(self.chanlist)

		
	def get_all_api(self):
		print("TODO: update to work with new way")
		return
		try:
			response = requests.get(self.url, headers=self.headers) #, json=data)
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Tern on yer fekin' server, ye fekin' Fekass!!{nc}\n\n")
			exit()
		self.chaninfo=response.json()
   		
	def get_file_list(self):
		temp=[]
		for conf_file in glob.glob(f"{self.conf_dir}/*.json"): #os.listdir(self.conf_dir):
			if conf_file != os.path.join(self.conf_dir, "main_config.json"):
				ret=self.get_network_name(conf_file)
				if ret!=None:
					temp.append({'name': ret, 'path': conf_file})
		#print("temp", type(temp), temp)		
		self.chanlist=temp
	
	def get_api_conf(self, fyl):
		try:
			response = requests.get(f"{self.urlbase}{fyl}", headers=self.headers) #, json=data)
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Tern on yer fekin' server, ye fekin' Fekass!!{nc}\n\n")
			exit()
		
		temp=response.json()
		
		return temp['station_config']['station_conf']

	def set_api_conf(self, fyl):
		#print(fyl['data'])
		try:
			response = requests.put(f"{self.urlbase}{fyl['path']}",data=fyl['data'], headers=self.headers) 
		except requests.exceptions.RequestException as e:
			print(f"\n\t{red}Tern on yer fekin' server, ye fekin' Fekass!!{nc}\n\n")
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
		with open(fyl['path'], "w") as conf:
			json.dump(fyl['data'], conf)

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
			
			
			
