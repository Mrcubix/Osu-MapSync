# Osu-MapSync
A tool that will allow the sync of you BM, scores, replays and collection from a pc to another using different methods

Testing is the only thing left to be done

Right now this tool support Windows  
Linux and MacOS hasn't been tested yet

Todo list:

- Add more sync methods
- Cleanup

# Supported Sync method

- FTP
- SSH
- localfile

# Usage:

Download and install python 3.6+
Open `Sync.py` > `help` for a list of commands

- Sync: Upload your data to a remote of local server of your choice for update on another machine
- Update: Update your local files with data from a local or remote server
- Help: Show this list of commands

# Credits:
I would like to thank:

- [Tadeo](https://github.com/tadeokondrak) for making the code for the dumper and serializer for osu!.db (bad.exe) and auhorizing me to use it in my project
- [KirkSuD](https://github.com/KirkSuD) for making [osudb](https://github.com/KirkSuD/osudb) a parser for every db file

# Note:

- FTPlib can't create folder on root of internal and external storage, so make sure your android FTP server root path isn't any of those