from emora_stdm import CompositeDialogueFlow,DialogueFlow,Macro
from enum import Enum
from marco import *

from transitions import *
# cdf = CompositeDialogueFlow('root', 'recovery_from_failure', 'recovery_from_failure',
#                             DialogueFlow.Speaker.USER, kb=central_knowledge)

# use for multiple flows
# cdf = CompositeDialogueFlow('start', 'topic_err', 'topic', initial_speaker=DialogueFlow.Speaker.USER)


# single flow
housing_info_path = "housing_info.json"

class State():
  START = "start"
  RATES = "rates"
  HOUSING_GENERALL = 1
  HALL_OPTIONS = "housing_options"
  INTRO_HALLS = "intro_hall"
  HOUSING_HALL = 3
  HALL_OPTIONS_ANSWER = 4

  


macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE(),
  "GET_ROOM_TYPE": GET_ROOM_TYPE(),
  "GET_RATES": GET_RATES(),
  "RETURN_HALL_LIST": RETURN_HALL_LIST(),
  "LOCATION": LOCATION(housing_info_path),
  "CONTACT_HALL": CONTACT_HALL(housing_info_path),
  "FLOOR_PLAN": FLOOR_PLAN(housing_info_path)
}

df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)



# preferred hall
# 


standard_opening = '"Hi this is Emory Housing. How can I help you?" #SET($preferred_hall=None)'

# START
df.add_system_transition(State.START, State.START, standard_opening)


# USER QUESTIONS
# 1. asking hall optinos
# 2. housing rates/ costs/ fee/ .....
# 3. Date ddl
# 4. Application
# 5. Contacts
# 6. Hall amenities
# 7. Room amenities/ Floor plan


# USER HALL OPTIONS
df.add_user_transition(State.START, State.HALL_OPTIONS, '[what, {housing, options}]')
# rates question
df.add_user_transition(State.START, State.RATES, '[{rates, fee, cost}]')
# specific hall
df.add_user_transition(State.START, State.INTRO_HALLS, '$preferred_hall=#CATCH_HALLS()')




# SYSTEM
# df.add_system_transition(State.HALL_OPTIONS, State.HALL_OPTIONS_ANSWER, "There are 8 residence halls for first year students. #GENERATE_HALL_RESPONSE()")
# df.load_transitions(ask_rates) # RATES
# df.add_system_transition("rates", State.START, ask_rates)
# residenthall state

# USER CATCH PREFERRED HALL
# df.add_user_transition(State.HALL_OPTIONS_ANSWER, State.HALL_OPTIONS_ANSWER, '[$preferred_hall=#CATCH_HALLS()]')

# go to each housing branch. or pass hall as a variable



if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    df.load_transitions(ask_rates)
    df.load_transitions(housing_options)
    df.load_transitions(intro_hall)
    # df.load_transitions(transitions)
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=False)
