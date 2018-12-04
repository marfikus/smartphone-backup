
# import sys
# import yadisk
import os
import datetime
from dateutil.tz import tzutc
import shutil

tzutc = tzutc()

def copy_with_replace_by_date(path_from, path_to, op_type):
	status = "Ok"
	msg = ""
	
	if not os.path.exists(path_from):
		status = "Error!"
		msg = "Path 'from' not found: '{}'".format(path_from)
		return {"status": status, "msg": msg}
	
	if op_type == "ff":
		print("file-file")
		if not os.path.isfile(path_from):
			status = "Error!"
			msg = "Path 'from' is not a file: '{}'".format(path_from)
			return {"status": status, "msg": msg}
		
		if os.path.exists(path_to):
			if not os.path.isfile(path_to):
				status = "Error!"
				msg = "Path 'to' is not a file: '{}'".format(path_to)
				return {"status": status, "msg": msg}
			
			mtime_path_from = int(os.path.getmtime(path_from))
			mtime_path_from = datetime.datetime.fromtimestamp(mtime_path_from)
			mtime_path_from = mtime_path_from.astimezone(tzutc)
			
			mtime_path_to = int(os.path.getmtime(path_to))
			mtime_path_to = datetime.datetime.fromtimestamp(mtime_path_to)
			mtime_path_to = mtime_path_to.astimezone(tzutc)
			
			if mtime_path_from > mtime_path_to:
				print("file-file: rewrite")
				shutil.copy(path_from, path_to)	
		else:
			f_path, f_name = os.path.split(path_to)
			if f_name == "": # for example, if path_to = 'dir1\dir2\'
				status = "Error!"
				msg = "Path 'to' is incorrect: '{}'".format(path_to)
				return {"status": status, "msg": msg}
			
			if os.path.exists(f_path):
				if not os.path.isdir(f_path):
					status = "Error!"
					msg = "Path: '{0}' is not a directory to write file: '{1}'. \n(May be '{2}' it is already existing file?)".format(f_path, f_name, os.path.basename(f_path))
					return {"status": status, "msg": msg}					
			else:
				print("Create path: ", f_path)
				os.makedirs(f_path)
				
			print("file-file: write")
			shutil.copy(path_from, path_to)
	
	elif op_type == "fd":
		print("file-dir")
		if not os.path.isfile(path_from):
			status = "Error!"
			msg = "Path 'from' is not a file: '{}'".format(path_from)
			return {"status": status, "msg": msg}
		
		if os.path.exists(path_to):
			if not os.path.isdir(path_to):
				status = "Error!"
				msg = "Path 'to' is not a directory: '{}'".format(path_to)
				return {"status": status, "msg": msg}
			
			file_name = os.path.basename(path_from)
			path_to_new = os.path.join(path_to, file_name)
			path_to_new = os.path.normpath(path_to_new)
			# print(path_to_new)
			
			if os.path.exists(path_to_new):
				mtime_path_from = int(os.path.getmtime(path_from))
				mtime_path_from = datetime.datetime.fromtimestamp(mtime_path_from)
				mtime_path_from = mtime_path_from.astimezone(tzutc)
			
				mtime_path_to_new = int(os.path.getmtime(path_to_new))
				mtime_path_to_new = datetime.datetime.fromtimestamp(mtime_path_to_new)
				mtime_path_to_new = mtime_path_to_new.astimezone(tzutc)
				
				if mtime_path_from > mtime_path_to_new:
					print("file-dir: rewrite")
					shutil.copy(path_from, path_to_new)
			else:
				print("file-dir: write")
				shutil.copy(path_from, path_to_new)
		else:
			print("'path_to' not exists")
			print("Create path: ", path_to)
			os.makedirs(path_to)
			print("file-dir: write")
			shutil.copy(path_from, path_to)	
		
	elif op_type == "df":
		print("dir-file")
		status = "Error!"
		msg = "Write directory to file? Are you really? It doesn't make sense. =)"
		return {"status": status, "msg": msg}
		
	elif op_type == "dd":
		print("dir-dir")
		if not os.path.isdir(path_from):
			status = "Error!"
			msg = "Path 'from' is not a directory: '{}'".format(path_from)
			return {"status": status, "msg": msg}

		list_path_from = os.listdir(path_from)
		print(list_path_from)
		print(len(list_path_from))
		
		if len(list_path_from) == 0:
			# print("path_to: ", path_to)
			if not os.path.exists(path_to):
				print("Create path: ", path_to)
				os.makedirs(path_to)
		
		for obj in list_path_from:
			print(obj)
			path_from_obj = os.path.join(path_from, obj)
			path_from_obj = os.path.normpath(path_from_obj)
			if os.path.isfile(path_from_obj):
				print("file")
				res = copy_with_replace_by_date(path_from_obj, path_to, "fd")
				print(res)
			elif os.path.isdir(path_from_obj):
				print("dir")
				path_to_obj = os.path.join(path_to, obj)
				path_to_obj = os.path.normpath(path_to_obj)
				res = copy_with_replace_by_date(path_from_obj, path_to_obj, "dd")
				print(res)
			else:
				# print("The object is not supported: ", path_from_obj)
				status = "Error!"
				msg = "The object is not supported: '{}'".format(path_from_obj)
				return {"status": status, "msg": msg}
			print("======================")
			
			
	else:
		status = "Error!"
		msg = "Operation type is undefined: '{}'".format(op_type)
		return {"status": status, "msg": msg}
			
	return {"status": status, "msg": msg}

dir_from = r"test_dir_from"
dir_from_f1 = r"test_dir_from\myfile.txt"
dir_from_f2 = r"test_dir_from\myfile2.txt"
dir_to = r"test_dir_to"
dir_to_f1 = r"test_dir_to\myfile.txt"
dir_to_f1_er = r"test_dir_to\myfile.txt\ddd"
dir_to_f2 = r"test_dir_to\myfile2.txt"
dir_to_d3 = r"test_dir_to\dir_3"
dir_to_d3_er = "test_dir_to\dir_3\\"
dir_to_d3_f1 = r"test_dir_to\dir_3\myfile.txt"

a = copy_with_replace_by_date("ddd", "test_dir_to\\ddd", "dd")
print(a)

# add copied files counter
# fix: copy empty dirs
# fix: создать каталог, если он не указан в пути назначения (сравнить с хcopy)

