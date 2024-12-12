from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
# from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.chains import RetrievalQA
from groq import Groq
from langchain_groq import ChatGroq
import os
import shutil
import sys
from PyPDF2 import PdfReader
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from groq import Groq
from langchain_groq import ChatGroq
from llama_parse import LlamaParse
#
import joblib
import os
import nest_asyncio  # noqa: E402
nest_asyncio.apply()


#28-10-2024

#28-10-2024
import bs4
from langchain_core.messages import HumanMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from uuid import uuid4
import time
from typing import List
from langchain.schema import Document


from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import atexit

from langchain.retrievers.multi_query import MultiQueryRetriever

load_dotenv()

import warnings
warnings.filterwarnings("ignore")

from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from urllib.parse import quote_plus
from source.log import logging



GROQ_API_KEY=os.getenv("GROQ_API_KEY")
LLAMA_CLOUD_API_KEY=os.getenv("LLAMA_CLOUD_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
PROJECT_HOME_PATH=os.getenv('PROJECT_HOME_PATH')


# Initialize Embeddings
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")




#initialize llm model instance 
# llm = ChatGoogleGenerativeAI(
#                     model="gemini-1.5-pro",
#                     google_api_key=GEMINI_API_KEY,
#                     temperature=0,
#                     verbose=True
#                     )

user = "shubham"
password = "shubham@2144"
encoded_password = quote_plus(password)

# chat_with_history = MongoDBChatMessageHistory(
#     session_id=user,
#     connection_string=f"mongodb+srv://shubham_m:{encoded_password}@cluster0.vek6b.mongodb.net/",
#     database_name="docease",
#     collection_name="chat_history"
# )

llm = ChatGroq(
                model_name="mixtral-8x7b-32768",
                api_key=GROQ_API_KEY,
                temperature=0,
                )
# Defining Gemini LLM
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY, temperature=0, verbose=True)


#create instance of llamaparse
parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    verbose=True
)



app = Flask(__name__)
CORS(app)


def parsed_pdf_data(pdf_name):
    """
    * method: parsed_pdf_data
    * description: Parses the provided PDF document, extracts various content types, and saves the parsed data in a pickle file.
    * return: None
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       04-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   pdf_name (str): The name of the PDF file to be parsed and processed.
    *
    * Notes:
    *   - The method uses LlamaParse API to extract and structure the document's content.
    *   - The parsed data is saved as a pickle file for future access.
    """


    pdf_file_name_with_path=os.path.join(PROJECT_HOME_PATH,'Data','Pdf_Store',pdf_name)

    parsed_pdf_file_path=os.path.join(PROJECT_HOME_PATH,'Data','Parsed_pdf','parsed_data.pkl')

    parsed_pdf_path=os.path.join(PROJECT_HOME_PATH,'Data','Parsed_pdf')

    if os.path.exists(parsed_pdf_path):
        print(f"deleting existing parsed pdf path :{parsed_pdf_path}")
        shutil.rmtree(parsed_pdf_path)
        

    os.makedirs(parsed_pdf_path,exist_ok=True)
  
    # Perform the parsing step and store the result in llama_parse_documents
    parsingInstructionGeneralized = """
    The provided document may contain various types of content, including text, tables, diagrams, mathematical equations, and HTML/Markdown.

    Follow these instructions carefully to ensure all data is captured accurately:

    1.Text Extraction:
    - Extract all plain text content such as paragraphs, lists, and descriptions.
    - Preserve text formatting like bold, italics, and underlines.
    - Maintain the logical flow of sentences and paragraphs without skipping essential information.

    2.Table Handling:
    - Identify tabular data and extract it in a structured format (CSV or JSON).
    - Ensure correct alignment of rows and columns.
    - Capture table headers and associate them with corresponding data.
    - For complex tables (with multi-level headers or merged cells), ensure proper mapping of the data and explain the table structure.

    3.Diagrams and Images:
    - Extract diagrams, charts, and images and store them separately (e.g., PNG, JPEG).
    - Extract any captions or annotations along with the diagrams.
    - Attempt to capture any embedded text or labels in the diagram.

    4.Mathematical Equations:
    - Identify and extract any mathematical formulas or symbols.
    - Ensure the extraction of superscripts, subscripts, and special characters.
    - Convert the equations to LaTeX or MathML format, if possible.

    5.HTML/Markdown Content:
    - For sections containing HTML, extract the HTML elements (tags, links, images) while preserving the structure.
    - For Markdown sections, retain headings, lists, code blocks, and links in markdown format.
    - Ensure any code snippets remain in their original format.

    6.Document Structure:
    - Preserve the document's hierarchical structure, including headings, subheadings, and sections, to maintain the readability of the parsed content.

    Try to provide an accurate representation of the document, and if questions arise, be as precise as possible when answering based on the parsed content.
    """

    parser = LlamaParse(api_key=LLAMA_CLOUD_API_KEY,
                        result_type="markdown",
                        language='en',
                        parsing_instruction=parsingInstructionGeneralized,
                        max_timeout=5000,)
    
    llama_parse_documents = parser.load_data(pdf_file_name_with_path)

    # Save the parsed data to a file
    joblib.dump(llama_parse_documents, parsed_pdf_file_path)

    # Set the parsed data to the variable
    # parsed_data = llama_parse_documents
    print("Saving the parse results in .pkl format ..........")
    # return parsed_data

