import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# sys.path.insert(0, r"D:\Python\TaxCalculator")

# ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.insert(0, ROOT)
from config.env_config import settings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma

api_key=settings.OPENAI_API_KEY
loader = PyPDFLoader("../data/Profile.pdf")
docs = loader.load()
print(f"API key value: {repr(api_key)}")  # if None, settings isn't reading .env
# print(len(docs))

#CHUNKING 

splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
splitter_data = splitter.split_documents(docs)
# print(len(splitter_data))

#EMBEDDING
embeddings = OpenAIEmbeddings(model = "text-embedding-3-large", api_key=api_key)
vector_store = Chroma.from_documents(
    documents=splitter_data, 
    embedding =embeddings
)

#QA

query = "Machine learnings and Data Scrience Content"
data = vector_store.similarity_search(query = query)

print(len(data))