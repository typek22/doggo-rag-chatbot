from utils.rag_handler import RAGHandler
from utils.ai_client import AIClient
from data.documents import documents

openai_client = AIClient("OPEN_AI")

rag_handler = RAGHandler(openai_client, collection_name="docs")
rag_handler.initiate_embeddings(data=documents)
