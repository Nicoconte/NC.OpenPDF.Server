from django.conf import settings
from django.core.files.storage import FileSystemStorage

from typing import IO

import os

class Storage:

    def __init__(self, foldername = None):

        self.foldername = foldername
        self.full_path  = None
        self.fileSystem = None

        if foldername != None:
            self.full_path = f"{settings.MEDIA_ROOT}{foldername}"
            self.fileSystem = FileSystemStorage(self.full_path)    

    def init(self, foldername):
        self.foldername = foldername
        self.full_path  = f"{settings.MEDIA_ROOT}{self.foldername}"
        self.fileSystem = FileSystemStorage(self.full_path)    
            

    @staticmethod
    def build_path(foldername):
        return f"{settings.MEDIA_ROOT}{foldername}"

    def create_folder(self):
        return os.mkdir(self.full_path)


    def save_file_into_folder(self, file: IO):
        name = file.name

        if (self.fileSystem.exists(name)):
            return None
            
        return self.fileSystem.save(name, file)

    def get_file_blob(self, filename):

        if not self.fileSystem.exists(filename):
            return None

        file_blob = self.fileSystem.open(filename, 'rb')

        return file_blob

    def delete_file(self, filename):        
        if self.fileSystem.exists(filename):
            self.fileSystem.delete(filename)
        
        return not self.fileSystem.exists(filename)

    def clear_dir(self):
        files = os.listdir(self.full_path)

        for file in files:
            os.remove(f"{self.full_path}/{file}")

    def calculate_disk_space(self):        
        size = 0
        files = os.listdir(self.full_path)
        
        for file in files:
            size += os.path.getsize(f"{self.full_path}/{file}")

        return size // (1024*1024) 
