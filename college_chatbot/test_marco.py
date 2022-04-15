
from emora_stdm import DialogueFlow
from emora_stdm import NatexNLU, Macro
from marco import *




macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE(),
  "GET_ROOM_TYPE": GET_ROOM_TYPE(),
  "GET_RATES": GET_RATES()
}


ask_rates = {
  "state": 'rates',
  '"Looks like you want to know the housing rates. Sure, we have 4 different room types: \n Single\n Double \n Triple\n Super Single\n\
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


if __name__ == '__main__':
  chatbot = DialogueFlow('rates', initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)
  chatbot.load_transitions(ask_rates)
  chatbot.run(debugging=False)

  

