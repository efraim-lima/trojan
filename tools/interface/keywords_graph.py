import os
import sys

# Obtenha o caminho absoluto da pasta 'functions' dois níveis acima do diretório deste arquivo
functions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Adicione o diretório ao caminho de busca do Python
sys.path.insert(0, functions_dir)

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pymongo import MongoClient
from functions.keyboards import analyze_typing

def count_keywords():
    client = MongoClient()
    db = client.mydatabase
    collection = db.wordcloud

    keywords_count = {}

    if collection.count_documents({}) > 0:
        documents = collection.find({}, {"_id": 0, "keyword": 1})

        for document in documents:
            keyword = document["keyword"]
            keywords_count[keyword] = keywords_count.get(keyword, 0) + 1

    return keywords_count

if __name__ == "__main__":
    while True:
        # Consultar as palavras geradas
        keywords = analyze_typing()

        # Contar as palavras
        word_counts = count_keywords()

        # Atualizar o wordcloud
        wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_counts)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()

        # Salvar o wordcloud em um arquivo
        wordcloud.to_file("wordcloud.png")
