from emora_stdm import CompositeDialogueFlow,DialogueFlow,Macro
from enum import Enum
from marco import *

# cdf = CompositeDialogueFlow('root', 'recovery_from_failure', 'recovery_from_failure',
#                             DialogueFlow.Speaker.USER, kb=central_knowledge)

# use for multiple flows
# cdf = CompositeDialogueFlow('start', 'topic_err', 'topic', initial_speaker=DialogueFlow.Speaker.USER)


# single flow

class State(Enum):
  START = 0
  HOUSING_GENERALL = 1
  HALL_OPTIONS = 2
  HOUSING_HALL = 3
  HALL_OPTIONS_ANSWER = 4
  
  Alabama = 5
  Complex = 6
  Eagle = 7
  Hamilton = 8
  Raoul = 9
  Turman = 10
  Dobbs = 11
  Harris = 12
  


macros = {
  "CATCH_HALLS": CATCH_HALL(),
  "GENERATE_HALL_RESPONSE": GENERATE_HALL_RESPONSE()
}

df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)



# preferred hall
# 


standard_opening = '"Hi this is Emory Housing. How can I help you?" #SET($preferred_hall=None)'

# START
df.add_system_transition(State.START, State.START, standard_opening)


# USER QUESTIONS
# 1. asking hall optinos
df.add_user_transition(State.START, State.HALL_OPTIONS, '[what, {housing, options}]')
# 2. housing rates/ costs/ fee/ .....
# 3. Date ddl
# 4. Application
# 5. Contacts
# 6. Hall amenities
# 7. Room amenities/ Floor plan





df.add_system_transition(State.HALL_OPTIONS, State.HALL_OPTIONS_ANSWER, "There are 8 residence halls for first year students. #GENERATE_HALL_RESPONSE()")
# residenthall state

# USER CATCH PREFERRED HALL
df.add_user_transition(State.HALL_OPTIONS_ANSWER, State.HALL_OPTIONS_ANSWER, '[$preferred_hall=#CATCH_HALLS()]')

# go to each housing branch. or pass hall as a variable



if __name__ == '__main__':
    # automatic verification of the DialogueFlow's structure (dumps warnings to stdout)
    df.check()
    df.precache_transitions()
    # run the DialogueFlow in interactive mode to test
    df.run(debugging=False)
