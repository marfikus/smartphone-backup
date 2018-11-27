
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
		# print("Path 'from' not found: ", path_from)
		status = "Error!"
		msg = "Path 'from' not found: '{}'".format(path_from)
		return {"status": status, "msg": msg}
	
	if op_type == "ff":
		print("file-file")
		if not os.path.isfile(path_from):
			# print("Path 'from' is not a file: ", path_from)
			# return False
			status = "Error!"
			msg = "Path 'from' is not a file: '{}'".format(path_from)
			return {"status": status, "msg": msg}
		
		if os.path.exists(path_to):
			if not os.path.isfile(path_to):
				# print("Path 'to' is not a file: ", path_to)
				# return False
				status = "Error!"
				msg = "Path 'to' is not a file: '{}'".format(path_to)
				return {"status": status, "msg": msg}
			
			path_from_mtime = int(os.path.getmtime(path_from))
			path_from_mtime = datetime.datetime.fromtimestamp(path_from_mtime)
			path_from_mtime = path_from_mtime.astimezone(tzutc)
			
			path_to_mtime = int(os.path.getmtime(path_to))
			path_to_mtime = datetime.datetime.fromtimestamp(path_to_mtime)
			path_to_mtime = path_to_mtime.astimezone(tzutc)
			
			if path_from_mtime > path_to_mtime:
				print("file-file: rewrite")
				shutil.copy(path_from, path_to)
				
		else:
			f_path, f_name = os.path.split(path_to)
			if f_name == "": # for example, if path_to = 'dir1\dir2\'
				# print("Path 'to' is incorrect: ", path_to)
				# return False
				status = "Error!"
				msg = "Path 'to' is incorrect: '{}'".format(path_to)
				return {"status": status, "msg": msg}
			
			if os.path.exists(f_path):
				if not os.path.isdir(f_path):
					# print("Path: '" + f_path + "' is not a directory to write file: '" + f_name + "'. \n(May be '" + os.path.basename(f_path) + "' it is already existing file?)")
					# return False
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
		pass
	elif op_type == "df":
		print("dir-file")
		# print("Write directory to file? Are you really? It doesn't make sense. =)")
		# return False
		status = "Error!"
		msg = "Write directory to file? Are you really? It doesn't make sense. =)"
		return {"status": status, "msg": msg}
		
	elif op_type == "dd":
		print("dir-dir")
		pass
	else:
		# print("Operation type is undefined: ", op_type)
		# return False
		status = "Error!"
		msg = "Operation type is undefined: '{}'".format(op_type)
		return {"status": status, "msg": msg}
		
	# file-file:
	# if os.path.isfile(path_from):
		# path_from_mtime = int(os.path.getmtime(path_from))
		# path_from_mtime = datetime.datetime.fromtimestamp(path_from_mtime)
		# path_from_mtime = path_from_mtime.astimezone(tzutc)
		
		# if os.path.exists(path_to):
			# if os.path.isfile(path_to):
				# print("file-file")
				# path_to_mtime = int(os.path.getmtime(path_to))
				# path_to_mtime = datetime.datetime.fromtimestamp(path_to_mtime)
				# path_to_mtime = path_to_mtime.astimezone(tzutc)
				
				# if path_from_mtime > path_to_mtime:
					# print("file-file: rewrite")
					# shutil.copy(path_from, path_to)
			
			# file-dir:
			# elif os.path.isdir(path_to):
				# print("file-dir")
				# file_name = os.path.basename(path_from)
				# p = os.path.join(path_to, file_name)
				# p = os.path.normpath(p)
				# print(p)
				
				# if os.path.exists(p):
					# p_mtime = int(os.path.getmtime(p))
					# p_mtime = datetime.datetime.fromtimestamp(p_mtime)
					# p_mtime = p_mtime.astimezone(tzutc)
					
					# if path_from_mtime > p_mtime:
						# print("file-dir: rewrite")
						# shutil.copy(path_from, p)
						
				# else:
					# print("file-dir: write")
					# shutil.copy(path_from, p)
					
		# else:
			# !!! если путь_куда - файл, то создаст каталог с именем этого файла (неправильно)
			# решил сделать другую версию(ветку) с третьим параметром, указывающим тип путей (ff, fd, df, dd)
			# мне кажется так будет более очевидное поведение программы и явная остановка, при ошибке ввода.
			# print("file-dir: create path and write")
			# os.makedirs(path_to)
			# file_name = os.path.basename(path_from)
			# p = os.path.join(path_to, file_name)
			# p = os.path.normpath(p)
			# print(p)
			# shutil.copy(path_from, p)
			
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

a = copy_with_replace_by_date(dir_from_f1, dir_to_d3_f1, "ff")
print(a)
