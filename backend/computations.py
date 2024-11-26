import re
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, SQLContext, functions as f
from pyspark.sql.functions import *
from functools import reduce
import json

spark = SparkSession.builder.appName("AmazonRecommender") \
                    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0") \
                    .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017") \
                    .config("spark.mongodb.read.database", "AmazonDB") \
                    .config("spark.mongodb.read.collection", "Products") \
                    .getOrCreate()
df = spark.read.format("mongodb").load()
# df.show()

def myinput(searchQuery):
    while (1):
        #output the data
        j = 1
        for doc in searchQuery:
            print(j, ". ", doc["title"]) # Get the title of the found item and print it!
            j += 1

        #ask user for what they selected
        selection = input("What would you like to select?\n")
        
        #verify selection is accurate
        count = len(searchQuery)
        if int(selection) > count or int(selection) < 1:
            print("Error in selection. Please enter another number\n")
            continue
        
        return int(selection) # Returns the user's selection from the JSON collection.

def myoutput(similarItems):
    #similarItems is the list of similar items
    for i in similarItems:
        print("Title: ", i['title'])
        print("Salesrank: ", i['salesrank'])
        print("Reviews: ", i['reviews'])
        print()
    return

def identifyRelated(item_json):

    # Grab the ASINs of the provided product.
    similar_items = item_json["similar"]
    print(similar_items)
    similar_items = similar_items.split()
    limit = int(similar_items[0]) # The first element in this list will be the number of similar items.

    if limit > 5:
      limit = 5
    
    product_asins = similar_items[1:limit+1] # Removes the integer indicator and limits the number of related products to 5

    # Returns a JSON object (dictionary) of the resulting matching items.
    return fetch_products(product_asins)

def queryMatchingItems(query, category=None):
    tokenized_query = query.split()
    cleansed_query = [re.sub(r'[^a-zA-Z0-9]', '', tok).lower() for tok in tokenized_query] # Using a broad pattern to remove non alpha-numeric characters from the query
    print("Cleansed query: ")
    print(cleansed_query)

    tokenized_df = df.withColumn("tokenized_title", f.split(f.lower(f.col("title")), "\\s+")) # Tokenizing the title of each product by whitespace and putting the result in a new column.
    tokenized_df = tokenized_df.withColumn("tokenized_title", f.expr("transform(tokenized_title, x -> regexp_replace(x, '[^a-zA-Z0-9]', ''))"))
    # tokenized_df.select("tokenized_title").show(5, truncate=False)
    # tokenized_df.limit(10).show()
    
    # Count the number of tokens in the title that match the query tokens
    matching_tokens_column = f.array(*[f.when(f.array_contains(f.col("tokenized_title"), token), token) for token in cleansed_query])
    tokenized_df = tokenized_df.withColumn("matching_tokens", matching_tokens_column)

    # Filter out the NULL values in the lists.
    tokenized_df = tokenized_df.withColumn("matching_tokens", f.expr("filter(matching_tokens, x -> x IS NOT NULL)"))
    
    # Add a column for the count of matching tokens
    tokenized_df = tokenized_df.withColumn("token_match_count", f.size(f.col("matching_tokens")))

    # tokenized_df.limit(10).show()
    
    # Applying a new column with the matching tokens
    min_tokens = (lambda x, y: x if x < y else y)(2, len(cleansed_query)) # Identifying the minimum number of tokens needed to match with a product.
    filtered_tokenized_df = tokenized_df.filter(f.col("token_match_count") >= min_tokens) # Limiting the minimum required number of tokens to be identified to match.
    print("\nFiltering by the tokens!\n")

    filtered_tokenized_df = filtered_tokenized_df.orderBy(f.col("token_match_count").desc()) # Sort by descending order (So we can start with the highest number of matching tokens)
    
    # We want to make sure that if a product group is specified, we filter based on the group too!
    if (category):
        filtered_tokenized_df = filtered_tokenized_df.filter(f.col("group") == category)

    filtered_tokenized_df = filtered_tokenized_df.limit(10) # Reducing to the top 10 results

    filter_collect = filtered_tokenized_df.select(f.col("ASIN")).collect()
    
    # We are going to take the matching products and return their JSON representations to be displayed to the webpage.
    resulting_ASINs = [row['ASIN'] for row in filter_collect] # Creating a list of ASINs for the matching products.
    return fetch_products(resulting_ASINs)

# Helper function to fetch the full product(s) and their information and return the info as JSON data.
def fetch_products(product_identifiers):
    condition = f.col('ASIN').isin(product_identifiers) # Creating the condition for identifying the rows.
    resulting_rows = df.filter(condition)

    resulting_rows = resulting_rows.collect() # Collecting the DataFrame rows in to a list of Row objects.

    # Converting the results to json data
    json_results = [row.asDict() for row in resulting_rows] # When we make rows into dictionaries, we can easily convert those dictionaries into JSON data.

    return json_results # Return the resulting json data
