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

import io
from pathlib import Path
from src.document_comparison.data_ingestion import DocumentIngestion
from src.document_comparison.document_comparator import DocumentComparatorLLM

# ---- Setup: Load local PDF files as if they were "uploaded" ---- #
def load_fake_uploaded_file(file_path: Path):
    return io.BytesIO(file_path.read_bytes())  

# ---- Step 1: Save and combine PDFs ---- #
def test_compare_documents():
    ref_path = Path("/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/document_comparison/Long_Report_V1.pdf")
    act_path = Path("/Users/vikaspandey/learning/GenAI/projects/smart-document-chat-portal/data/document_comparison/Long_Report_V2.pdf")

    class SimulateUpload:
        def __init__(self, file_path: Path):
            self.name = file_path.name
            self._buffer = file_path.read_bytes()

        def getbuffer(self):
            return self._buffer

    # Instantiate
    comparator = DocumentIngestion()
    ref_upload = SimulateUpload(ref_path)
    act_upload = SimulateUpload(act_path)

    # Save files and combine
    ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = comparator.combine_documents()
    comparator.clean_old_sessions(keep_latest=3)

    print("\n Combined Text Preview (First 1000 chars):\n")
    print(combined_text[:1000])

    # ---- Step 2: Run LLM comparison ---- #
    llm_comparator = DocumentComparatorLLM()
    df = llm_comparator.compare_documents(combined_text)
    
    print("\n Comparison DataFrame:\n")
    print(df.head())
        
if __name__ == "__main__":
    test_compare_documents()
    