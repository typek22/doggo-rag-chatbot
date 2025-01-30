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
            {"role": "developer",
             "content":
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer "
                    "the question. If you don't know the answer, say that you "
                    "don't know. Use three sentences maximum and keep the "
                    "answer concise."
                    "\n\n"
                    f"{aug_data}"
             }
        ]
        developer_msg = [
            {"role": "developer",
             "content":
                "Given a chat history and the latest user question "
                "which might reference context in the chat history, "
                "formulate a standalone question which can be understood "
                "without the chat history. Do NOT answer the question, "
                "just reformulate it if needed and otherwise return it as is."
             }
        ]
        user_msg = [
            {"role": "user",
             "content": prompt}
        ]
        return developer_msg + user_msg



    def get_response(self, aug_data, prompt, prev_messages):
        if self._client:
            full_message =  self.get_full_message(aug_data, prompt)
#            messages = prev_messages + full_message

            developer_msg = [
                {"role": "developer",
                 "content":
                     "Given a chat history and the latest user question "
                     "which might reference context in the chat history, "
                     "formulate a standalone question which can be understood "
                     "without the chat history. Do NOT answer the question, "
                     "just reformulate it if needed and otherwise return it as is."
                 }
            ]
            user_msg = [
                {"role": "user",
                 "content": prompt}
            ]

            messages = developer_msg + prev_messages + user_msg






            logging.info(f"ALL SENT MESSAGES: ```{messages}```")

            output = self._client.chat.completions.create(
                model= self.model,
                messages=messages,
                stream = True
            )
            return output