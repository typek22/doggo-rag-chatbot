import streamlit as st
import logging
from utils.rag_handler import RAGHandler
from utils.ai_client import AIClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Line %(lineno)d - %(filename)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

openai_client = AIClient("OPEN_AI")
rag_handler = RAGHandler(openai_client, collection_name="docs")

#Start streamlit
st.title("Ask anything about my dog 🐶")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    logging.info(f"Recieved user input: {prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    rag_data = rag_handler.get_embedding(prompt=prompt)

    with st.chat_message("assistant"):
        stream = openai_client.get_response(aug_data=rag_data,
                                            prompt=prompt)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    logging.info(f"Response was delivered.")
