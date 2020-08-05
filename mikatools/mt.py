import codecs
import random

def make_mt_valid(file1, file2, sample_len=5000):
	"""
	Samples randomly sample_len pairs of source and target senteces and saves them in files ending _valid.txt
	If there are less than sample_len pairs, a half of the pairs is sampled.
	The files are treated as UTF-8
	:param file1: A path to the source file such as source.txt --> output to source_valid.txt
	:param file2: A path to the target file such as target.txt --> output to target_valid.txt
	"""
	sources = codecs.open(file1, "r", encoding="utf-8").read().split("\n")
	targets = codecs.open(file2, "r", encoding="utf-8").read().split("\n")
	
	source_valid = codecs.open(file1.replace(".txt", "") + "_valid.txt", "w", encoding="utf-8")
	target_valid = codecs.open(file2.replace(".txt", "") + "_valid.txt", "w", encoding="utf-8")
	random.seed()
	if len(sources) > sample_len:
		valids = random.sample(range(len(sources)), sample_len)
	else:
		valids = random.sample(range(len(sources)), int(len(sources)/2))
	for valid in valids:
		source_valid.write(sources[valid] + "\n")
		target_valid.write(targets[valid] + "\n")
	source_valid.close()
	target_valid.close()