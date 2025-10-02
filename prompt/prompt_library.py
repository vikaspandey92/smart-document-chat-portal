from langchain_core.prompts import ChatPromptTemplate

document_analysis_prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant trained to analyze and summarize documents.
    Return ONLY the JSON response as specified below.
    {format_instructions}
    Analyze this document:
    {document_text}""")

document_comparison_prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant trained to compare and contrast documents.
    1. Compare the content in both documents.
    2. Highlight the differences in the documents and note down the page number.
    3. The output you provide must be page-wise comparison.
    4. If the documents are identical, simply state "The documents are identical."
    
    Input Documents:
    {combined_documents}
    Return ONLY the JSON response as specified below.
    {format_instructions}""")

PROMPT_REGISTERY = {
    "document_analysis": document_analysis_prompt,
    "document_comparison": document_comparison_prompt,
}