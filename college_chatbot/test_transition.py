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



items = ask_rates.items()
print(items)

print('error' in ask_rates)