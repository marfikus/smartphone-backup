
import yadisk
import os
import datetime
from dateutil.tz import tzutc
import shutil
import my_input_data as mid
import connect_data
import posixpath
import pickle

tzutc = tzutc()
local_db = {}
file_name_local_db = "local_db"

def make_dirs_yadisk(path):
	# print(path)
	list_dirs = []
	while not y.exists(path):
		path, dir_name = posixpath.split(path)
		list_dirs.append(dir_name)
	
	list_dirs.reverse()
	# print(path)
	for i in list_dirs:
		# print(i)
		path = posixpath.join(path, i)
		path = posixpath.normpath(path)
		# print(path)
		y.mkdir(path)
		
	return path

	
def check_file_in_local_db(path, mtime):
	# print("check:")
	global local_db, file_name_local_db
	
	if len(local_db) == 0:
		if not os.path.exists(file_name_local_db):
			print("File '{}' not found!\n".format(file_name_local_db))
			return False
			
		print("loading local_db")
		f = open(file_name_local_db, "rb")
		local_db = pickle.load(f)
		f.close()
	
	# for i in local_db:
		# print(i, local_db[i])
	print("path: ", path)
	
	if path not in local_db:
		print("Path is not in local_db!\n")
		return False
	
	mtime_from_db = local_db[path]
	# print("mtime_from_db: ", mtime_from_db)
	
	if mtime > mtime_from_db:
		print("Rewrite is necessary!\n")
		return False
		
	return True


def write_file_to_local_db(path, mtime):
	# print("write to db:")
	global local_db, file_name_local_db

	local_db[path] = mtime
	# local_db.update(path=mtime)
	
	# for i in local_db:
		# print(i, local_db[i])

	f = open(file_name_local_db, "wb")
	pickle.dump(local_db, f)
	f.close()

	
