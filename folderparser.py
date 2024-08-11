import os
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch
import re

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('path_to_your_fine-tuned_model')
nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

def parse_repository(dir_path):
    # List to store Python files
    res = []

    # Iterate directory
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)) and path.endswith('.py'):
            res.append(path)
    return res

def extract_functions_and_imports(file_paths):
    functions_dict = {}
    for file in file_paths:
        with open(file, 'r') as f:
            content = f.read()
        
        # Extract functions
        functions = content.split("def ")
        functions.pop(0)
        
        for func in functions:
            name = func.split("(")[0]
            functions_dict[name] = func
        
        # Extract imports (just for analysis, not used in recommendation)
        imports = re.findall(r'^import (.+)|^from (.+) import .+', content, re.MULTILINE)
        
        # Save imports and functions if needed (omitted for brevity)
    
    return functions_dict

def recommend_function(keyword, functions_dict):
    recommendations = {}
    for name, code in functions_dict.items():
        # Use BERT model to predict the relevance of each function to the keyword
        inputs = tokenizer(keyword, name, return_tensors="pt")
        outputs = model(**inputs)
        score = torch.nn.functional.softmax(outputs.logits, dim=-1)
        relevance = score[0][1].item()  # Assume label 1 is 'relevant'
        recommendations[name] = relevance
    
    # Sort and return the best matches
    sorted_recommendations = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))
    return sorted_recommendations

if __name__ == "__main__":
    dir_path = r'/path/to/your/repository'
    python_files = parse_repository(dir_path)
    
    functions_dict = extract_functions_and_imports(python_files)
    
    keyword = "Your search query"
    recommendations = recommend_function(keyword, functions_dict)
    
    for func, score in recommendations.items():
        print(f"Function: {func}, Relevance Score: {score}")