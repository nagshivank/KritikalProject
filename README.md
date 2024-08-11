# KritikalProject
This project implements a Python-based coding assistant that uses a fine-tuned BERT model to parse a repository of code and suggest relevant functions or components based on user input. The assistant is accessible via a web interface powered by Flask, allowing users to easily search through code projects. It is an effort towards producing open-source alternatives to existing commercial tools like GitHub Copilot, making intelligent code recommendations more accessible.

### Setting Up the Environment

Install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

### Fine-Tune the BERT Model

The pre-trained BERT model was fine-tuned.

```bash
python fine_tune_bert.py
```

### Start the Flask API

To provide a web interface for searching the code repository, the Flask API can be started at *http://127.0.0.1:5000* by running:

```bash
python app.py
```

### Use the Web Interface

Open your web browser and navigate to `http://127.0.0.1:5000`. Enter your search query in the input field and click "Search" to see the recommended functions along with their relevance scores.
