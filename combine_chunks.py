import os
import shutil
import splitfolders

def merge_all(dir, class_name, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    class_path = os.path.join(dir, class_name)
    for dir_name in os.listdir(class_path):
        dir_path = os.path.join(dir, class_name, dir_name)
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir, class_name, dir_name, file_name)
            new_file_path = os.path.join(dst, file_name)
            if os.path.exists(new_file_path):
                continue
            shutil.copyfile(file_path, new_file_path)

merge_all('data', 'hw', 'data/merged/hw')
merge_all('data', 'no_hw', 'data/merged/no_hw')

splitfolders.ratio('data/merged', output="data/split", seed=1337, ratio=(.8, 0.1,0.1)) 