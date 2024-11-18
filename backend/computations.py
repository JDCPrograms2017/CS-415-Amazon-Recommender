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
        for line in searchQuery:
            print(line)
            j += 1

        #ask user for what they selected
        selection = input("What would you like to select?\n")
        
        #verify selection is accurate
        count = len(searchQuery)
        if int(selection) > count or int(selection) < 1:
            print("Error in selection. Please enter another number\n")
            continue
        #get that input and put the data into a storage
        return fetch_products(searchQuery[selection - 1])

def myoutput(similarItems):
    #similarItems is the list of similar items
    for i in similarItems:
        print("Title: " + i['Title'])
        print("Salesrank: " + i['salesrank'])
        print("Reviews: " + i['reviews'])
        print()
    return

def identifyRelated(item_json):

    # Grab the ASINs of the provided product.
    similar_items = item_json["similar"]
    similar_items = similar_items.split(" ")
    limit = int(similar_items[0]) # The first element in this list will be the number of similar items.

    if limit > 5:
      limit = 5
    
    product_asins = similar_items[1:limit] # Removes the integer indicator and limits the number of related products to 5

    # return the list
    return fetch_products(product_asins)

def queryMatchingItems(query, category=None):
    tokenized_query = query.split()
    cleansed_query = [re.sub(r'[^a-zA-Z0-9]', '', tok).lower() for tok in tokenized_query] # Using a broad pattern to remove non alpha-numeric characters from the query
    print("Cleansed query: ")
    print(cleansed_query)

    tokenized_df = df.withColumn("tokenized_title", f.split(f.lower(f.col("title")), "\\s+"))
    # tokenized_df.limit(10).show()

    conditions = f.lit(True)
    for token in cleansed_query:
        conditions = conditions & f.array_contains(f.col("tokenized_title"), token)
    
    filtered_tokenized_df = tokenized_df.filter(conditions)

    filtered_tokenized_df = filtered_tokenized_df.withColumn("tokenized_title", f.split(f.lower(f.col("title")), "\\s+"))
    # filtered_tokenized_df.limit(10).show()
    
    # Count the number of tokens in the title that match the query tokens
    matching_tokens_column = f.array(*[f.when(f.array_contains(f.col("tokenized_title"), token), token).otherwise(None) for token in cleansed_query])
    
    # Add a column for the count of matching tokens
    filtered_tokenized_df = filtered_tokenized_df.withColumn("matching_tokens", matching_tokens_column)
    filtered_tokenized_df = filtered_tokenized_df.withColumn("token_match_count", f.size(f.col("matching_tokens")))

    # filtered_tokenized_df.limit(10).show()
    
    # Applying a new column with the matching tokens
    min_tokens = (lambda x, y: x if x < y else y)(3, len(cleansed_query)) # Identifying the minimum number of tokens needed to match with a product.
    filtered_tokenized_df = filtered_tokenized_df.filter(f.size(f.col("matching_tokens")) > min_tokens) # Limiting the minimum required number of tokens to be identified to match.
    print("\nFiltering by the tokens!\n")

    filtered_tokenized_df = filtered_tokenized_df.orderBy(f.col("token_match_count").desc()) # Sort by descending order (So we can start with the highest number of matching tokens)

    filtered_tokenized_df = filtered_tokenized_df.limit(10) # Reducing to the top 10 results
    
    # We are going to take the matching products and return their JSON representations to be displayed to the webpage.
    resulting_ASINs = [row['ASIN'] for row in filtered_tokenized_df.select('ASIN').collect()] # Creating a list of ASINs for the matching products.
    return fetch_products(resulting_ASINs)

# Helper function to fetch the full product(s) and their information and return the info as JSON data.
def fetch_products(product_identifiers):
    condition = f.col('ASIN').isin(product_identifiers) # Creating the condition for identifying the rows.
    resulting_rows = df.filter(condition)

    resulting_rows = resulting_rows.collect() # Collecting the DataFrame rows in to a list of Row objects.

    # Converting the results to json data
    json_results = [row.asDict() for row in resulting_rows] # When we make rows into dictionaries, we can easily convert those dictionaries into JSON data.
    json_final_dump = json.dumps(json_results, indent=4)

    return json_final_dump # Return the resulting json data
