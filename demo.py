import json
import json_lines

lists =  []
count=3

filename = '/home/nirisha/amitness/amitness/blogs.jl'

list_of_dict = []

with open(filename, 'rb') as f:
    for item in json_lines.reader(f):
        list_of_dict.append(item)
        if len(list_of_dict)==5:
            break

print(list_of_dict)


# for line in open('/home/nirisha/amitness/amitness/blogs.jl'):
#     print(type(line))
#     print(line)
#     # lists.append(dict(line))
#     # if len(lists)==5:
#     break

# for i in data:
#     print(type(i))
#     break


# print(lists)

