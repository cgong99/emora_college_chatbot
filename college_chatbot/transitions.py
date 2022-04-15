housing_options = {
  "state": 'housing_options',
  '"There are 8 residence halls for first year students. " "Which one do you want to know more?"': {
    '[$preferred_hall=#CATCH_HALLS()]': 'intro_hall',
    'error': {
      '"Sorry I don\'t think I know this name. Do you want to try another name or say return I can help you with other things?"': {
        '[$preferred_hall=#CATCH_HALLS()]': 'intro_hall',
        'error': 'start'
      }
    }
  }
}

intro_hall = {
  "state": 'intro_hall',
  '"What do you want to know about $preferred_hall?"':{
    '[location]':"good questions",
    'error':'start'
  }
}

ask_rates = {
  "state": 'rates',
  '"Looks like you want to know the housing rates. Sure, we have 4 different room types: \n  Single\n  Double \n  Triple\n  Super Single\n\
  Which one do you want to know about?"':{
    "[$room=#GET_ROOM_TYPE()]": {
      '"The rate for" $room "room would be" #GET_RATES(room) "dollars per semester."': {
        "error": 'rates'
      }
    },
    'error' : {
      '"Sorry I don\'t quite understand that."' : "end"
    }
  }
}

