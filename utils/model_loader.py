import os
import sys
import json
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    '''Class to load and initialize the model based on configuration.'''
    def __init__(self):
        '''Initialize the ModelLoader with configuration and environment variables.'''
        self.config = load_config()
        load_dotenv()
        self._validate_env()
        log.info("Configuration loaded successfully",  config_keys = list(self.config.keys()))

    def _validate_env(self):
        '''Validate required environment variables.'''
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys = {key: os.getenv(key) for key in required_vars}
        missing_vars = [key for key, value in self.api_keys.items() if not value]
        if missing_vars:
            log.error("Missing required environment variables", missing_vars=missing_vars)
            raise DocumentPortalException("Missing required environment variables", sys)

    def load_embeddings(self):
        '''Load and return the embedding model based on configuration.'''
        try:
            log.info("Loading embedding model...")
            model_name = self.config['embedding_model']['model_name']
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Failed to load embedding model", error=str(e))
            raise DocumentPortalException("Failed to load embedding model", sys)

    def load_llm(self):
        '''Load and return the language model based on configuration.'''
        llm_block = self.config['llm']
        log.info("Loading language model...")
        provider_key = os.getenv("LLM_PROVIDER", "google") # default
        if provider_key not in llm_block:
            log.error("LLM provider not supported", provider=provider_key)
            raise ValueError(f"LLM provider '{provider_key}' not found in configuration")
        
        llm_config = llm_block[provider_key]
        provider = llm_config.get('provider')
        model_name = llm_config.get('model_name')
        temperature = llm_config.get('temperature', 0.2) 
        max_tokens = llm_config.get('max_tokens', 2048)

        log.info("LLM configuration", provider=provider, model_name=model_name, temperature=temperature, max_tokens=max_tokens)

        if provider == "groq":
            return ChatGroq(model=model_name, api_key=self.api_keys["GROQ_API_KEY"], temperature=temperature, max_tokens=max_tokens)
        elif provider == "google":
            return ChatGoogleGenerativeAI(model=model_name, api_key=self.api_keys["GOOGLE_API_KEY"], temperature=temperature, max_output_tokens=max_tokens)
        else:
            log.error("LLM provider not supported", provider=provider)
            raise ValueError(f"LLM provider '{provider}' is not supported")


        
if __name__ == "__main__":
    '''Test the ModelLoader class.'''
    model_loader = ModelLoader()
    embedding_model = model_loader.load_embeddings()
    result = embedding_model.embed_query("Hello, world!")
    log.info("Embedding model loaded successfully", embedding=result)
    llm_model = model_loader.load_llm()
    log.info("Models loaded successfully", embedding_model=str(embedding_model), llm_model=str(llm_model))
    result = llm_model.invoke('Hello, how are you?')
    log.info("LLM invocation result", result=result)
           

