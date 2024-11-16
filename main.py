#import computations as com

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
        
        #item = myinput()
        #similar = com.identifyRelated(item)
        #myoutput(similar)
    
    return


if __name__ == "__main__":
    main()
