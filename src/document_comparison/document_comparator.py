import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTERY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(llm=self.llm, parser=self.parser)
        self.prompt = PROMPT_REGISTERY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser 
        self.log.info("DocumentComparator initialized successfully.")

    def compare_documents(self, combined_docs: str) -> pd.DataFrame:
        """Compares two documents and returns the differences."""
        try:
            inputs = {"combined_documents" : combined_docs,
                      "format_instructions": self.parser.get_format_instructions()}
            self.log.info("Starting document comparison", inputs=inputs)
            response = self.chain.invoke(inputs)
            self.log.info("Chain invoked successfully", response=response)
            return self._format_response(response)
            
        except Exception as e:
            self.log.error(f"Error in compare_documents: {e}")
            raise DocumentPortalException("An error occured while comparing documents", sys)

    def _format_response(self, response: list[dict]) -> pd.DataFrame:
        """Formats the comparison response."""
        try:
            df = pd.DataFrame(response)
            self.log.info("Response formatted successfully", dataframe=df)
            return df
        except Exception as e:
            self.log.error(f"Error in response formatting: {e}")
            raise DocumentPortalException("An error occured while formatting response", sys)