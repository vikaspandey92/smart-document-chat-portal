import os
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputparser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    '''analyzes the document and extracts relevant information'''
    def __init__(self):
        pass
    
    def analyze_document(self):
        pass
