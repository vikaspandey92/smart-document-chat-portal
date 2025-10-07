from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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

contextualize_question_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given a conversation history and the most recent user query, rewrite the query as a standalone question "
        "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
        "question if necessary; otherwise, return it unchanged."
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

context_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an assistant designed to answer questions using the provided context. Rely only on the retrieved "
        "information to form your response. If the answer is not found in the context, respond with 'I don't know.' "
        "Keep your answer concise and no longer than three sentences.\n\n{context}"
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

PROMPT_REGISTERY = {
    "document_analysis": document_analysis_prompt,
    "document_comparison": document_comparison_prompt,
    "contextualize_question": contextualize_question_prompt,
    "context_qa": context_qa_prompt  
}