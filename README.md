# BlackBerry Interview Prompt
The code in this repository was written and designed by Garrett Michiels.

This code creates a RESTful Web API that takes in GUID's and stores them in a Redis cache and MongoDB database.
The database is formatted as a collection where each entry is a document containing the GUID, the expiration, and the user.
## How to run
It is recommended that a python virtual environment be used. When doing so, make sure to run:
```bash
pip install -r requirements.txt
```

Before running the python code, make sure to be running a Redis server and MongoDB server.

There are several input options. A port and host can be provided for both the MongoDB and Redis server.

To change the database's Host, add: ```--dbHost <str>```

To change the database's Port, add: ```--dbPort <int>```

To change the cache's Host, add: ```--cacheHost <str>```

To change the cache's Port, add: ```--cachePort <int>```

To get helpful debug messages in the terminal: ```--debug <bool>```

To run with the default values:
```python3 webAPI.py```

This is equivalent to running:
```python3 webAPI.py --dbHost localhost --cacheHost localhost --dbPort 5555 --cachePort 6379```


## Improvements
- The cache and database are being accessed upon each request. Could keep an open line to the two and not open them each time.
- Localhost UI for GUID input.
