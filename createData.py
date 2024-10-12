import json

filename = "amazon-meta.txt"
out = open("amazon.json", "w")

list1 = []
fields = ['ASIN', 'title', 'group', 'salesrank', 'similar']
l = 0
dict2 = {}
with open(filename) as fp:
    for line in fp:
        description = list(line.strip().split(":", 1))
        if description[0] == "":
            list1.append(dict2)
            #json.dump(dict2, out, indent = 4, sort_keys = False)
            #dict1[l] = dict2
            dict2 = {}
        elif description[0] == 'Id':
            dict2["Id"] = description[1].strip()
            #l = description[1].strip()
            continue
        elif description[0] == 'categories':
            num = int(description[1])
            x = 0
            cate = []
            cate.append(description[1].strip())
            while x < num:
                cate.append(fp.readline().strip())
                x += 1
            dict2['categories'] = cate
        elif description[0] == 'reviews':
            items = list(description[1].split(None, 3))
            num = int(items[1])
            x = 0
            rev = []
            rev.append(description[1].strip())
            while x < num:
                rev.append(fp.readline().strip())
                x += 1
            dict2['reviews'] = rev
        i = 0
        while i < len(fields):
            if description[0] == fields[i]:
                dict2[fields[i]] = description[1].strip()
            i = i + 1

json.dump(list1, out, indent = 4, sort_keys = False)
out.close()

# Full information about Amazon Share the Love products
#Total items: 548552
