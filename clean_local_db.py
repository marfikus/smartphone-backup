
import os
import pickle

def clean_local_db():
	file_name_local_db = "local_db"
	
	if not os.path.exists(file_name_local_db):
		print("File db not exists!", file_name_local_db)
		return False
		
	f = open(file_name_local_db, "rb")
	local_db = pickle.load(f)
	f.close()
	
	local_db_clean = {}
	for path in local_db:
		# print(path)
		if os.path.exists(path):
			local_db_clean[path] = local_db[path]
		else:
			print(path)
			
	f = open(file_name_local_db, "wb")
	pickle.dump(local_db_clean, f)
	f.close()
	
	return True
	
clean_local_db()