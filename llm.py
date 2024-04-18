# Working with Local LLM 
from langchain.vectorstores.redis import Redis
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv

load_dotenv()
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Function to load data from csv file

def load_data(path):
    loader = CSVLoader(path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    texts = text_splitter.split_documents(data)
    return texts
# Vectorizing data


def vectorize_data(texts,index="test_index"):
    print ("Vectorizing data")
    try:
        document_store = Redis.from_existing_index(
            index_name=index,
            redis_url=os.getenv("REDIS_URL"),
            embedding=embeddings,
            schema="redis_schema.yaml"
            
        )
        print("Loaded from the already existing index")
    except:   
        document_store = Redis.from_documents(
            texts,
            embeddings,
            redis_url=os.getenv("REDIS_URL"),
            index_name=index,
        )
        document_store.write_schema("redis_schema.yaml")
        print("Created a new index.")
        
    return document_store

texts = load_data("netflix_titles.csv")

document_store = vectorize_data(texts)


def get_related_documents(question):
    print("Getting related documents")
    related_doc = document_store.similarity_search(question, k=3)
    content = [doc.page_content for doc in related_doc]
    knowledge = "\n".join(content)
    return knowledge



def get_answer(question):
    print("Getting answer")
    knowledge = get_related_documents(question)
    question = knowledge + "\n" + question + "Make sure to just answer the question asked no aditional detail required"
    llm = Ollama(model="codegemma")
    answer = llm.invoke(question)
    return answer

print(get_answer("When was Blood & Water launched?"))