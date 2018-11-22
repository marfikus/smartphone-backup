
# import sys
# import yadisk
import os
import datetime
from dateutil.tz import tzutc
import shutil

tzutc = tzutc()

def copy_with_replace_by_date(path_from, path_to):
	if not os.path.exists(path_from):
		print("Path 'from' not found!")
		return False
	
	# file-file:
	if os.path.isfile(path_from):
		path_from_mtime = int(os.path.getmtime(path_from))
		path_from_mtime = datetime.datetime.fromtimestamp(path_from_mtime)
		path_from_mtime = path_from_mtime.astimezone(tzutc)
		
		if os.path.exists(path_to):
			if os.path.isfile(path_to):
				print("file-file")
				path_to_mtime = int(os.path.getmtime(path_to))
				path_to_mtime = datetime.datetime.fromtimestamp(path_to_mtime)
				path_to_mtime = path_to_mtime.astimezone(tzutc)
				
				if path_from_mtime > path_to_mtime:
					print("file-file: rewrite")
					shutil.copy(path_from, path_to)
			
			# file-dir:
			elif os.path.isdir(path_to):
				print("file-dir")
				file_name = os.path.basename(path_from)
				p = os.path.join(path_to, file_name)
				p = os.path.normpath(p)
				# print(p)
				
				if os.path.exists(p):
					p_mtime = int(os.path.getmtime(p))
					p_mtime = datetime.datetime.fromtimestamp(p_mtime)
					p_mtime = p_mtime.astimezone(tzutc)
					
					if path_from_mtime > p_mtime:
						print("file-dir: rewrite")
						shutil.copy(path_from, p)
						
				else:
					print("file-dir: write")
					shutil.copy(path_from, p)
					
		else:
			# !!! если путь_куда - файл, то создаст каталог с именем этого файла (неправильно)
			# решил сделать другую версию(ветку) с третьим параметром, указывающим тип путей (ff, fd, df, dd)
			# мне кажется так будет более очевидное поведение программы и явная остановка, при ошибке ввода.
			print("file-dir: create path and write")
			os.makedirs(path_to)
			file_name = os.path.basename(path_from)
			p = os.path.join(path_to, file_name)
			p = os.path.normpath(p)
			# print(p)
			shutil.copy(path_from, p)
			
	return True

dir_from_f1 = r"test_dir_from\myfile.txt"
dir_from_f2 = r"test_dir_from\myfile2.txt"
dir_to_f1 = r"test_dir_to\myfile.txt"
dir_from = r"test_dir_from"
dir_to = r"test_dir_to"
dir_to_d3 = r"test_dir_to\dir_3"

a = copy_with_replace_by_date(dir_from_f1, dir_to_f1)	
print(a)
