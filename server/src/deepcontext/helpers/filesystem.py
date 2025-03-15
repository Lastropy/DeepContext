import os
import shutil

def delete_directory_if_exists(directory_path: str):
    if os.path.exists(directory_path): 
       shutil.rmtree(directory_path)

def create_directory(directory_path: str):
    os.makedirs(directory_path)

def update_directory(directory_path: str):
    delete_directory_if_exists(directory_path)
    create_directory(directory_path)

def save_file(file, file_path):
    file.save(file_path)

def persist_files_in_directory(file_objects, save_documents_directory):
    for file_object in file_objects:
        if file_object.filename == "":
            raise Exception("No filename given.")
        file_path = os.path.join(save_documents_directory, file_object.filename)
        save_file(file_object, file_path)