from emora_stdm import CompositeDialogueFlow,DialogueFlow,Macro
from enum import Enum
from marco import *

from transitions import *
# cdf = CompositeDialogueFlow('root', 'recovery_from_failure', 'recovery_from_failure',
#                             DialogueFlow.Speaker.USER, kb=central_knowledge)

# use for multiple flows
# cdf = CompositeDialogueFlow('start', 'topic_err', 'topic', initial_speaker=DialogueFlow.Speaker.USER)


# single flow

class State():
  START = "start"
  RATES = "rates"
  HOUSING_GENERALL = 1
  HALL_OPTIONS = "housing_options"
  HOUSING_HALL = 3
  HALL_OPTIONS_ANSWER = 4

  


macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE(),
  "GET_ROOM_TYPE": GET_ROOM_TYPE(),
  "GET_RATES": GET_RATES()
}

df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)
# how to use knowledgeBase?
# knowledge = KnowledgeBase()
# knowledge.load_json_file(OPENINGDIR.replace('__***__','opening_database.json'))


standard_opening = '"Hi this is Emory Housing. How can I help you?" #SET($preferred_hall=None)'

# START
df.add_system_transition(State.START, State.START, standard_opening)

# USER HALL OPTIONS
df.add_user_transition(State.START, "housing_options", '[what, {housing, options}]')
# rates question
df.add_user_transition(State.START, "rates", '[{rates, fee, cost}]')
# 




# SYSTEM
# df.add_system_transition(State.HALL_OPTIONS, State.HALL_OPTIONS_ANSWER, "There are 8 residence halls for first year students. #GENERATE_HALL_RESPONSE()")
# df.load_transitions(ask_rates) # RATES
# df.add_system_transition("rates", State.START, ask_rates)
# residenthall state

# USER CATCH PREFERRED HALL
df.add_user_transition(State.HALL_OPTIONS_ANSWER, State.HALL_OPTIONS_ANSWER, '[$preferred_hall=#CATCH_HALLS()]')

# go to each housing branch. or pass hall as a variable



if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    df.load_transitions(ask_rates)
    df.load_transitions(intro_hall)
    df.load_transitions(housing_options)
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=False)
