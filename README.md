# BlackBerry Interview Prompt
The code in this repository was written and designed by Garrett Michiels.

This code creates a RESTful Web API that takes in GUID's and stores them in a Redis cache and MongoDB database.
The database is formatted as a collection where each entry is a document in a collection containing the GUID, the expiration, and the user.

## How to run
It is recommended that a python virtual environment be used. When doing so, make sure to run:
```bash
pip install -r requirements.txt
```

Before running the python code, make sure to be running a Redis server and MongoDB server. You can provide any ports you would like for these but the default ones are 5555 for MongoDB and 6379 for Redis.

To easily run the API with the default ports. Run the executable _defaultRun_.

There are several input options. A port and host can be provided for both the MongoDB and Redis server.

* To change the API's Port, include: ```--apiPort <int>```

* To change the database's Host, include: ```--dbHost <str>```

* To change the database's Port, include: ```--dbPort <int>```

* To change the cache's Host, include: ```--cacheHost <str>```

* To change the cache's Port, include: ```--cachePort <int>```

* To enable helpful debug messages in the terminal: ```--debug <bool>```

To run with the default values:
```python3 webAPI.py```

This is equivalent to running:
```python3 webAPI.py --dbHost localhost --cacheHost localhost --dbPort 5555 --cachePort 6379```


## Room For Improvement
- Checking for expired GUIDs in initialize() is inefficient and can be a threaded background process
- Localhost UI for GUID input.
