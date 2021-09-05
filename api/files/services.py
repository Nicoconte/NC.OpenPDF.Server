from os import stat
from .models import File

class FileService:


    @staticmethod
    def save(user, filename, path):
        file = File.objects.create(
            user = user,
            filename = filename,
            path = path    
        )
        
        return file if file is not None else None

    @staticmethod
    def save_many(user, files, storage):
        success = []
        error   = []

        for file in files:
            filename = storage.save_file_into_folder(file)

            #TODO: Seria mejor que un servicio se encargue de esto?            
            try:
                fileObj = File.objects.create(
                    user     = user,
                    filename = filename,
                    path     = storage.full_path 
                )

                success.append({
                    "id": fileObj.id,
                    "filename": fileObj.filename.lower(),
                    "extension": fileObj.filename.split(".")[1],
                    "path": fileObj.path
                })
                
            except Exception as e:
                error.append({
                    "filename": filename,
                    "reason": "file already exists",
                    "inner_reason": str(e)
                })        

        return success, error

    
    @staticmethod
    def find_by_id(id):
        try:
            return File.objects.get(id=id)
        except:
            return None

    @staticmethod
    def find_all(user):
        return File.objects.filter(user=user)

    @staticmethod
    def delete(id):
        try:
            return File.objects.get(id=id).delete()
        except:
            return None


    @staticmethod
    def build_files_fullpath(files_id):
        files_path = []

        for id in files_id:
            file = FileService.find_by_id(id)
            if file:
                files_path.append(f"{file.path}/{file.filename}")
        
        return files_path        

    @staticmethod
    def delete_all(user):
        return File.objects.filter(user=user).delete()


    @staticmethod
    def find_file_by_unique_name(filename):
        try:
            return File.objects.get(filename=filename)
        except:
            return None


    @staticmethod
    def calculate_files_size(files):
        return sum([f.size for f in files]) // (1024 ** 2)