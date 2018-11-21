
# import sys
# import yadisk
import os
import datetime
from dateutil.tz import tzutc
import shutil

tzutc = tzutc()

local_path_1 = r"test_dir_1\myfile.txt"
local_path_2 = r"test_dir_2\myfile.txt"

def copy_with_replace_by_date(path_from, path_to):
	if not os.path.exists(path_from):
		print("Path 'from' not found!")
		return False
	
	if os.path.isfile(path_from):
		path_from_date_mod = int(os.path.getmtime(path_from))
		path_from_date_mod = datetime.datetime.fromtimestamp(path_from_date_mod)
		path_from_date_mod = path_from_date_mod.astimezone(tzutc)
		
		if os.path.exists(path_to):
			if os.path.isfile(path_to):		
				path_to_date_mod = int(os.path.getmtime(path_to))
				path_to_date_mod = datetime.datetime.fromtimestamp(path_to_date_mod)
				path_to_date_mod = path_to_date_mod.astimezone(tzutc)
				
				if path_from_date_mod > path_to_date_mod:
					print("rewrite")
					shutil.copy(path_from, path_to)
			
	return True
		
a = copy_with_replace_by_date(local_path_1, local_path_2)	
print(a)
