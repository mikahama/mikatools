#encoding: utf-8
import json, codecs, pickle, requests, os, sys
from tqdm import tqdm
try:
	#python 3
	from queue import Queue
except ImportError:
	#python2
	from Queue import Queue
from threading import Thread
import os.path
from multiprocessing import Process
from multiprocessing import JoinableQueue
from .crypto import CryptoReadStream, CryptoWriteStream, base64
import warnings

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def file_exists(file, accept_directories=False):
	"""
	Checks whether a file exists or not
	:param file: Path to the file or folder to test
	:param accept_directories: Sets whether directories return True
	:type file: string
	:type accept_directories: bool
	:return: Returns a bool indicating whether the file exists
	:rtype: bool
	"""
	if not accept_directories:
		return os.path.isfile(file)
	else:
		return os.path.exists(file)

def script_path(join_file=None):
	"""
	Returns the path to the caller Python script
	:return: path to the Python string
	:rtype: string
	"""
	path = os.path.dirname(os.path.abspath(sys._getframe().f_back.f_globals["__file__"]))
	if join_file is None:
		return path
	else:
		return os.path.join(path, join_file)

def pickle_dump(data, file_path, password=None, salt="", key=None,key_password=None):
	"""
	Pickles an object into a file by path
	:param data: an object to be pickled
	:param file_path: path to the file
	:type data: object
	:type file_path: string
	"""
	if password or key:
		crypto_text = base64.urlsafe_b64encode(pickle.dumps(data)).decode("utf-8")
		text_dump(file_path, crypto_text,password=password, salt=salt, key=key,key_password=key_password)
	else:
		pickle.dump(data, open(file_path, "wb"))

def pickle_load(file_path, password=None, salt="", key=None, key_password=None):
	"""
	Loads a pickled object by path
	:param file_path: Path to the file
	:type file_path: string
	:return: The loaded object
	:rtype: object
	"""
	if password or key:
		f = open_read(file_path, password=password, salt=salt, key=key,key_password=key_password)
		d = pickle.loads(base64.urlsafe_b64decode(f.read()))
		f.close()
		return d
	else:
		return pickle.load(open(file_path, "rb"))

def print_json_help(json_dictionary, indent=0, indent_char="  "):
	"""
	Prints a json formated help file
	For example, {"key1":"value", "key2":[2,4], "key3":{"key":"value"}} prints out
	- key1:
	  value
	- key2:
	  2, 4
	- key3:
	  - key:
	    value
	:param json_dictionary: A dictionary containing json compatible data
	:type json_dictionary: dict
	:param indent: How much indent should there be for the keys
	:type indent: int
	:param indent_char: A string that is used to indent
	:type indent_char: string
	"""
	tabs = indent_char*indent
	for key, value in json_dictionary.items():
		print(tabs +"- " + key + ":")
		if type(value) is dict:
			print_json_help(value, indent=indent+1, indent_char=indent_char)
		elif type(value) is list:
			print(tabs + indent_char + ", ".join(str(x) for x in value))
		else:
			print(tabs + indent_char + str(value))

def json_dump(data, file_path, sort_keys=True,  allow_overwrite=True, append=False, password=None, salt="", key=None,key_password=None):
	"""
	Dumps a dictionary into JSON always in UTF-8 encoding and outputting the letters as they are (no ugly escaping)
	:param data: The dictionary to be dumped
	:param file_path: Path to the file
	:param sort_keys: Should the keys be sorted
	:type data: dict
	:type file_path: string
	:type sort_keys: bool
	"""
	with open_write(file_path, password=password, salt=salt, allow_overwrite=allow_overwrite, append=append, key = key,key_password=key_password) as file_handle:
		json.dump(data, file_handle ,indent=4, sort_keys=sort_keys, ensure_ascii=False)

def json_load(file_path, default_dictionary=None, password=None, salt ="", key=None, key_password=None, line_by_line=False):
	"""
	Loads an UTF-8 encoded JSON
	:param file_path: Path to the JSON file
	:param default_dictionary: Dictioary to return if file is not found
	:type file_path: string
	:rtype: dict
	:return: The JSON dictionary
	"""
	with open_read(file_path, password=password, salt=salt, key = key, key_password=key_password) as file_handle:
		if default_dictionary is not None:
			try:
				return json.load(file_handle)
			except:
				return default_dictionary
		elif line_by_line:
			res = []
			for i, l in enumerate(file_handle):
				try:
					res.append(json.loads(l))
				except Exception as e:
					warnings.warn("Line " +str(i + 1) + ": " + str(e) , ResourceWarning)
			return res
		else:
			return json.load(file_handle)


def open_read(file_path, password=None, salt="", key=None, key_password=None):
	"""
	Opens a file for reading in UTF-8
	:rtype: file
	:param file_path: Path to file
	:type file_path: string
	:return: A file opened for reading
	"""
	if password or key:
		return CryptoReadStream(file_path, password, salt=salt, key=key, key_password=key_password)
	return codecs.open(file_path, "r", encoding="utf-8")

