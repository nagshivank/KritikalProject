from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    
    dir_path = r'Projects/'
    python_files = parse_repository(dir_path)
    
    functions_dict = extract_functions_and_imports(python_files)
    
    recommendations = recommend_function(query, functions_dict)
    
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
