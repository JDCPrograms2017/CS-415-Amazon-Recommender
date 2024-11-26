# This code is supposed to connect to MongoDB on localhost:27017
# and setus up a /search endpoint that takes query and category into a POST request, searches the db and 
# returns matching products

#make sure to do pip install json2html

from flask import Flask, request, jsonify, render_template, session, url_for
from pymongo import MongoClient
import json
from json2html import *
import computations as com

app=Flask(__name__)
app.secret_key = '12verys3cret'
client=MongoClient('mongodb://localhost:27017')
db=client['BigDataProject']
products_collection=db['Products']

@app.route('/')
def home():
    return render_template("search.html")

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
        
        return jsonify(items)
        
    return render_template("search.html")

@app.route('/selection', methods=['POST'])
def select():
    if request.method == 'POST':
        #output the data

        #get selected item
        # search = request.form['choice']
        itemData = request.get_json()

        similar = com.identifyRelated(itemData)
        #similar = com.identifyRelated(items[int(search) - 1])

        # Storing the similar products in the cookies to be rendered after redirect.
        session['related-products'] = similar
        redirect_url = url_for('related_products_page')
        
        # print(f'URL being sent: {redirect_url}')
        return jsonify({'redirect-url': redirect_url})
    return render_template("selection.html", products=similar)

@app.route('/display-related-products', methods=['GET'])
def related_products_page():
    if request.method == 'GET':
        related_products = session.get('related-products')
        return render_template('display.html', products=related_products)

@app.route('/display', methods=['POST'])
def output():
    return render_template("search.html")

if __name__== '__main__':
    app.run(debug=True)
