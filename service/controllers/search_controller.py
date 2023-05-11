from service import app
from flask import request, jsonify
from service.models import bm25_search

@app.route("/bm25", methods=["POST"])
def bm25():
    data = request.get_json()
    query = data['query']
    k = data['k']
    return jsonify(bm25_search.search(query=query, k=k))