def load_parsed_data():
    """
    * method: load_parsed_data
    * description: Loads parsed PDF data from a pickle file if the file exists; returns the parsed data.
    * return: parsed_data (the loaded parsed data from the file)
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       04-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   None
    """


    parsed_pdf_file_path=os.path.join(PROJECT_HOME_PATH,'Data','Parsed_pdf','parsed_data.pkl')
    
    if os.path.exists(parsed_pdf_file_path):
        # Load the parsed data from the file
        parsed_data = joblib.load(parsed_pdf_file_path)

    else:
        print("Error path does not exist !")

    return parsed_data


# parsed_pdf_data('shubham_murtadak_data_scientist_resume.pdf')

# parsed_data=load_parsed_data()
# print(parsed_data)



# Create vector database
def create_vector_database(pdf_name):
    """
    * method: create_vector_database
    * description: Creates a vector database using document loaders and embeddings.
    *               This function loads documents, splits them into chunks, transforms them into
    *               embeddings using FastEmbedEmbeddings, and persists the embeddings into a
    *               Chroma vector database.
    * return: Tuple (Chroma vector database, Embedding model)
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * Shubham M       04-OCT-2024    1.0      initial creation
    *
    * Parameters
    *   pdf_name
    """

    parsed_pdf_data(pdf_name)
    # Call the function to either load or parse the data
    llama_parse_documents = load_parsed_data()
    # print(llama_parse_documents[0].text[:300])

    markdown_file_name_with_path=os.path.join(PROJECT_HOME_PATH,'Data','Markdown_store','output.md')
    
    markdown_file_folder=os.path.join(PROJECT_HOME_PATH,'Data','Markdown_store')
   
    

    if os.path.exists(markdown_file_folder):
        print(f"deleting existing markdown folder :{markdown_file_folder}")
        # Remove the folder and its contents
        shutil.rmtree(markdown_file_folder)
    
    os.makedirs(markdown_file_folder,exist_ok=True)

    with open(markdown_file_name_with_path, 'a',encoding="utf8",errors="surrogateescape") as f:  # Open the file in append mode ('a')
        for doc in llama_parse_documents:
            f.write(doc.text + '\n')


    try:
        loader = UnstructuredMarkdownLoader(markdown_file_name_with_path)

        documents = loader.load()
    except Exception as e:
        print(f"error:{e}")

    print("documents:",documents)
    # Split loaded documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    #len(docs)
    print(f"length of documents loaded: {len(documents)}")
    print(f"total number of document chunks generated :{len(docs)}")
    #docs[0]


    vdb_path=os.path.join(PROJECT_HOME_PATH,'Database','chroma_db')
    # D:\personal\Personal Projects\DocEase~Chat with Pdf\backend\Database\chroma_db

    # Check if the folder exists
    if os.path.exists(vdb_path):
        # Remove the folder and its contents
        shutil.rmtree(vdb_path)

    print(vdb_path)
    # Create and persist a Chroma vector database from the chunked documents
    vs = Chroma.from_documents(
        documents=docs,
        embedding=embed_model,
        persist_directory=vdb_path,  # Local mode with in-memory storage only
        collection_name="rag"
    )

    print('Vector DB created successfully !')
    return vs,embed_model


@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        uploaded_file = request.files['file']
        print(uploaded_file)
        if uploaded_file.filename != '':
            target_directory =os.path.join(PROJECT_HOME_PATH,'Data','Pdf_Store')
            # target_directory = ".\docs"
            os.makedirs(target_directory, exist_ok=True)
            unique_filename = str(uuid.uuid4()) + ".pdf"
            file_path = os.path.join(target_directory, unique_filename)
            print(file_path)
            uploaded_file.save(file_path)
            print(f"pdf saved at location :{file_path} successfully !")
            parsed_pdf_data(unique_filename)
            parsed_data=load_parsed_data()
            print(parsed_data)
            vs,embed_model=create_vector_database(unique_filename)

            return jsonify({
                "message": "PDF file uploaded and saved successfully",
                "original_filename": uploaded_file.filename,
                "file_path": file_path
            })
        else:
            return jsonify({"error": "No file selected"})
    except Exception as e:
        return jsonify({"error": str(e)})



