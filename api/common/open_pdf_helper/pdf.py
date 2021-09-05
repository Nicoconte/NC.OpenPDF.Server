from PyPDF2 import PdfFileReader, PdfFileWriter

from .file import File

class PDF(File):

    def __init__(self, output_dir):
        File.__init__(self)
        self.__pdf_writer = PdfFileWriter()        
        self.__output_dir = output_dir

    def __save(self):
        if self._exists(self.__output_dir, self._filename):
            self._filename = self._rename_file(self._filename)

        with open(f"{self.__output_dir}/{self._filename}", 'wb') as out:
            self.__pdf_writer.write(out)            

        return self._exists(self.__output_dir, self._filename)

    def __copy(self, pdf):
        """
            Create a new PDF with the pages of the current (given) pdf
        """
        for index in range(pdf.getNumPages()):
            self.__pdf_writer.addPage(pdf.getPage(index))


    def merge(self, pdf_files: list, name="Convertido_por_OpenPDF.pdf") -> bool:        
        
        if len(pdf_files) < 2:
            return False

        self._filename = name
        
        try:
            for pdf in pdf_files:
                current_pdf = PdfFileReader(pdf)

                self.__copy(current_pdf)

            return self.__save()

        except Exception as e:
            print(f"Cannot merge -> {str(e)}")

    
    def encrypt(self, pdf_file: str, password: str, name="Encriptado_por_OpenPDF.pdf") -> bool:
        self._filename = name

        current_pdf = PdfFileReader(pdf_file)
        try:
            
            self.__copy(current_pdf)

            self.__pdf_writer.encrypt(password)

            return self.__save()

        except Exception as e:
            print(f"Cannot encrypt {str(e)}")

    def decrypt(self, pdf_file: str, password: str, name="Desencriptado_por_OpenPDF.pdf") -> bool:
        self._filename = name

        current_pdf = PdfFileReader(pdf_file)
        try:
            if current_pdf.isEncrypted:
                current_pdf.decrypt(password)

                self.__copy(current_pdf)

                return self.__save()
            
            return False

        except Exception as e:
            print(f"Cannot decrypt -> {str(e)}")




