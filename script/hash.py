#!/usr/bin/python

import os
import json
import hashlib

def get_files_list(directory, update_url): 
	file_list={}
	os.chdir(directory)
	for root, dirs, files in os.walk('.'):
		for file in files:
			file_name = root.replace('\\','/') + '/' + file
			file_hash = checksum(file_name)
			file_size = os.path.getsize(file_name)
			file_url = update_url + file_name.replace('./','')
			file_list[file_name] = {'file_hash':file_hash, 'file_size':file_size, 'file_url':file_url}
	return(file_list)

def checksum(file_name, hash_factory=hashlib.md5, chunk_num_blocks=128):
	h = hash_factory()
	with open(file_name,'rb') as f: 
		while chunk := f.read(chunk_num_blocks*h.block_size): 
			h.update(chunk)
	return h.hexdigest()

def save_json(jsons, file):
	with open(file, 'w', encoding="utf-8") as f:
		f.write(json.dumps(jsons, indent=2, ensure_ascii=False))

def read_version(directory, file):
	os.chdir(directory)
	with open(file, 'r', encoding="utf-8") as f:
		return f.read().split("LocalVersion=")[1].split("\n")[0]
		
if __name__ == '__main__':
	version_file = 'version.ini'
	info_json = {}
	info_json['name'] = 'vupslash'
	info_json['version'] = read_version('../main/',version_file)
	info_json['discription'] = 'A Sanguosha like game but characters is vup'
	info_json['author'] = '萌龙少主'
	info_json['website'] = 'https://vupslash.icu'
	info_json['source_url'] = 'https://gitee.com/shadlc/vup-slash-source/raw/master/main/'
	info_json['files'] = get_files_list('../main/', info_json['source_url'])
	json_name = 'hash_list.json'
	os.chdir('../')
	save_json(info_json, json_name)