def retrive_data(question):
    """
    * method: retrive_data
    * description: Retrieves relevant documents from a Chroma vector database based on the given question.
    *               This function loads the vector store, queries it using the specified LLM, and 
    *               returns the most relevant documents along with the count of retrieved documents.
    * return: Tuple (list of retrieved documents, number of documents)
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       04-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   question: str - The question/query to be used for document retrieval.
    *   pdf_name: str - The name of the PDF file (used for context).
    """

    print("inside retriver !")
    # llm = ChatGroq(temperature=0,
    #                     model_name="mixtral-8x7b-32768",
    #                     api_key=GROQ_API_KEY,)
    
   
    
    vdb_path=os.path.join(PROJECT_HOME_PATH,'Database','chroma_db')
    #load vector-store data
    vectorstore = Chroma(embedding_function=embed_model,
                      persist_directory=vdb_path,
                      collection_name="rag")
    

    # Retrieving & querying  documents 
    retriever = MultiQueryRetriever.from_llm(
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":10}),
        llm=llm
    )
 
    docs = retriever.invoke(input=question)
    
    no_of_doc=len(docs)
    print(docs,no_of_doc)
    return docs,no_of_doc


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query')

        print(f"Query: {query}")

        docs,no_of_docs=retrive_data(query)

        print()
        print(f"number of docs retrieve are :{no_of_docs}")

   
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # llm = ChatGroq(temperature=0,
        #                 model_name="mixtral-8x7b-32768",
        #                 api_key=GROQ_API_KEY,)
        
        vdb_path=os.path.join(PROJECT_HOME_PATH,'Database','chroma_db')
        #load vector-store data
        vectorstore = Chroma(embedding_function=embed_model,
                        persist_directory=vdb_path,
                        collection_name="rag")
    
        # docs,no_of_docs=retrive_data(question)
        retriever=vectorstore.as_retriever(search_kwargs={'k': 5})
        
        # custom_prompt_template = """
        #         You are a helpful chat assistant named DocEase, specializing in tasks related to PDF data.You will get pdf content and Your task is to answer question on that pdf content .
        #         Your key expertise includes:

        #         1. Answering questions based on the content of PDFs.
        #         2. Translating PDF data between multiple languages, including English, Marathi, and Hindi (and vice versa).
        #         3. Summarizing PDF content.
        #         4. Providing answers in an engaging and clear format.
                

        #         Instructions:
        #         - If the exact answer is not available in the PDF, provide the best possible answer based on your understanding.
        #         - Keep your responses concise, informative, and user-friendly.

        #         Context: {context}  
        #         Question: {question}

        #     """

        # custom_prompt_template = """
        #     You are a helpful chat assistant named DocEase, specializing in tasks related to PDF data. You will get PDF content, and your task is to answer questions based on that content.

        #     Your key expertise includes:

        #     1. Answering questions based on the content of PDFs.
        #     2. Translating PDF data between multiple languages, including English, Marathi, and Hindi (and vice versa).
        #     3. Summarizing PDF content.
        #     4. Providing answers in an engaging and clear format.

        #     **Instructions:**
        #     - If the exact answer is not available in the PDF, provide the best possible answer based on your understanding.
        #     - Keep your responses concise, informative, and user-friendly.
        #     - Format your answers using **Markdown** for clarity and readability, including headings, bullet points, and code blocks when necessary.

        #     **Context:** 
        #     {context}  

        #     **Question:** 
        #     {question}

        #     """

        custom_prompt_template = """
                You are a helpful chat assistant named DocEase, specializing in tasks related to PDF data. You will get PDF content, and your task is to answer questions based on that content.

                Your key expertise includes:
                0. Provide your Introduction and features at start on conversation in response to question such as 'Hi','Hello'.Give suggestion to user which questions they can ask based on our below mentioned features.
                1. Answering questions based on the content of PDFs.
                2. Translating PDF data between multiple languages, including English, Marathi, and Hindi (and vice versa).
                3. Summarizing PDF content.
                4. Providing answers in an engaging and clear format.


                **Instructions:**
                - If the exact answer is not available in the PDF, provide the best possible answer based on your understanding.
                - Keep your responses concise, informative, and user-friendly.
                - Format your answers using **Markdown** for clarity and readability, including headings, bullet points, and code blocks when necessary.
                - Do Not start response with Answer keyword.

                **Context:**  
                {context}  

                **Question:**  
                {question}  

                **Answer:**  
                Please format your answer using Markdown as follows:
                - **Headings** for important sections.
                - **Bullet points** for lists or steps.
                - **Code blocks** or **bold** for important terms or keywords.
                - **Short paragraphs** for better readability.

                For example:
                - If you're explaining a concept, break it down into clear steps or bullet points.
                - Use **bold** for key terms and phrases.
                - Use headings like `### Summary`, `### Key Points`, `### Conclusion` to structure your response.

                """


    
        prompt = PromptTemplate(template=custom_prompt_template,
                                input_variables=['context', 'question'])
        
        print(prompt)  

        #define_qa_chain
        qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                chain_type="stuff",
                                retriever=retriever,
                                return_source_documents=True,
                                chain_type_kwargs={"prompt": prompt})
        

        # chat_with_history.add_user_message(query)
        answer=qa_chain.invoke({query})['result']
        # chat_with_history.add_ai_message(answer)

    
        response = {
            "result": answer,
            "conversation_result":''
        }

        print(response)
        return jsonify(response)
        
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run()
