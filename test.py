#encoding: utf-8
from mikatools import *
from mikatools import crypto
import random

"""
def counter(max):
	random.seed()
	w = open_write(str(random.randint(1,101)) + "_tmp.txt")
	for i in range(max):
		w.write(str(i) + "\n")
	w.close()


jobs = [{"max":10000},{"max":10000},{"max":10000},{"max":10000},{"max":10000},{"max":10000}]

t = WorkerRunner(counter, jobs, 2)
t.start()
print("all done")
"""
#data = {"hats":{"paper": 2, "funny": 4}, "owners ages": [4,5,8], "true":"yeah", "very":{"deep":{"dict":2}}}

#print_json_help(data)

"""
text = "salainen viestini\nsala_sala"
o = open_write("secret.txt", password="super", salt="secret")
o.write(text,line_breaks=False)
o.write(text)
o.close()


i = open_read("secret.txt", password="super", salt="secret")
for x in i:
	print("line read:")
	print(x)
"""
"""
secret_data = {"Росси́я":"العربية"}
json_dump(secret_data, "secret.json", password="secret", salt="very")
print(json_load("secret.json", password="secret", salt="very"))
pickle_dump(secret_data, "secret.bin", password="secret", salt="very")
print(pickle_load("secret.bin", password="secret", salt="very"))


text = "salainen viestini\nsala_sala"
private, public = crypto.generate_keys()
o = open_write("secret.txt", key=public)
o.write(text)
o.write(text)
o.close()


i = open_read("secret.txt", key=private)
for x in i:
	print("line read:")
	print(x)

private, public = crypto.generate_keys()
secret_data = {"Росси́я":"العربية"}
json_dump(secret_data, "secret.json", key=public)
print(json_load("secret.json", key=private))
pickle_dump(secret_data, "secret.bin", key=public)
print(pickle_load("secret.bin", key=private))

"""

download_file("https://github.com/mikahama/natas/blob/master/natas/models/normalization.pt?raw=true", "norm.pt", show_progress=True)