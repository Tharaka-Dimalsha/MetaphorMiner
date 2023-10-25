from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Create an Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme':'http'}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    
    # Define your Elasticsearch query here
    # For a basic example, we'll use a simple match query
    body = {
    "query": {
        "match": {
            "content": {
                "query": query,
                "analyzer": "sinhalaAnalyzer"
            }
        }
    }
}

    print(body)
    # Search the Elasticsearch index
    results = es.search(index='sinhala_index_1', body=body)
    
    # Extract relevant information from search results
    hits = results['hits']['hits']
    
    # Return the search results to the user
    return render_template('results.html', hits=hits)

if __name__ == '__main__':
    app.run(debug=True)
