import logging
import chromadb

EMBEDDING_DISTANCE = 1.4
NO_RESULTS = 3

class RAGHandler:
    def __init__(self, openai_client, collection_name):
        self.openai_client = openai_client
        self.chroma_client= chromadb.PersistentClient(path="./chroma_db")
        self.collection_name = collection_name


    def initiate_embeddings(self, data):
        try:
            self.chroma_client.delete_collection(self.collection_name)
        except ValueError: #collection exists
            pass
        self.collection = self.chroma_client.create_collection(name=self.collection_name)

        logging.info("Creating new RAG database.")

        # store each document in a vector embedding database
        for i, d in enumerate(data):
            response = self.openai_client.embeddings_create(input=d)
            embedding = response.data[0].embedding
            self.collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[d]
            )


    def get_embedding(self, prompt):
        logging.info("Getting embedding data...")
        logging.info(f"Prompt: {prompt}")

        # generate an embedding for the prompt and retrieve the most relevant doc
        response = self.openai_client.embeddings_create(input=prompt)

        n_results = NO_RESULTS
        collection = self.chroma_client.get_collection(name=self.collection_name)
        results = collection.query(
            query_embeddings=[response.data[0].embedding],
            n_results=n_results
        )
        docs = [doc for doc, dist in zip(results['documents'][0], results['distances'][0]) if dist < EMBEDDING_DISTANCE]
        data = " ".join(docs)
        logging.info(f"Results: {results}")
        if data:
            return data
        else:
            return None