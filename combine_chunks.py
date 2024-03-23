import os
import shutil

def merge_all(dir):
    merged_dir = os.path.join(dir, "merged")
    if not os.path.exists(merged_dir):
        os.mkdir(merged_dir)
    for dir_name in os.listdir(dir):
        dir_path = os.path.join(dir, dir_name)
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir, dir_name, file_name)
            new_file_path = os.path.join(merged_dir, file_name)
            if os.path.exists(new_file_path):
                continue
            shutil.copyfile(file_path, new_file_path)

merge_all('data/hw')
merge_all('data/no_hw')
