import re
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, SQLContext, functions as f
from pyspark.sql.functions import *
from functools import reduce

spark = SparkSession.builder.appName("AmazonRecommender") \
                    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0") \
                    .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017") \
                    .config("spark.mongodb.read.database", "AmazonDB") \
                    .config("spark.mongodb.read.collection", "Products") \
                    .getOrCreate()
df = spark.read.format("mongodb").load()
df.show()

def identifyRelated(line):
    #check if the current item is the item we are selecting to find similar items for
    
    #grab line of "similar"

    #get first item which is number of items
    (limit, items) = line.similar.split(" ", 1)
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
            if i.ASIN == items[index]:
                similarItems.append(i)
        index += 1

    #return the list
    return similarItems

def queryMatchingItems(query, category=None):
    tokenized_query = query.split()
    cleansed_query = [re.sub(r'[^a-zA-Z0-9]', '', tok) for tok in tokenized_query] # Using a broad pattern to remove non alpha-numeric characters from the query

    # There is now the necessity to broadcast the tokens to all Spark nodes for efficient computation:
    query_broadcast = spark.sparkContext.broadcast(cleansed_query) # Broadcasting query tokens to the Spark nodes. (Since this project is local, there's only one node but whatevah.)
    tokenized_df = df.withColumn("tokenized_title", f.split(f.col("Title"), "\\s+")) # Making a tokenized version of the dataframe
    
    # Exploding the tokenized titles so that we can process each token and identify matching substrings.
    columns_to_preserve = [col for col in tokenized_df.columns if col != "tokenized_title"]
    exploded_tokens = tokenized_df.select(*columns_to_preserve, f.explode(f.col("tokenized_title")).alias("token"))

    # Filter out the tokens based on the given condition
    conditions = [f.col("token").contains(f'{token}') for token in cleansed_query]
    filter_condition = reduce(lambda x, y: x | y, conditions)
    filtered_tokenized_df = exploded_tokens.filter(filter_condition)

    # Regroup the filtered dataframe    
    filtered_tokenized_df = filtered_tokenized_df.groupBy("Title", *[col for col in df.columns if col != "tokenized_title"]).agg(f.collect_set("token").alias("matching_tokens"))
    
    # Applying a new column with the matching tokens
    filtered_tokenized_df = filtered_tokenized_df.filter(f.size(f.col("matching_tokens")) > 2) # Setting some arbitrary value for token count. (I made it so that we need to find 2 or more related tokens to display the item)
    
    # If we specify a category, then we should filter based on the category too.
    #if category:
    #    filtered_tokenized_df = filtered_tokenized_df.filter(f.col("category") == category)
    
    filtered_tokenized_df = filtered_tokenized_df.withColumn("token_match_count", f.size(f.col("matching_tokens")))
    filtered_tokenized_df = filtered_tokenized_df.orderBy(f.col("token_match_count").desc()) # Sort by descending order (So we can start with the highest number of matching tokens)

    # TODO: Format the n number of matching items for the query and return the data in a way that's fitting for the application. (Or return nothing if a query fails to find matching items.)
    return filtered_tokenized_df

'''def findSimilarItems():
    df.printSchema()
    #df.foreach(helper)
    #df.show(10)
    return

if __name__ == "__main__":
    findSimilarItems()'''
