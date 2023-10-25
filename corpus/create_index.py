import os
from elasticsearch import Elasticsearch

attempt=1

# Create an Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme':'http'}])

# Define the index name
index_name = f'sinhala_index_{attempt}'

# Define the Sinhala analyzer settings
sinhala_analyzer = {
    "settings": {
    "analysis": {
      "analyzer": {
        "sinhalaAnalyzer": {
          "type": "custom",
          "tokenizer": "icu_tokenizer",
          "char_filter": ["punctuation_char_filter"]
        },
        "sinhalaSearchAnalyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": ["punctuation_char_remove_filter"]
        }
      },
      "char_filter": {
        "punctuation_char_filter": {
          "type": "mapping",
          "mappings": [".=>", "|=>", "-=>", "_=>", "'=>", "/=>", ",=>"]
        },
        "punctuation_char_remove_filter": {
          "type": "mapping",
          "mappings": [
            ".=>\\u0020",
            "|=>\\u0020",
            "-=>\\u0020",
            "_=>\\u0020",
            "'=>\\u0020",
            "/=>\\u0020",
            ",=>\\u0020"
          ]
        }
      },
      "filter": {
        "edge_n_gram_filter": {
          "type": "edge_ngram",
          "min_gram": "2",
          "max_gram": "20",
          "side": "front"
        }
      }
    }
  },
}

# Create the index with Sinhala analyzer settings
es.indices.create(index=index_name, body=sinhala_analyzer)

# Define the Sinhala content mapping
content_mapping = {
    "properties": {
        "content": {
            "type": "text",
            "analyzer": "sinhalaAnalyzer"
        }
    }
}

# Put the Sinhala content mapping in the index
es.indices.put_mapping(index=index_name, body=content_mapping)

# Directory containing the .txt files
txt_files_directory = 'D:\\Edu\\MetaphorMiner\\corpus'

# Iterate through each .txt file and index its content
for filename in os.listdir(txt_files_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(txt_files_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            document = {"content": content}
            es.index(index=index_name, body=document)
            print(f"{filename} indexed successfully")

print("Indexing completed.")
