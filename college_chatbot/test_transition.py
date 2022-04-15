ask_rates = {
  "state": 'rates',
  '"Hi"':{
    "[$room=#GET_ROOM_TYPE()]": {
      '"Good"': {
        "error": 'rates'
      }
    },
    'error' : {
      '"Sorry "' : "end"
    }
  }
}

intro_hall = {
  "state": 'intro_hall',
  '"What do you want to know about" $preferred_hall':{
    '[{where, location}]':{
      "#LOCATION(preferred_hall)": 'end'
    },
    '[{contacts, number}]':{
      '"contact"':'end'
    },
    'error': {
      '"Sorry I don\'t know about this information."' : 'intro_hall'
    }
  }
}


import json
path = "housing_info.json"
path = path
with open(path, 'r') as f:
  db = json.load(f)

print(db.keys())
print(db['alabama'])
print(db['alabama']['Staff'])
print(list(db['alabama']['Staff'].keys()))