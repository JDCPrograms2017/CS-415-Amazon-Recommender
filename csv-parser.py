import pandas as pd

amazon_products_df = pd.read_csv('./datasets/amazon_products.csv')
amazon_categories_df = pd.read_csv('./datasets/amazon_categories.csv')

# Converting every piece of data in the .csv files to JSON format.
# TODO: Filter out categories we don't want to use.
amazon_products_df.to_json('amazon_products.json', orient = 'records', indent = 2)
amazon_categories_df.to_json('amazon_categories.json', orient = 'records', indent = 2)