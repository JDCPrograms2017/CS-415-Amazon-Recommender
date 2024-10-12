import json

filename = "./amazon-meta.txt"
out = open("amazon.json", "w", encoding="utf-8")

products = {} # Establish a dictionary that will hold each product Document. This dictionary is the Collection of those Documents.
fields = ['ASIN', 'title', 'group', 'salesrank', 'similar']
dict2 = {}
current_ID = None # Establish a temporary variable to save the current ID of each product to make as the Document ID.
document_count = 0
document_limit = 200000
with open(filename, encoding="utf-8") as fp:
    for line in fp:
        description = list(line.strip().split(":", 1))
        if description[0] == "":
            if current_ID: # If the current ID is identified for the product.
                products[f"{current_ID}"] = dict2
            dict2 = {}
            current_ID = None
            document_count += 1

            if document_count == document_limit:
                break # This helps us limit the output data to 200,000 entries. We really don't need 1 million products here, haha.
        
        elif description[0] == 'Id':
            current_ID = description[1].strip() # It's necessary to set current_ID first so that we can know when to proceed to the next Document.
        elif description[0] == 'title':
            dict2["title"] = description[1].strip()
        elif description[0] == 'categories':
            num = int(description[1])
            cate = [description[1].strip()]
            for _ in range(num):
                cate.append(fp.readline().strip())
            dict2['categories'] = cate
        elif description[0] == 'reviews':
            items = list(description[1].split(None, 3))
            num = int(items[1])
            rev = [description[1].strip()]
            for _ in range(num):
                rev.append(fp.readline().strip())
            dict2['reviews'] = rev
        
        for field in fields:
            if description[0] == field:
                dict2[field] = description[1].strip()

# Wrapping our dictonary of products with their ID in a Collection titled "products"
final_dict = {"products": products}
json.dump(final_dict, out, indent = 4, sort_keys = False)
out.close()

# Full information about Amazon Share the Love products
#Total items: 548552
