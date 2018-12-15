
# rename file before use: 'my_input_data_template.py' > 'my_input_data.py'

list_of_paths = [
# structure hint: [path_from, path_to, op_type("ff"|"fd"|"df"|"dd")]
# [r"/dir1/dir2", r"/dir3", "dd"]
]

set_of_ignored_paths = {
# structure hint: path_from
# r"/dir1/dir2",
# r"dir\myfile.txt",
}
