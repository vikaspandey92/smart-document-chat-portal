from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant trained to analyze and summarize documents.
    Return ONLY the JSON response as specified below.
    {format_instructions}
    Analyze this document:
    {document_text}""")