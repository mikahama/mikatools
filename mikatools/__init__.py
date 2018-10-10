#encoding: utf-8
import json, codecs, pickle, requests, os, sys
from clint.textui import progress

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

def script_path():
	return os.path.dirname(os.path.abspath(sys._getframe().f_back.f_globals["__file__"]))

def pickle_dump(data, file_path):
	pickle.dump(data, open(file_path, "wb"))

def pickle_load(data, file_path):
	return pickle.load(open(file_path, "rb"))

def json_dump(data, file_path, sort_keys=True):
	json.dump(data, codecs.open(file_path, "w", encoding="utf-8"),indent=4, sort_keys=sort_keys, ensure_ascii=False)

def json_load(file_path):
	return json.load(codecs.open(file_path, "r", encoding="utf-8"))

def open_read(file_path):
	return codecs.open(file_path, "r", encoding="utf-8")

def open_write(file_path):
	return codecs.open(file_path, "w", encoding="utf-8")

def download_json(url, args={}):
	r = requests.get(url, **args)
	return r.json()

def download_file(url, path, show_progress=False):
	if show_progress:
		__download_file_with_bar(url, path)
	else:
		file = urlopen(url)
		with open(path ,'wb') as output:
			output.write(file.read())
		output.close()


def __download_file_with_bar(url, path):
	r = requests.get(url, stream=True)
	with open(path, 'wb') as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
			if chunk:
				f.write(chunk)
				f.flush()

def ensure_unicode(func):
	def wrapper(*args, **kwargs):
		text = func(*args, **kwargs)
		if type(text) is str:
			text = text.decode("utf-8")
		return text
	return wrapper

def ensure_ascii(func):
	def wrapper(*args, **kwargs):
		text = func(*args, **kwargs)
		if type(text) is unicode:
			text = text.encode("utf-8", 'ignore')
		return text
	return wrapper

class SafeDict(dict):
	def __init__(self, empty_type, init_params={}, *args, **kw):
		self.empty_type = empty_type
		self.init_params = init_params
		super(SafeDict,self).__init__(*args, **kw)

	def __getitem__(self, item):
		if item not in self.keys():
			self[item] = self.__give_empty__()
		return super(SafeDict,self).__getitem__(item)

	def __give_empty__(self):
		return self.empty_type(**self.init_params)
