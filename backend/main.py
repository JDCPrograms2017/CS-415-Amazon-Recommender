import computations as com

def menu():
    print("\nSelect an item\n")
    print("1) Search for products\n")
    selection = input("2) Quit\n")
    return selection

def main():
    while (1):
        selection = menu()
        if int(selection) > 2 or int(selection) < 1:
            print("Error in input for selecting a to do item\n")
            break
        elif int(selection) == 2:
            print("Quitting\n")
            break

        user_query = input("What item are you looking for?\n")
        user_category = input("\nWhat category does it belong to?\n")
        
        item = com.queryMatchingItems(user_query, user_category) # Fetches a JSON object that contains the resulting products from the query.
        # print(item)
        user_choice = com.myinput(item) # Myinput will allow the user to select a product from this list of products and then the selection will be returned as an integer index.

        similar = com.identifyRelated(item[int(user_choice) - 1]) # Fetches the JSON object (dictionary) of the product we select and sends it to identifyRelated to get the matching items.)
        com.myoutput(similar)
    
    return


if __name__ == "__main__":
    main()