def open_write(file_path, allow_overwrite=True, append=False, password=None, salt="", key=None, key_password=None):
	"""
	Opens a file for writing in UTF-8
	:rtype: file
	:param file_path: Path to file
	:type file_path: string
	:return: A file opened for writing
	"""
	mode = "w"
	if append:
		mode = "a"
	elif not allow_overwrite:
		mode = "x"
	if password or key:
		return CryptoWriteStream(file_path, password, salt=salt, allow_overwrite=allow_overwrite, append=append, key=key, key_password=key_password)
	return codecs.open(file_path, mode, encoding="utf-8")

def text_dump(file_path, text, allow_overwrite=True, append=False, password=None, salt="", key=None, key_password=None):
	"""
	Opens a file for writing in UTF-8, writes text and closes the file
	:rtype: file
	:param file_path: Path to file
	:type file_path: string
	:return: A file opened for writing
	"""
	f = open_write(file_path, allow_overwrite=allow_overwrite, append=append, password=password, salt=salt, key=key, key_password=key_password)
	f.write(text)
	f.close()

def download_json(url, args={}):
	"""
	Downloads a JSON
	:param url: The URL of the JSON
	:type url: string
	:param args: Optional keyword arguments for requests
	:type args: dict
	:return: The downloaded JSON
	:rtype: dict
	"""
	r = requests.get(url, **args)
	return r.json()

def download_file(url, path, show_progress=False):
	"""
	Downloads a file and saves it to a path

	:param url: The URL of the file
	:type url: string
	:param path: A path for saving the file
	:type path: string
	:param show_progress: Use True to show a progress bar in terminal
	:type show_progress: bool
	"""
	if show_progress:
		__download_file_with_bar(url, path)
	else:
		file = urlopen(url)
		with open(path ,'wb') as output:
			output.write(file.read())
		output.close()


def __download_file_with_bar(url, path):
	r = requests.get(url, stream=True)
	leng = r.headers.get('content-length')
	if leng is None:
		print("No content-length, cannot show progress for download")
		r = None
		download_file(url, path, False)
		return
	with open(path, 'wb') as f:
		total_length = int(leng)
		for chunk in tqdm(r.iter_content(chunk_size=1024), total=(total_length/1024) + 1): 
			if chunk:
				f.write(chunk)
				f.flush()



class SafeDict(dict):
	"""
	Mainly same as Python's inbuilt defaultdict
	"""
	def __init__(self, empty_type, init_params={}, *args, **kw):
		"""
		Intializes a SafeDict
		:param empty_type: type used if the key has no value in the dictionary
		:param init_params: keyword arguments passed to the type when initialized for a missing key
		:param args: passed to super class (dict)
		:param kw: passed to super class (dict)
		"""
		self.empty_type = empty_type
		self.init_params = init_params
		super(SafeDict,self).__init__(*args, **kw)

	def __getitem__(self, item):
		if item not in self.keys():
			self[item] = self.__give_empty__()
		return super(SafeDict,self).__getitem__(item)

	def __give_empty__(self):
		return self.empty_type(**self.init_params)


		

class WorkerRunner():
	"""
	WorkerRunner makes multi threading/processing a walk in a park!

	Just look at the following example

		def counter(max):
			random.seed()
			w = open_write(str(random.randint(1,101)) + "_tmp.txt")
			for i in range(max):
				w.write(str(i) + "\n")
			w.close()

		jobs = [{"max":10000},{"max":10000},{"max":10000},{"max":10000},{"max":10000},{"max":10000}]

		t = WorkerRunner(counter, jobs, 2)
		t.start()

	This code runs counter method in parallel to process all the jobs in the list.
	The jobs list contains a list of the keyword arguments you want to pass to the method.
	This runs all the items in the list (6 times counting till 10000) in parallel, maximum 2 at the time
	"""
	def __init__(self, function, kwarg_list, number_of_workers=4, run_as_threads=False):
		"""
		Initializes WorkerRunner
		:param function: The function to be run in parallel
		:type function: function
		:param kwarg_list: A list containing the the keyword arguments to be passed to the function
		:type kwarg_list: list
		:param number_of_workers: Number of parallel threads/processes
		:type number_of_workers: int
		:param run_as_threads: True run as threads, False run as processes. Note: threading is sort of broken in vanilla Python, but processes cannot access shared global variables as easily
		:type run_as_threads: bool
		"""
		self.function = function
		if run_as_threads:
			self.runner = Thread
			self.q = Queue()
		else:
			self.runner = Process
			self.q = JoinableQueue()

		for kwarg in kwarg_list:
			self.q.put(kwarg)
		self.number_of_workers = number_of_workers
		self.threads = []


	def _function_wrapper(self, q):
		while not q.empty():
			kwargs = q.get()
			self.function(**kwargs)
			q.task_done()


	def start(self, join=True):
		"""
		Starts the threads/processes
		:param join: If True, waits till the threads/processes are done, if False returns the queue without waiting
		:type join: bool
		:return: Returns the queue only if join=False, otherwise doesn't return anything
		:rtype: JoinableQueue or Queue
		"""
		for i in range(self.number_of_workers):
			worker = self.runner(target=self._function_wrapper, args=(self.q,))
			worker.daemon = True
			worker.start()
		if join:
			self.q.join()
		else:
			return self.q




