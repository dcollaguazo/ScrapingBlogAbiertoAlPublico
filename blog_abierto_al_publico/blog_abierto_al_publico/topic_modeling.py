import json
import nltk

with open('C:/Users/DANIELACO/blog_abierto_al_publico/output.json') as data_file:
	data = json.load(data_file)

blog_content = []

for i in range(20,25):
	blog_content.append(str(data[i]['blog_content']))

print(type(blog_content[0]))



