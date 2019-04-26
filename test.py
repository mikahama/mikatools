#encoding: utf-8
from mikatools import *
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
data = {"hats":{"paper": 2, "funny": 4}, "owners ages": [4,5,8], "true":"yeah", "very":{"deep":{"dict":2}}}

print_json_help(data)