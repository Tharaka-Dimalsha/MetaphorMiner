from elasticsearch import Elasticsearch
import os

attempt=1

# Define the Elasticsearch server connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme':"http"}])  # Update with your Elasticsearch server details

# Specify the directory containing the text files
directory = "C:\\Users\\thara\\OneDrive\\Desktop\\Search-Engine\\corpus"

# Function to read and index text files
def index_text_files():
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r',encoding='utf-8') as file:
                content = file.read()
                # Define the document structure
                document = {
                    'file_name': filename,
                    'text_content': content
                }
                # Index the document into Elasticsearch
                es.index(index=f'index_{attempt}', body=document)
                print(f"Indexed: {filename}")

# Call the function to index the text files
index_text_files()
