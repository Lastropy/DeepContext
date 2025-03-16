import os
import shutil
from typing import List
from werkzeug.datastructures import FileStorage

class FileUtils:
    """
    Utility class for file and directory operations.
    """
    
    @staticmethod
    def delete_directory_if_exists(directory_path: str) -> None:
        """
        Deletes a directory if it exists.

        Args:
            directory_path (str): Path to the directory.
        """
        try:
            if os.path.exists(directory_path): 
                shutil.rmtree(directory_path)
        except Exception as e:
            raise Exception(f"Error deleting directory {directory_path}: {e}")
    
    @staticmethod
    def create_directory(directory_path: str) -> None:
        """
        Creates a directory if it does not exist.

        Args:
            directory_path (str): Path to the directory.
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
        except Exception as e:
            raise Exception(f"Error creating directory {directory_path}: {e}")
    
    def format_directory(directory_path: str) -> None:
        """
        Deletes and then recreates a directory.

        Args:
            directory_path (str): Path to the directory.
        """
        try:
            FileUtils.delete_directory_if_exists(directory_path)
            FileUtils.create_directory(directory_path)
        except Exception as e:
            raise Exception(f"Error formatting directory {directory_path}: {e}")
    
    @staticmethod
    def save_file(file: FileStorage, file_path: str) -> None:
        """
        Saves an uploaded file to the given file path.

        Args:
            file (FileStorage): The file object to be saved.
            file_path (str): Path where the file should be saved.
        """
        try:
            file.save(file_path)
        except Exception as e:
            raise Exception(f"Error saving file {file_path}: {e}")
    
    def persist_files_in_directory(file_objects: List[FileStorage], save_documents_directory: str) -> None:
        """
        Saves multiple uploaded files in a specified directory.

        Args:
            file_objects (List[FileStorage]): List of file objects to save.
            save_documents_directory (str): Directory where files should be saved.
        """
        try:
            for file_object in file_objects:
                if not file_object.filename:
                    raise ValueError("No filename given.")
                file_path = os.path.join(save_documents_directory, file_object.filename)
                FileUtils.save_file(file_object, file_path)
        except Exception as e:
            raise Exception(f"Error saving files in {save_documents_directory}: {e}")
