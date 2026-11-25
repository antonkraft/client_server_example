# Client Server Example 
This repository contains a small file transmission application implemented with Python.

## What it does
The Client waits for the Server to respond, the Server waits for a Client to connect. Both end the execution after a given time (default 5 seconds).
On a successful connection the Client transmits a given file to the Server. The Server stores the file under the same name inside a given folder. If the file already exists, the file is not overwritten.
Transmission is displayed in form of a progress bar on the Client side.
After a successful file transmission, both applications end.

## Further improvements
Not required but desired features are:
* Server runs to serve connections in series
* Server handling multiple Clients (queue)
* Server notifying Client, if file already exists, to abort connection and save bandwidth.

## Requirements
* make
* Python 3
* Windows 11 (probably works on Win 10 as well)

## Folder Structure
```
.
├── LICENCE: Apache 2.0
├── Makefile: for Windows
├── makefile.linux: Alternate Make for Linux, requires renaming (see below)
├── client.py: Python code for Client
├── server.py: Python code for Server
├── README.md: This file
```

## Usage
Open up two PowerShell Terminals/Command Prompts in Windows, one for the server, one for client
* `make` or `make install` to create everything necessary to run the code (once is enough)
* `make runS ARGS="--output <FOLDER>"` to run the Server and `make runC ARGS="--input <FILE>"` to run the client.
* `make clean` to revert changes made by `make install` (once is enough)
* `make test` to demonstrate the code based on a large file and display checksums for comparison (no second terminal needed for this)

### Optional flags
Client and Server have optional flags for Host, Port and Timeouts. Either of them or all three can be set. Examples:
``` bash
make runS ARGS="--host 0.0.0.0 --port 666 --timeout 100 --output <FOLDER>"
make runC ARGS="--timeout 1 --input <FILE>"
```
Default values
``` python
    HOST = "127.0.0.1"
    PORT = 8001
    TOUT = 5
```

### Usage without Make

All Make targets can be run manually from the command line.

#### Setup (once)

``` powershell
python -m venv venv
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\pip.exe install -r requirements.txt
```

#### Run
```
venv\Scripts\python.exe server.py --output <FOLDER>
venv\Scripts\python.exe client.py --input <FILE>
```

#### Optional flags /examples)
```
venv\Scripts\python.exe server.py --host 127.0.0.1 --output <FOLDER>
venv\Scripts\python.exe client.py --host 127.0.0.1 --input <FILE>
```

#### Cleanup
```
Remove-Item -Recurse -Force venv, __pycache__, test_output -ErrorAction SilentlyContinue
Remove-Item -Force test_input.txt -ErrorAction SilentlyContinue
```

## Linux
This was not tested on Linux. The makefile is therefore minimalistic. Rename _Makefile_ to something else and _makefile.linux_ to makefile.
* `make` or `make setup` to create everything necessary to run the code. Set/Unset the respective Package Manager in the first line of `makefile`
* `make runS ARGS="--output <FOLDER>"` to run the Server and `make runC ARGS="--input <FILE>"` to run the client and prepare everything for that, if necessary
* `make clean` to remove temporary files
