# Running the script

`usage: python3 main.py`

Before running you will need to create a .env file that you'll need to populate with the following:

```
# clientId under authentication controls on source environment
CLIENT_ID=''
# secret of above
SECRET=''
# clientId under authentication controls on destination environment
DEST_CLIENT_ID=''
# secret of above
DEST_SECRET=''
# source base url endpoint and interpolated url for api calls specifically to get AF config
GET_FLOW_URL=''
# dest base url endpoint and interpolated url for api calls specifically to post AF Config
POST_FLOW_URL=''
# dest environment url to update action flows via api. We use this to update the name
UPDATE_FLOW_URL=''
# source auth url to get token for API source calls
SOURCE_AUTH_URL=''
# dest auth url to get token for API dest calls
DEST_AUTH_URL=''
# source environment id
SOURCE_ENV=''
# dest environment id
DEST_ENV=''
```

# Dependencies

Dependencies are listed in the requirements.txt file. You can install them by running `pip install -r requirements.txt`

# Adding the Action Flows to move

In `BackgroundWorker.py` in `def run` there is a list of action flows to move. You can add or remove from this list as needed.
The list is just a simple json list of action flow ids from the source, and the name you want saved to the destination. 

Format is as follows:
```
flows = [
    {'id': 'ABC123', 'name': 'The name you want it called in the destination'},
]
```

# How to use the app

To run just hit the `Move AFs` button and it'll move the AFs automatically. The text box under the button will update with the status of each move.

There isn't a lot of robust error handling, so be aware of that. For a simple script I didn't think it really required it.

