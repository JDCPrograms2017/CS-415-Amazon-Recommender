# This code is supposed to connect to MongoDB on localhost:27017
# and setus up a /search endpoint that takes query and category into a POST request, searches the db and 
# returns matching products

from flask import Flask, request, jsonify
from pymongo import MongoClient

app=Flask(__name__)
client=MongoClient('mongodb://localhost:27017')
db=client['BigDataProject']
products_collection=db['Products']

@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/search', methods=['POST'])
def search():
    data=request.json
    query=data.get('query','')
    category=data('group','')
    search_filter={'title': {'$regex':query, '$options': 'i'}}
    if category:
        search_filter['group']={'$regex': category, '$options':'i'}
    
    results=list(products_collection.find(search_filter,{'_id':0}))
    return jsonify(results)

if __name__== '__main__':
    app.run(debug=True)