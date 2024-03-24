# **Pdf Chatbot**

This is a local, AI-powered question-answering chatbot that utilizes PDFs as its knowledge source. 

**Features:**

* Answer questions directly from uploaded PDFs.
* Supports various PDF lengths and topics.
* Engage in natural conversations for efficient information retrieval.
* Saves chat history in daily Markdown files for easy reference.
* Completely local processing ensures data privacy and security.

**Getting Started**

1.  **Prerequisites:**
    * Python 3.x
    * Streamlit
    * Ollama
    * Langchain libraries (langchain-core, langchain-community)
    * Additional libraries as specified in `requirements.txt` (if applicable)

2.  **Installation:**
    * Clone this repository:
       ```bash
       git clone https://github.com/YashBaravaliya/pdf-chat
       ```
    * Navigate to the project directory:
       ```bash
       cd pdf-chatbot
       ```
    * Install dependencies:
       ```bash
       pip install -r requirements.txt
       ```

    

3.  **Run the application:**
    * Start a terminal or command prompt in the project directory.
    * Run the script:
       ```bash
       streamlit run main.py
       ```
    * This will launch the Streamlit app in your web browser.

**Usage**

1.  Upload a PDF document using the file uploader in the sidebar.
2.  Ask your questions related to the uploaded PDF content in the chat interface.
3.  The chatbot will analyze the PDF and provide answers based on its understanding of the text.
4.  The conversation history is automatically saved as daily Markdown files in the `history` folder for future reference.

**Further details and enhancements can be found in the comments within the code.**

**Feel free to contribute or raise any issues through pull requests!**

