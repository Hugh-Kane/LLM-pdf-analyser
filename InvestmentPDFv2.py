


import os 

from apikey import apikey
from langchain.llms import OpenAI
import streamlit as st

from langchain.document_loaders import PyPDFLoader
#import Chroma 
#document is tokenised & loaded into Chroma so that we can GPT prompts
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Import vector store stuff 
from langchain.agents.agent_toolkits import(
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

#os.environ['OPENAI_API_KEY'] = apikey

llm = OpenAI(temperature=0.9,verbose=True)
embeddings = OpenAIEmbeddings()

#Create and load PDF Loader
loader = PyPDFLoader('TSLA-Q1-2023-Update.pdf')
#Split pages from pdf 
pages = loader.load_and_split()
#Load documents into vector database aka ChromaDB
store = Chroma.from_documents(pages,embeddings,collection_name = 'TSLA-Q1-2023-Update.pdf')

vectorstore_info = VectorStoreInfo(
    name = "TSLA-Q1-2023-Update",
    description = "Tesla Q1 2023 report",
    vectorstore = store
)

toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

#vector store agent 
agent_executor = create_vectorstore_agent(
    llm = llm,
    toolkit=toolkit,
    verbose=True
)
prompt = st.text_input('Input')

if prompt:
    #response = llm(prompt=prompt)

    response = agent_executor.run(prompt)

    st.write(response)

    # With a streamlit expander  
    with st.expander('Document Similarity Search'):
        # Find the relevant pages
        search = store.similarity_search_with_score(prompt) 
        # Write out the first 
        st.write(search[0][0].page_content) 


#conda activate LangChainPDF
#cd /Users/hugh/Desktop/Python/LangChain/InvestmentPDF
#streamlit run InvestmentPDFv2.py

# what was the model s/x production number for Q1-2023
