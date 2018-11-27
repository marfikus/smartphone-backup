
import shutil
import smartphone_backup_test as sbt

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

# a = copy_with_replace_by_date(dir_from_f1, dir_to_d3_f1, "ff")
# print(a)

def test_df():
	res = sbt.copy_with_replace_by_date(r"test_dir_from\myfile.txt", r"test_dir_to\myfile.txt", "df")
	if not res["status"] == "Error!":
		return False
	if not res["msg"] == "Write directory to file? Are you really? It doesn't make sense. =)":
		return False
	return True
	

print("========================================")
if test_df():
	print("test_df: passed")
else:
	print("test_df: FAILED!")
print("========================================")