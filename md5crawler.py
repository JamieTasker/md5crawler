import hashlib
import os
import sys
import csv
from datetime import datetime
import queue
from threading import Thread

def get_dirs_files(folder):

	file_list = []
	for root, dirs, files in os.walk(folder):
		for file in files:
			file_list.append(root.replace('\\', '/') + '/' + file)
	
	return file_list

def get_md5_queue_to_dict(q, md5_data):
	
	while True:
		try:
			current_file = q.get()
			hash = hashlib.md5()
			hash.update(open(current_file, 'rb').read())
			md5 = hash.hexdigest()
			
			md5_data[current_file] = md5
			
		except (PermissionError, FileNotFoundError):
			pass
			
		q.task_done()

def get_file_date_modified_str(file):
	
	filetime_epoch = os.path.getmtime(file)
	filetime_str = datetime.fromtimestamp(filetime_epoch).strftime('%d/%m/%Y - %H:%M:%S')
	
	return filetime_str

def get_file_date_created_str(file):
	
	filetime_epoch = os.path.getctime(file)
	filetime_str = datetime.fromtimestamp(filetime_epoch).strftime('%d/%m/%Y - %H:%M:%S')
	
	return filetime_str
	
def get_dict_value_duplicates(search_dict):
	
	duplicates_dict = {}
	vals = list(search_dict.values())
	
	for key, value in search_dict.items():
		if vals.count(value) > 1:
			if value not in duplicates_dict:
				duplicates_dict[value] = [key]
			else:
				duplicates_dict[value].append(key)
		
	return duplicates_dict

application_start = datetime.now()

#####PARAMS##### 
# Specify the parameters for your search. You'll probably want to change these. 
search_dir = '/home/user/'
csv_out =  open('/home/user/MD5Out.csv', 'w')
################

csv_writer = csv.writer(csv_out, delimiter=',', lineterminator='\n')
md5_dict = {}

print ('Getting a list of files...')
files = get_dirs_files(search_dir)
files_length = len(files)

print ('Generating MD5 for ' + str(files_length) + ' files using 10 threads...')
q = queue.Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
  worker = Thread(target=get_md5_queue_to_dict, args=(q, md5_dict))
  worker.setDaemon(True)
  worker.start()

for file in files:
  q.put(file)

q.join()

print('Finding duplicate files...\n')
dup_dict = get_dict_value_duplicates(md5_dict)

for keys, values in dup_dict.items():
	csv_writer.writerow([keys])
	csv_writer.writerow(['filepath', 'datemodified', 'datecreated'])
	print('This MD5 key: ' + keys + ' was generated for ' + str(len(values))  + ' files: ')
	for value in values:
		print (value)
		date_modified = get_file_date_modified_str(value)
		date_created = get_file_date_created_str(value)
		
		to_write = [value, date_modified, date_created]
		csv_writer.writerow(to_write)
		
	print ('\n')

csv_out.close()

application_end = datetime.now()

time_taken = application_end-application_start
print (time_taken)
print ('\nDone!')