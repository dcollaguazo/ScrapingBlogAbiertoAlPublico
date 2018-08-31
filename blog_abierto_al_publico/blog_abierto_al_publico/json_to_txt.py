from os import path, listdir
import io
import sys, getopt
import json

def json_to_txt_converter(filename:str):
	with open(filename) as json_data:
		d = json.load(json_data)
		counter = 0
		for item in d:
			counter+=1
			content = item['blog_content'][0]
			title = item['title']
			# print(filename)
			with open('../txts/blog_' + str(counter) + ".txt","w", encoding="utf-8") as f:
				f.write(title + " " + content)
				f.close()

if __name__ == "__main__":
	filename = "../abierto.json"
	json_to_txt_converter(filename)