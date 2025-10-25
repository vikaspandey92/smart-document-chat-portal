import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import Metadata, PromptType
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTERY

class DocumentAnalyzer:
    '''analyzes the document and extracts relevant information'''
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            # prepare parsers
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(llm=self.llm, parser=self.parser)
            # preparing prompt
            self.prompt = PROMPT_REGISTERY[PromptType.DOCUMENT_ANALYSIS.value]
            self.log.info("DocumentAnalyzer initialized successfully")

        except Exception as e:
            self.log.error(f"Error in initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Error in initializing DocumentAnalyzer", sys)
    
    def analyze_document(self, document_text: str) -> dict:
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("metadata extraction chain created successfully")
            response = chain.invoke({"document_text": document_text, 
                                    "format_instructions": self.parser.get_format_instructions()})
            self.log.info("Metadata extraction successfully", keys=list(response.keys()))
            return response
        except Exception as e:
            self.log.error(f"Metadata extraction failed", error=str(e))
            raise DocumentPortalException("Metadata extraction failed") from e
        
