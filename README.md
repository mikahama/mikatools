# Mikatools

Mikatools provides fast and easy methods for common Python coding tasks.
Some functionality:
 - script_path() gives the location of the current Python script
 - [json_dump(data, file_path)](https://github.com/mikahama/mikatools/wiki/JSON-and-Pickle) saves a dictionary in UTF-8 in a pretty format with indentation, real unicode characters (no unreadable escaped letters) and sorts the keys.
 - [json_load(file_path)](https://github.com/mikahama/mikatools/wiki/JSON-and-Pickle) loads json with UTF-8 encoding
 - download_file(url, path) downloads a file and saves it on the disk
 - decorators @ensure_unicode and @ensure_ascii for Python 2 developers who struggle with unicode/string distinction (i.e. all of us)
 - [open_read(file, password=None, salt=""")](https://github.com/mikahama/mikatools/wiki/Text-file-streams) opens a UTF-8 file for reading and optionally decrypts it
 - [open_write(file, password=None, salt="")](https://github.com/mikahama/mikatools/wiki/Text-file-streams) opens a UTF-8 file for writing and optionally encrypts it
 - [Super easy multitasking!](https://github.com/mikahama/mikatools/wiki/Multitasking)

[Read the wiki for more](https://github.com/mikahama/mikatools/wiki)

The library mostly provides functionality for my other libraries.
