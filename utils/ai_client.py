from openai import OpenAI
import logging
from dotenv import load_dotenv
import os


class AIClient:
    def __init__(self, type):
        load_dotenv()
        if type == "OPEN_AI":
            api_key = os.getenv('OPEN_AI_KEY')
            self.model = "gpt-4o"
            self._client = OpenAI(api_key=api_key)
        elif type == "DEEP_SEEK":
            api_key = os.getenv('DEEP_SEEK_KEY')
            self.model = "deepseek-chat"
            self._client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        else:
            self._client = None  # Placeholder for other AI models

        #Deepseek has no embedding model yet
        api_key = os.getenv('OPEN_AI_KEY')
        self._emb_client = OpenAI(api_key=api_key)  # Placeholder for other AI models
        self.embedding_model = "text-embedding-3-large"

    def embeddings_create(self, input, *args, **kwargs):
        if self._client:  # Call OpenAI's chat method if available
            return self._emb_client.embeddings.create(model=self.embedding_model, input=input, *args, **kwargs)
        raise NotImplementedError("Chat function is not available for this AI type")


    def get_full_message(self, aug_data, prompt):
        developer_msg = [
            {"role": "system",
             "content":
                "You don't reveal that you have my data. "
                "Don't say anything like 'based on information provided.'"
             },
        ]
        user_msg = [
            {"role": "user",
             "content": f"Using this data: '{aug_data}'. Respond to this prompt: '{prompt}'"}
        ]
        return developer_msg + user_msg


    def get_response(self, aug_data, prompt):
        if self._client:
            full_message =  self.get_full_message(aug_data, prompt)
            messages = full_message

            logging.info(f"ALL SENT MESSAGES: ```{messages}```")

            output = self._client.chat.completions.create(
                model= self.model,
                messages=messages,
                stream = True
            )
            return output