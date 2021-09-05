import uuid 
import random

def create_password():
    try:
        base_password = uuid.uuid4().hex[:8]
        base_len = len(base_password) 

        final_password = ""

        random_lower = random.randint(0, 1)

        for i in range(base_len):
            if random_lower == 1 and base_password[i].isalpha:
                final_password += base_password[i].lower()
            else:
                final_password += base_password[i].upper()

            random_lower = random.randint(0, 1)

        return final_password
    
    except Exception as e:    
        print(str(e))                  