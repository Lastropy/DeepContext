import os
import shutil
class FileUtils: 
    def delete_directory_if_exists(directory_path: str):
        try:
            if os.path.exists(directory_path): 
                shutil.rmtree(directory_path)
        except Exception as e:
            raise Exception(f"Error deleting directory {directory_path}: {e}")

    def create_directory(directory_path: str):
        try:
            os.makedirs(directory_path, exist_ok=True)
        except Exception as e:
            raise Exception(f"Error creating directory {directory_path}: {e}")

    def format_directory(self, directory_path: str):
        try:
            self.delete_directory_if_exists(directory_path)
            self.create_directory(directory_path)
        except Exception as e:
            raise Exception(f"Error formatting directory {directory_path}: {e}")

    def save_file(file, file_path):
        try:
            file.save(file_path)
        except Exception as e:
            raise Exception(f"Error saving file {file_path}: {e}")

    def persist_files_in_directory(self,file_objects, save_documents_directory):
        try:
            for file_object in file_objects:
                if not file_object.filename:
                    raise ValueError("No filename given.")
                file_path = os.path.join(save_documents_directory, file_object.filename)
                self.save_file(file_object, file_path)
        except Exception as e:
            raise Exception(f"Error saving files in {save_documents_directory}: {e}")