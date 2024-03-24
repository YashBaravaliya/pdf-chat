import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.llms import Ollama
from src.helper import *
import os
from datetime import datetime


global chat_box

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token + ""
        self.container.markdown(self.text)


def upload_and_process_pdf(file_uploader):
    uploaded_file = file_uploader("Upload PDF file")
    if uploaded_file:
        with open(uploaded_file.name, mode='wb') as w:
            w.write(uploaded_file.getvalue())

        # Load PDF files
        loader = PyPDFLoader(uploaded_file.name)
        documents = loader.load()

        return documents
    else:
        st.warning("Please upload a PDF file")
    return None


def initialize_chatbot(documents, template):
    # Split Text into Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(documents)

    # Load the Embedding Model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cuda'})

    # Convert the Text Chunks into Embeddings and Create a FAISS Vector Store
    vector_store = FAISS.from_documents(text_chunks, embeddings)
    vector_store.save_local("vector_store")

    qa_prompt = PromptTemplate(template=template, input_variables=['context', 'question'])

    # Initialize LangChain components 
    chat_box = st.sidebar.empty()
    stream_handler = initialize_stream_handler(chat_box)
    llm = Ollama(model="rag", callback_manager=CallbackManager([StreamingStdOutCallbackHandler(), stream_handler]))

    memory = ConversationBufferWindowMemory(k=3)

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type='stuff',
                                        retriever=vector_store.as_retriever(search_kwargs={'k': 2}),
                                        return_source_documents=False,
                                        chain_type_kwargs={'prompt': qa_prompt},
                                        memory=memory)

    return chain

def save_chat_history(question, answer):
    current_date = datetime.now().strftime("%d-%m-%Y")
    folder_name = "history"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_name = os.path.join(folder_name, f"chat_history_{current_date}.md")
    with open(file_name, "a") as file:
        file.write(f"**{question}**\n")
        file.write(f"{answer}\n\n{'-'*50}\n\n")

def initialize_stream_handler(container):
    stream_handler = StreamHandler(container)
    return stream_handler




def main():
    st.set_page_config(page_title="Pdf Chatbot 📔")

    st.title("Pdf Chatbot 📔")

    st.sidebar.title("Upload PDF")

    documents = upload_and_process_pdf(st.sidebar.file_uploader)

    if documents:
        chat_history = st.session_state.get("chat_history", [])
        st.session_state.chat_history = chat_history

        chain = initialize_chatbot(documents, template)

        # Display conversation history
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(message.content)

        # Handle user input and bot response
        user_query = st.chat_input("Your Message")
        if user_query is not None and user_query != "":
            st.session_state.chat_history.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)

            
            with st.chat_message("AI"):
    
                ai_response = chain({'query': user_query})['result']
                st.markdown(ai_response)

            save_chat_history(user_query, ai_response)
                # Stream output

            st.session_state.chat_history.append(AIMessage(ai_response))

            

if __name__ == "__main__":
    main()
