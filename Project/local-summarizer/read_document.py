from pathlib import Path
from pypdf import PdfReader

class ReadDocument:
    def __init__(self, file_input):
        self.file_input = file_input

    def read_document(self):
        file_name = str(self.file_input.filename)
        file_suffix = Path(file_name).suffix.lower()

        if file_suffix == ".txt":
            document_bytes = self.file_input.read()
            document_decoded = document_bytes.decode("utf-8")
            return document_decoded
        elif file_suffix == ".pdf":
            reader = PdfReader(self.file_input)
            all_pages = []
            for page in reader.pages:
                extracted_text = page.extract_text()
                all_pages.append(extracted_text)
            str_all_pages = "\n\n".join(all_pages)
            return str_all_pages
            
        elif file_suffix == ".docx":
            print("success")
        else:
            print("error")