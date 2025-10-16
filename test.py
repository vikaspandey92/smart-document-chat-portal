# #Testing document ingestion and analysis using a PDFHandler and DocumentAnalyzer

# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler       
# from src.document_analyzer.data_analysis import DocumentAnalyzer  

# # Path to the PDF you want to test
# PDF_PATH = r"/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/document_analyzer/attention_is_all_you_need.pdf"

# # Dummy file wrapper to simulate uploaded file (Streamlit style)
# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()

# def main():
#     try:
#         # ---------- STEP 1: DATA INGESTION ----------
#         print("Starting PDF ingestion...")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler = DocumentHandler(session_id="test_ingestion_analysis")
        
#         saved_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")

#         # ---------- STEP 2: DATA ANALYSIS ----------
#         print("Starting metadata analysis...")
#         analyzer = DocumentAnalyzer()  # Loads LLM + parser
        
#         analysis_result = analyzer.analyze_document(text_content)

#         # ---------- STEP 3: DISPLAY RESULTS ----------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test failed: {e}")

# if __name__ == "__main__":
#     main()

# Testing document comparison using DocumentIngestion and DocumentComparatorLLM
# import io
# from pathlib import Path
# from src.document_comparison.data_ingestion import DocumentIngestion
# from src.document_comparison.document_comparator import DocumentComparatorLLM

# # ---- Setup: Load local PDF files as if they were "uploaded" ---- #
# def load_fake_uploaded_file(file_path: Path):
#     return io.BytesIO(file_path.read_bytes())  

# # ---- Step 1: Save and combine PDFs ---- #
# def test_compare_documents():
#     ref_path = Path("/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/document_comparison/Long_Report_V1.pdf")
#     act_path = Path("/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/document_comparison/Long_Report_V2.pdf")

#     class SimulateUpload:
#         def __init__(self, file_path: Path):
#             self.name = file_path.name
#             self._buffer = file_path.read_bytes()

#         def getbuffer(self):
#             return self._buffer

#     # Instantiate
#     comparator = DocumentIngestion()
#     ref_upload = SimulateUpload(ref_path)
#     act_upload = SimulateUpload(act_path)

#     # Save files and combine
#     ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
#     combined_text = comparator.combine_documents()
#     comparator.clean_old_sessions(keep_latest=3)

#     print("\n Combined Text Preview (First 1000 chars):\n")
#     print(combined_text[:1000])

#     # ---- Step 2: Run LLM comparison ---- #
#     llm_comparator = DocumentComparatorLLM()
#     df = llm_comparator.compare_documents(combined_text)
    
#     print("\n Comparison DataFrame:\n")
#     print(df.head())
        
# if __name__ == "__main__":
#     test_compare_documents()

# Testing ConversationalRAG with a FAISS retriever
# import sys
# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH = Path("faiss_index")

# def test_conversational_rag(pdf_path:str, question:str):
#     try:
#         model_loader = ModelLoader()
#         if FAISS_INDEX_PATH.exists():
#             print("Loading existing FAISS retriever...")
#             embeddings = model_loader.load_embeddings()
#             vector_store = FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings, allow_dangerous_deserialization=True)
#             retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
#         else:
#             print("Ingesting document and creating FAISS retriever...")
#             with open(pdf_path, "rb") as f:
#                 uploaded_files = [f]
#                 ingestor = SingleDocIngestor()
#                 retriever = ingestor.ingest_files(uploaded_files)
#         print("Running Conversational RAG...")
#         rag = ConversationalRAG(session_id="test_conversational_rag", retriever=retriever)
#         response = rag.invoke(question)
#         print(f"\nQuestion: {question}\n")
#         print(f"Answer: {response}\n")
#     except Exception as e:
#         print(f"Test failed: {e}")
#         sys.exit(1)

# if __name__ == "__main__":
#     PDF_PATH = r"/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/single_document_chat/attention_is_all_you_need.pdf"
#     QUESTION = "What is the significance of the attention mechanism? can you explain it in simple terms?"
#     if not Path(PDF_PATH).exists():
#         print(f"PDF file does not exist: {PDF_PATH}")
#         sys.exit(1)
#     test_conversational_rag(PDF_PATH, QUESTION)

# Testing MultiDocumentChat with FAISS retriever
import sys
from pathlib import Path
from src.multi_document_chat.data_ingestion import DocumentIngestor
from src.multi_document_chat.retrieval import ConversationalRAG
from utils.model_loader import ModelLoader
def test_multi_document_chat_rag():
    try:
        test_files = [
            r"/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/muti_document_chat/attention_is_all_you_need.pdf",
            r"/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/muti_document_chat/llama2_paper.pdf",
            r"/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/muti_document_chat/market_analysis_report.docx",
            r"/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/muti_document_chat/state_of_the_union.txt"]
        
        uploaded_files = []
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))
            else:
               print(f"File does not exist: {file_path}")

        ingestor = DocumentIngestor()
        retriver = ingestor.ingest_files(uploaded_files)
        for f in uploaded_files:
            f.close()
        session_id = "test_multi_document_chat_rag"
        rag = ConversationalRAG(session_id=session_id, retriever=retriver)
        questions = "Explain the attention mechanism in simple terms."  
        answer = rag.invoke(questions)
        print(f"\nQuestion: {questions}\n")
        print(f"Answer: {answer}\n")   
        
        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_multi_document_chat_rag()