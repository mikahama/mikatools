# Mikatools

Mikatools provides fast and easy methods for common Python coding tasks.
Some functionality:
 - script_path() gives the location of the current Python script
 - json_dump(data, file_path) saves a dictionary in UTF-8 in a pretty format with indentation, real unicode characters (no unreadable escaped letters) and sorts the keys.
 - json_load(file_path) loads json with UTF-8 encoding
 - download_file(url, path) downloads a file and saves it on the disk
 - decorators @ensure_unicode and @ensure_ascii for Python 2 developers who struggle with unicode/string distinction (i.e. all of us)

The library mostly provides functionality for my other libraries.