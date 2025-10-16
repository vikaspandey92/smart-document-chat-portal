import uuid
from pathlib import Path
import sys
from datetime import datetime, timezone
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

class DocumentIngestor:
    '''Class to handle document ingestion, processing, and vector store creation.'''
    SUPPORTED_FILE_TYPES = ['.txt', '.pdf', '.docx', '.md']
    def __init__(self, temp_dir:str='data/muti_document_chat', faiss_dir:str='faiss_index', session_id:str | None = None):
        try:
            self.log = CustomLogger().get_logger()
            # initializing directories
            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            # Initializing session directories
            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)

            self.model_loader = ModelLoader()
            self.log.info("DocumentIngestor initialized successfully", 
                          session_id=self.session_id,
                          temp_base_dir=str(self.temp_dir),
                          faiss_base_dir=str(self.faiss_dir),
                          temp_dir=str(self.session_temp_dir),
                          faiss_dir=str(self.session_faiss_dir))
        except Exception as e:
            self.log.error("Error in initializing DocumentIngestor", error = str(e))
            raise DocumentPortalException("Initialization error in DocumentIngestor", sys)



    def ingest_files(self, uploaded_files):
        '''Ingest and process uploaded files, returning a FAISS retriever.'''
        try:
            documents = []
            for file in uploaded_files:
                file_extension = Path(file.name).suffix.lower()
                if file_extension not in self.SUPPORTED_FILE_TYPES:
                    self.log.warning("Unsupported file type", file_name=file.name)
                    continue
                
                unique_file_name = f"{uuid.uuid4().hex[:8]}{file_extension}"
                temp_file_path = self.session_temp_dir / unique_file_name

                # Save uploaded file to temp directory
                with open(temp_file_path, 'wb') as f:
                    f.write(file.read())
                self.log.info("Saved uploaded file", file_name=file.name, saved_path=str(temp_file_path), session_id=self.session_id)
                
                # Load document based on file type
                if file_extension == '.pdf':
                    loader = PyPDFLoader(str(temp_file_path))
                elif file_extension == '.docx':
                    loader = Docx2txtLoader(str(temp_file_path))
                elif file_extension in ['.txt', '.md']:
                    loader = TextLoader(str(temp_file_path), encoding='utf8')
                else:
                    self.log.warning("No loader available for file type", file_name=file.name)
                    continue
                
                docs = loader.load()
                documents.extend(docs)
            if not documents:
                raise DocumentPortalException("No  valid documents loaded from the file", sys)
            self.log.info(f"Loaded {len(docs)} documents from {file.name}", file_name=file.name)
            return self._create_retriever(documents)
        except Exception as e:
            self.log.error("Error in ingest_files", error = str(e))
            raise DocumentPortalException("Error in ingesting files", sys)
        
    def _create_retriever(self, documents):
        '''Process documents, create embeddings, and return a FAISS retriever.'''
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(documents)
            self.log.info("Split documents into chunks", total_chunks = len(chunks), session_id=self.session_id)
            embeddings = self.model_loader.load_embeddings()
            vector_store = FAISS.from_documents(chunks, embeddings)

            # save FAISS index as session
            vector_store.save_local(str(self.session_faiss_dir))
            self.log.info("Created and saved FAISS vector store", faiss_path=str(self.session_faiss_dir), session_id=self.session_id)
            return vector_store.as_retriever(search_type = 'similarity', search_kwargs={"k": 5})
        except Exception as e:
            self.log.error("Error in _create_retriever", error = str(e))
            raise DocumentPortalException("Error in creating retriever", sys)