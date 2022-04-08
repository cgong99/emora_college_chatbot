
from emora_stdm import DialogueFlow
from emora_stdm import NatexNLU, Macro
from marco import *




macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE()
}

chatbot = DialogueFlow('Housing-Rates', initial_speaker=DialogueFlow.Speaker.SYSTEM, macros={"Topic": macros()})
transitions = {
  "state": "Housing-Rates",
  "Looks like you want to know the housing rates. Sure, we have 8 residence hall\
  for first year students. Which one do you want to know?":{
    "[$hall = #CATCH_HALLS()]": {
      "#GET_HALL_RATES()": "restart"
    }
  }

}
chatbot.load_transitions(transitions)
chatbot.run(debugging=False)