import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    '''handles PDF saving and reading operations'''
    def __init__(self, data_dir=None, session_id=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH",
                                                os.path.join(os.getcwd(), "data", "document_analyzer"))
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{str(uuid.uuid4())[:8]}"
            self.session_dir = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_dir, exist_ok=True)
            self.log.info("DocumentHandler initialized", session_id=self.session_id, session_dir = self.session_dir)
        except Exception as e:
            self.log.error(f"Error in initializing DocumentHandler: {e}")
            raise DocumentPortalException("Error in initializing Documenthandler", e) from e  

    def save_pdf(self, uploaded_file=None):
        try:
            file_name = os.path.basename(uploaded_file.name)
            if not file_name.lower().endswith('.pdf'):
                raise DocumentPortalException("Uploaded file is not a PDF", "InvalidFileType")
            save_path = os.path.join(self.session_dir, file_name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            self.log.info(f"PDF saved at {save_path}", file=file_name, session_id=self.session_id)
            return save_path
        except Exception as e:
            self.log.error(f"Error in saving PDF: {e}", session_id=self.session_id)
            raise DocumentPortalException("Error in saving PDF", e) from e

    def read_pdf(self, pdf_path: str) -> str:
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text_chunks.append(f"\n--- Page {page_num} ---\n{page.get_text()}")
                text = "\n".join(text_chunks)
            self.log.info("PDF read successfully", pdf_path = pdf_path, session_id=self.session_id, pages=len(text_chunks))
            return text
            
        except Exception as e:
            self.log.error(f"Error in reading PDF: {e}", session_id=self.session_id)
            raise DocumentPortalException("Error in reading PDF", e) from e
        
if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO

    doc_handler = DocumentHandler()
    pdf_path = "/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/document_analyzer/attention_is_all_you_need.pdf"
    
    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path).name
            self.file_path = file_path
        def getbuffer(self):
            return open(self.file_path, "rb").read()
    dummy_file = DummyFile(pdf_path)
    try:
        saved_path = doc_handler.save_pdf(dummy_file)
        print(saved_path)
        content = doc_handler.read_pdf(saved_path)
        print(content[:500])  # print first 500 characters
    except Exception as e:
        print(f"Error: {e}")    
