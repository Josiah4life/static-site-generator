import os
import shutil

def copy_directory_recursive(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
        print(f"Created directory: {dest}")
        
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
            
        else:
            copy_directory_recursive(src_path, dest_path)