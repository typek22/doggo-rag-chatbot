# Doggo RAG Chatbot 🐶
A simple streamlit chatbot to showcase functioning of Retrieval Augmented Generation (RAG) and how to integrate it with
a public LLM to create custom chatbot with a specific knowledge.

I write about this code in my LinkedIn article https://www.linkedin.com/pulse/creating-custom-chatbot-based-rag-llm-ivan-magdolen-splfe

- 1st article
  - branch "part_1"
- 2nd article
  - branch "part_2"

## Features

- You can chat with custom chatbot who knows data about Zaira (my dog)

## Requirements

- Python 3.8 or higher
- see requirements.txt

## Usage

### Clone and run virtual environment
```bash
$ git clone https://github.com/doggo-rag-chatbot.git
$ cd doggo-rag-chatbot
$ python -m venv .
$ ./Scripts/activate
$ pip install -r requirements.txt
```

### Set you API key in environment variables
```python
OPEN_AI_KEY='mykey'
```

### Create embeddings database
```shell
$ python embeddings_init.py
```

### Run the chatbot
```shell
$ streamlit run streamlit-app.py
```
### And go to 
```shell
http://localhost:8501
```