def copy_with_replace_by_date(path_from, path_to, op_type, set_of_ignored_paths):
	status = "Ok"
	msg = ""
	copied_files = 0
	global task_errors
	
	if not os.path.exists(path_from):
		status = "Error!"
		msg = "Path 'from' not found: '{}'".format(path_from)
		return {"status": status, "msg": msg, "copied_files": copied_files}
		
	if path_from in set_of_ignored_paths:
		msg = "Path is ignored: '{}'".format(path_from)
		return {"status": status, "msg": msg, "copied_files": copied_files}
	
	if op_type == "ff":
		# print("file-file")
		if not os.path.isfile(path_from):
			status = "Error!"
			msg = "Path 'from' is not a file: '{}'".format(path_from)
			return {"status": status, "msg": msg, "copied_files": copied_files}
			
		mtime_path_from = int(os.path.getmtime(path_from))
		mtime_path_from = datetime.datetime.fromtimestamp(mtime_path_from)
		mtime_path_from = mtime_path_from.astimezone(tzutc)
			
		if check_file_in_local_db(path_from, mtime_path_from):
			msg = "File skipped: '{}'".format(path_from)
			return {"status": status, "msg": msg, "copied_files": copied_files}		
			
		if y.exists(path_to):
			if not y.is_file(path_to):
				status = "Error!"
				msg = "Path 'to' is not a file: '{}'".format(path_to)
				return {"status": status, "msg": msg, "copied_files": copied_files}
			
			mtime_path_to = y.get_meta(path_to, fields={"modified"})["modified"]
			mtime_path_to = mtime_path_to.astimezone(tzutc)
			# print(mtime_path_to)
			
			if mtime_path_from > mtime_path_to:
				print("file-file: rewrite")
				# shutil.copy(path_from, path_to)
				y.upload(path_from, path_to, overwrite=True)
				copied_files += 1
				
			write_file_to_local_db(path_from, mtime_path_from)
			# if 'local_db' is empty(lost or irrelevant), but files in 'path_to' is exists			
		else:
			f_path, f_name = os.path.split(path_to)
			if f_name == "": # for example, if path_to = 'dir1\dir2\'
				status = "Error!"
				msg = "Path 'to' is incorrect: '{}'".format(path_to)
				return {"status": status, "msg": msg, "copied_files": copied_files}
			
			if y.exists(f_path):
				if not y.is_dir(f_path):
					status = "Error!"
					msg = "Path: '{0}' is not a directory to write file: '{1}'. \n(May be '{2}' it is already existing file?)".format(f_path, f_name, os.path.basename(f_path))
					return {"status": status, "msg": msg, "copied_files": copied_files}
			else:
				print("Create path: ", f_path)
				# os.makedirs(f_path)
				# y.mkdir(f_path)
				make_dirs_yadisk(f_path)
				
			print("file-file: write")
			# shutil.copy(path_from, path_to)
			y.upload(path_from, path_to)
			copied_files += 1
			write_file_to_local_db(path_from, mtime_path_from)
	
	elif op_type == "fd":
		# print("file-dir")
		if not os.path.isfile(path_from):
			status = "Error!"
			msg = "Path 'from' is not a file: '{}'".format(path_from)
			return {"status": status, "msg": msg, "copied_files": copied_files}
			
		mtime_path_from = int(os.path.getmtime(path_from))
		mtime_path_from = datetime.datetime.fromtimestamp(mtime_path_from)
		mtime_path_from = mtime_path_from.astimezone(tzutc)
		
		if check_file_in_local_db(path_from, mtime_path_from):
			msg = "File skipped: '{}'".format(path_from)
			return {"status": status, "msg": msg, "copied_files": copied_files}			
		
		file_name = os.path.basename(path_from)
		path_to_new = posixpath.join(path_to, file_name)
		path_to_new = posixpath.normpath(path_to_new)
		# print(path_to_new)
		
		if y.exists(path_to):
			if not y.is_dir(path_to):
				status = "Error!"
				msg = "Path 'to' is not a directory: '{}'".format(path_to)
				return {"status": status, "msg": msg, "copied_files": copied_files}
			
			if y.exists(path_to_new):
				if not y.is_file(path_to_new):
					status = "Error!"
					msg = "Path 'to' is not a file: '{}'".format(path_to_new)
					return {"status": status, "msg": msg, "copied_files": copied_files}
			
				mtime_path_to_new = y.get_meta(path_to_new, fields={"modified"})["modified"]
				mtime_path_to_new = mtime_path_to_new.astimezone(tzutc)
				
				if mtime_path_from > mtime_path_to_new:
					print("file-dir: rewrite")
					# shutil.copy(path_from, path_to_new)
					y.upload(path_from, path_to_new, overwrite=True, timeout=120.0)
					copied_files += 1
					# write_file_to_local_db(path_from, mtime_path_from)
					
				write_file_to_local_db(path_from, mtime_path_from)
				# if 'local_db' is empty(lost or irrelevant), but files in 'path_to' is exists
			else:
				print("file-dir: write")
				# shutil.copy(path_from, path_to_new)
				y.upload(path_from, path_to_new, timeout=120.0)
				copied_files += 1
				write_file_to_local_db(path_from, mtime_path_from)
		else:
			# print("'path_to' not exists")
			print("Create path: ", path_to)
			# os.makedirs(path_to)
			make_dirs_yadisk(path_to)
			print("file-dir: write")
			# shutil.copy(path_from, path_to)
			y.upload(path_from, path_to_new, timeout=120.0)
			copied_files += 1
			write_file_to_local_db(path_from, mtime_path_from)
		
	elif op_type == "df":
		print("dir-file")
		status = "Error!"
		msg = "Write directory to file? Are you really? It doesn't make sense. =)"
		return {"status": status, "msg": msg, "copied_files": copied_files}
		
	elif op_type == "dd":
		# print("dir-dir")
		if not os.path.isdir(path_from):
			status = "Error!"
			msg = "Path 'from' is not a directory: '{}'".format(path_from)
			return {"status": status, "msg": msg, "copied_files": copied_files}

		list_path_from = os.listdir(path_from)
		# print("list_path_from: ", list_path_from)
		# print("len(list_path_from): ", len(list_path_from))
		
		len_objects = len(list_path_from)
		if len_objects == 0:
			# print("path_to: ", path_to)
			if not y.exists(path_to):
				print("Empty folder. Create path: ", path_to)
				# os.makedirs(path_to)
				make_dirs_yadisk(path_to)
		
		cur_obj = 1
		for obj in list_path_from:
			print("Object {0} of {1}:".format(cur_obj, len_objects))
			# print("obj: ", obj)
			path_from_obj = os.path.join(path_from, obj)
			path_from_obj = os.path.normpath(path_from_obj)

			# if the file was deleted during directory copying
			if not os.path.exists(path_from_obj):
				res = {"status": "Error!", "msg": "Path not found: '{}'".format(path_from_obj), "copied_files": 0, "tag": "fake return"}
				task_errors.append(res)
				cur_obj += 1
				continue 
				# just skipped this file but didn't stop the task

			if os.path.isfile(path_from_obj):
				print("obj: {} (file)".format(obj))
				res = copy_with_replace_by_date(path_from_obj, path_to, "fd", set_of_ignored_paths)
				print(res)
				copied_files += res["copied_files"]
				if res["status"] == "Error!":
					task_errors.append(res)
			elif os.path.isdir(path_from_obj):
				print("obj: {} (dir)".format(obj))
				path_to_obj = posixpath.join(path_to, obj)
				path_to_obj = posixpath.normpath(path_to_obj)
				res = copy_with_replace_by_date(path_from_obj, path_to_obj, "dd", set_of_ignored_paths)
				print(res)
				copied_files += res["copied_files"]
				if res["status"] == "Error!":
					task_errors.append(res)
			else:
				res = {"status": "Error!", "msg": "The object is not supported: '{}'".format(path_from_obj), "copied_files": 0, "tag": "fake return"}
				task_errors.append(res)
				# just skipped this file but didn't stop the task
				
			cur_obj += 1
			print("-----------------------------------------------")
			
	else:
		status = "Error!"
		msg = "Operation type is undefined: '{}'".format(op_type)
		return {"status": status, "msg": msg, "copied_files": copied_files}
			
	return {"status": status, "msg": msg, "copied_files": copied_files}

	
y = yadisk.YaDisk(token=connect_data.token)

if not y.check_token():
	print("Token is False!")
	quit()

task_errors = []
general_report = []

sum_copied_files = 0
cur_task = 1
len_tasks = len(mid.list_of_tasks)
for i in mid.list_of_tasks:
	print("===============================================")
	print("Task {0} of {1}:".format(cur_task, len_tasks))
	print(i)
	res = copy_with_replace_by_date(i[0], i[1], i[2], mid.set_of_ignored_paths)
	print(res)
	sum_copied_files += res["copied_files"]
	general_report.append([i, res, task_errors.copy()])
	task_errors.clear()
	cur_task += 1
	print("===============================================")
	
print("\nGeneral report:")
for i in general_report:
	print("===============================================")
	print("Task:", i[0])
	print("Result:", i[1])
	error_count = len(i[2])
	print("Internal errors:", error_count)
	if error_count > 0:
		for j in i[2]:
			print(j)
	print("===============================================")
print("Total files copied:",  sum_copied_files)
	
