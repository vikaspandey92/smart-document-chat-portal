import sys
from pathlib import Path
import uuid
from datetime import datetime, timezone
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self, base_dir: str = "data/document_comparison", session_id=None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.log.info("DocumentIngestion initialized successfully", session_id=self.session_id, path=str(self.session_path))

        
    def save_uploaded_files(self, reference_file, actual_file):
        """Saves the uploaded file to the specified directory."""
        try:
            ref_path = self.session_path / reference_file.name
            actual_path = self.session_path / actual_file.name
            
            if not reference_file.name.lower().endswith('.pdf') or not actual_file.name.lower().endswith('.pdf'):
                raise ValueError("Only PDF files are supported.")
            
            with open(ref_path, 'wb') as f:
                f.write(reference_file.getbuffer())

            with open(actual_path, 'wb') as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files saved", reference=str(ref_path), actual=str(actual_path), session_id=self.session_id)
            return ref_path, actual_path

        except Exception as e:
            self.log.error("Error in save_uploaded_file:", error = str(e), session_id=self.session_id)
            raise DocumentPortalException("An error occured while saving files", sys)
        
    def read_pdf(self, pdf_path: Path) -> str:
        """Reads a PDF file and extracts its text content."""
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        all_text.append(f"\n --- Page {page_num + 1} ---\n{text}")
                self.log.info("Extracted text from PDF successfully", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.log.error("Error in read_pdf:", error = str(e), file=str(pdf_path))
            raise DocumentPortalException("An error occured while reading PDF file", sys)
        
    def combine_documents(self) -> str:
        """Combines the text content of two documents."""
        try:
            doc_parts = []
            for file in sorted(self.session_path.iterdir()):
                if file.is_file() and file.suffix.lower() == '.pdf':
                  content = self.read_pdf(file)
                  doc_parts.append(f"Document: {file.name}\n{content}")
            
            combined_text = "\n\n".join(doc_parts)
            self.log.info("Combined documents successfully", count=len(doc_parts), session_id=self.session_id)
            return combined_text
        except Exception as e:
            self.log.error("Error in combine_documents", error = str(e), session_id=self.session_id)
            raise DocumentPortalException("An error occured while combining documents", sys)
        
    def clean_old_sessions(self, keep_latest: int = 3):
        """Cleans up old session directories, keeping only the latest N sessions."""
        try:
            session_folders = sorted([d for d in self.base_dir.iterdir() if d.is_dir()], reverse=True)
            for folder in session_folders[keep_latest:]:
                for file in folder.iterdir():
                        file.unlink()
                folder.rmdir()
                self.log.info("Deleted old session", path=str(folder))
        except Exception as e:
            self.log.error("Error in clean_old_sessions", error = str(e))
            raise DocumentPortalException("An error occured while cleaning old sessions", sys)
    