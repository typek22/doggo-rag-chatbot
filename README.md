# Doggo


## Features

- a
- b
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

