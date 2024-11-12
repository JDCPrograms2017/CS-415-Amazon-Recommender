import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, SQLContext, functions as f
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("AmazonRecommender") \
                    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0") \
                    .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017") \
                    .config("spark.mongodb.read.database", "AmazonDB") \
                    .config("spark.mongodb.read.collection", "Products") \
                    .getOrCreate()
df = spark.read.format("mongodb").load()
df.show()

def helper(line):
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
    while index < limit:
        for i in df:
            if i.ASIN == items[index]:
                similarItems.append(i)
        index += 1

    #return the list
    return similarItems

def findSimilarItems():
    df.printSchema()
    #df.foreach(helper)
    #df.show(10)
    return

if __name__ == "__main__":
    findSimilarItems()
