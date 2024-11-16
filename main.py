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
        
        item = com.queryMatchingItems(user_query, user_category)
        #for product in item:
        #    print(product)
        #similar = com.identifyRelated(item)
        #myoutput(similar)
    
    return


if __name__ == "__main__":
    main()