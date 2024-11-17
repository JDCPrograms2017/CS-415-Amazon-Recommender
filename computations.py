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
df = df.dropDuplicates(["Title"])
df.show()

def identifyRelated(line):
    #check if the current item is the item we are selecting to find similar items for
    
    #grab line of "similar"

    #get first item which is number of items
    (limit, items) = line['similar'].split(" ", 1)
    #limit is the first item

    #iterate through the rest of the string until the limit is hit
    #want to use split to split through each tab
    items = items.split(" ", limit)

    #for each item, search for the ASIN in the entire database
    #put the contents in a list
    index = 0
    similarItems = []
    if limit > 5:
      limit = 5
    while index < limit:
        for i in df:
            if i['ASIN'] == items[index]:
                similarItems.append(i)
        index += 1

    #return the list
    return similarItems

def queryMatchingItems(query, category=None):
    tokenized_query = query.split()
    cleansed_query = [re.sub(r'[^a-zA-Z0-9]', '', tok).lower() for tok in tokenized_query] # Using a broad pattern to remove non alpha-numeric characters from the query

    tokenized_df = df.withColumn("tokenized_title", f.split(lower(f.col("Title")), "\\s+")) # Making a tokenized version of the dataframe and making the tokens lowercase (to remove case sensitivity)
    
    # Exploding the tokenized titles so that we can process each token and identify matching substrings.
    columns_to_preserve = [col for col in tokenized_df.columns if col != "tokenized_title"]
    exploded_tokens = tokenized_df.select(*columns_to_preserve, f.explode(f.col("tokenized_title")).alias("token"))

    # Filter out the tokens based on the given condition
    conditions = [f.col("token").contains(f'{token}') for token in cleansed_query]
    filter_condition = reduce(lambda x, y: x | y, conditions)
    filtered_tokenized_df = exploded_tokens.filter(filter_condition)

    # Regroup the filtered dataframe    
    filtered_tokenized_df = filtered_tokenized_df.groupBy("Title", "ASIN", "categories").agg(f.collect_set("token").alias("matching_tokens"))
    
    # Applying a new column with the matching tokens
    min_tokens = (lambda x, y: x if x < y else y)(3, len(cleansed_query)) # Identifying the minimum number of tokens needed to match with a product.
    filtered_tokenized_df = filtered_tokenized_df.filter(f.size(f.col("matching_tokens")) > min_tokens) # Limiting the minimum required number of tokens to be identified to match.
    
    # Defining a function within the scope of this function to filter by categories if need be.
    def match_categories(categories):
        parsed_categories = [entry.split('[')[0] for entry in categories if entry]
        matched_cats = set(parsed_categories) & set(category)
        return list(matched_cats)

    # If we specify a category, then we should filter based on the category too.
    if category:
        cat_match_udf = f.udf(match_categories, returnType=ArrayType(StringType()))
        filtered_tokenized_df = filtered_tokenized_df.withColumn("Matching Categories", cat_match_udf(f.col("categories")))
        filtered_tokenized_df = filtered_tokenized_df.filter(f.size(f.col("Matching Categories")) > 0)
    
    filtered_tokenized_df = filtered_tokenized_df.withColumn("token_match_count", f.size(f.col("matching_tokens")))
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

'''def findSimilarItems():
    df.printSchema()
    #df.foreach(helper)
    #df.show(10)
    return

if __name__ == "__main__":
    findSimilarItems()'''
