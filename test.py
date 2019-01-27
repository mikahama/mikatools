#encoding: utf-8
from mikatools import *
import random

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

