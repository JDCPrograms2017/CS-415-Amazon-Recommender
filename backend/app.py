# This code is supposed to connect to MongoDB on localhost:27017
# and setus up a /search endpoint that takes query and category into a POST request, searches the db and 
# returns matching products

#make sure to do pip install json2html

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import json
from json2html import *
import computations as com

app=Flask(__name__)
client=MongoClient('mongodb://localhost:27017')
db=client['BigDataProject']
products_collection=db['Products']

@app.route('/')
def home():
    return render_template("search.html")


# @app.route('/search', methods=['POST'])
# def search():
#     data=request.json
#     query=data.get('query','')
#     category=data('group','')
#     search_filter={'title': {'$regex':query, '$options': 'i'}}
#     if category:
#         search_filter['group']={'$regex': category, '$options':'i'}
    
#     results=list(products_collection.find(search_filter,{'_id':0}))
#     return jsonify(results)
items = []
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # search = request.form['search']
        # user_category = request.form['category']
        clientReq = request.get_json()
        search = clientReq.get('query')
        user_category = clientReq.get('category')

        # item = [{'title' : 'something'}, {'title': 'num2'}] #sample data
        global items # Referencing the global item variable to persist the query result across API calls.
        items = com.queryMatchingItems(search, user_category) # Fetches a JSON object that contains the resulting products from the query.
        
        #used this link https://pypi.org/project/json2html/
        j = 1
        for i in items:
            i['number'] = j
            rev = i['reviews'][0].split(":")
            new = rev[3]
            i['avg'] = new
            j += 1
        j -= 1
        # html = json2html.convert(json = item)
        # return render_template("selection.html", products=items, max=j)
        print(jsonify(items))
        return jsonify(items)
        
    return render_template("search.html")

@app.route('/selection', methods=['POST'])
def select():
    if request.method == 'POST':
        #output the data

        #get selected item
        search = request.form['choice']
        # print(item)
        # print("User choice: ", search)
        # search should be an integer (in a string type)

        similar = com.identifyRelated(items[int(search) - 1])
        # similar = [{'title' : 'something'}] #sample data

        # html = json2html.convert(json = similar)
        for i in items:
            rev = i['reviews'][0].split(":")
            new = rev[3]
            i['avg'] = new
        return render_template("display.html", products=similar)
    return render_template("selection.html", products=similar)

@app.route('/display', methods=['POST'])
def output():
    return render_template("search.html")

if __name__== '__main__':
    app.run(debug=True)
