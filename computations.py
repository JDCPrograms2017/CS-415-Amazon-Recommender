from pyspark.sql import SparkSession

dbname = "amazon.json"
spark = SparkSession.builder.appName("Amazon").getOrCreate()
df = spark.read.json(dbname)
#df.show()

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
