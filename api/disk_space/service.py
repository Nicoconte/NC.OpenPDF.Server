from api.disk_space.models import DiskSpace

class DiskSpaceService:
    
    @staticmethod
    def save(user):
        obj = DiskSpace.objects.create(user=user)
        return obj if obj is not None else None

    @staticmethod
    def get_disk_space_information(user):
        return DiskSpace.objects.get(user=user)

    @staticmethod
    def is_there_space_into_the_disk(user, entry_file_size):
        obj = DiskSpace.objects.get(user=user)
        
        current_space_used = obj.space_used + entry_file_size 

        if current_space_used > obj.limit: 
            return False
        
        return True    
    
    @staticmethod
    def update_disk_space(user, size, new_files=False):
        obj = DiskSpace.objects.get(user=user)
        
        # If the size is from new files, we add to the current size of the folder
        if new_files:
            obj.space_used = obj.space_used + size
            obj.save()
            return 

        #Otherwise, we can say that we delete files so we should set the actual size of the folder
        obj.space_used = size
        obj.save()
        