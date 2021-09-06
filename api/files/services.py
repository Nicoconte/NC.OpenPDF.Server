from os import stat
from .models import File

class FileService:


    @staticmethod
    def save(user, filename, path, storage):
        file = File.objects.create(
            user       = user,
            filename   = filename,
            path       = path,
            extension  = storage.get_file_extension(filename),
            size       = storage.calculate_file_size(filename)
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
                    user      = user,
                    filename  = filename,
                    path      = storage.full_path,
                    extension = storage.get_file_extension(filename),
                    size      = FileService.get_single_blob_file_size(file)  
                )

                success.append({
                    "id": fileObj.id,
                    "filename": fileObj.filename,
                    "extension": fileObj.extension,
                    "path": fileObj.path,
                    "size": fileObj.size,
                    "uploaded_at": fileObj.uploaded_at
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
    def get_blob_files_size(files):
        return sum([f.size for f in files]) // (1024 ** 2)

    @staticmethod
    def get_single_blob_file_size(file):
        return file.size // (1024 ** 2)    