housing_options = {
  "state": 'housing_options',
  '"There are 8 residence halls for first year students. " #RETURN_HALL_LIST() "\nWhich one do you want to know more?"': {
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
  '"What do you want to know more about?"':{
    '[{where, location}]':{
      '"Here is the location: " #LOCATION(preferred_hall)\n What else can I help you?': 'end'
    },
    '[{contact, contacts, number}]':{
      '#CONTACT_HALL(preferred_hall)':'end'
    },
    '[{floor, [floor, plan], [rooms, look, like]}]': {
      '#FLOOR_PLAN(preferred_hall)': 'end'
    },
    'error': {
      '"Sorry I don\'t know about this information."' : 'intro_hall'
    }
  }
}
# ask location
# ask contacts
# ask room amenities
# ask floor amenities

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

# transitions = {
#     'state': 'intro_hall',
#     '"Hello. How are you?"': {
#         '[{good, okay, fine}]': {
#             '"Good. I am doing well too."': {
#                 'error': {
#                     '"See you later!"': 'end'
#                 }
#             }
#         },
#         'error': {
#             '"Well I hope your day gets better!"': {
#                 'error': {
#                     '"Bye!"': 'end'
#                 }
#             }
#         }
#     }
# }