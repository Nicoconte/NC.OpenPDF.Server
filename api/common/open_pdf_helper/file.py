import os

from uuid import uuid4

class File:
    def __init__(self):
        self._filename = ""

    def _rename_file(self, name: str) -> str:
        return f"{name.split('.pdf')[0]}_{uuid4()}.pdf"
    
    def _exists(self, dir:str, name: str) -> bool:
        files = os.listdir(dir)
        return name in files         

