# Mikatools

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3977549.svg)](https://doi.org/10.5281/zenodo.3977549)

Mikatools provides fast and easy methods for common Python coding tasks.
Some functionality:
 - [script_path()](https://github.com/mikahama/mikatools/wiki/Miscellaneous#script_pathjoin_filenone) gives the location of the current Python script
 - [json_dump(data, file_path)](https://github.com/mikahama/mikatools/wiki/JSON-and-Pickle) saves a dictionary in UTF-8 in a pretty format with indentation, real unicode characters (no unreadable escaped letters) and sorts the keys.
 - [json_load(file_path)](https://github.com/mikahama/mikatools/wiki/JSON-and-Pickle) loads json with UTF-8 encoding
 - [download_file(url, path, show_progress=False)](https://github.com/mikahama/mikatools/wiki/Miscellaneous#download_fileurl-path-show_progressfalse) downloads a file and saves it on the disk
 - [open_read(file, password=None, salt=""")](https://github.com/mikahama/mikatools/wiki/Text-file-streams) opens a UTF-8 file for reading and optionally decrypts it
 - [open_write(file, password=None, salt="")](https://github.com/mikahama/mikatools/wiki/Text-file-streams) opens a UTF-8 file for writing and optionally encrypts it
 - [Super easy multitasking!](https://github.com/mikahama/mikatools/wiki/Multitasking)

[Read the wiki for more](https://github.com/mikahama/mikatools/wiki)

The library mostly provides functionality for my other libraries.

# Cite:

    @software{mika_hamalainen_2020_3977549,
      author       = {Mika Hämäläinen},
      title        = {mikahama/mikatools 1.0.0},
      month        = aug,
      year         = 2020,
      publisher    = {Zenodo},
      version      = {1.0.0},
      doi          = {10.5281/zenodo.3977549},
      url          = {https://doi.org/10.5281/zenodo.3977549}
    }


