from emora_stdm import DialogueFlow
from emora_stdm import NatexNLU, Macro



class Topic_Housing(Macro):
    def __init__(self):
        #self.model  # can load classifier here
        pass
    def run(self, sentence, vars, args):
        # type = self.model.predict(sentence)
        type = 1
        return type == 1

class Topic_Dining(Macro):
    def __init__(self):
        #self.model  # can load classifier here
        pass
    def run(self, sentence, vars, args):
        # type = self.model.predict(sentence)
        type = 1
        return type == 1


# vars = {}

macros={"Housing": Topic_Housing(), "Dining": Topic_Dining}
chatbot = DialogueFlow('start', initial_speaker=DialogueFlow.Speaker.SYSTEM, macros=macros)

initial = {
  'state': 'start',
  '"Hello! What can I help you?"': {
    'Housing': 'housing',
    'Dining': 'dining'
  }
}


housing = {
  'state': 'housing',
  '"How can I help you with Emory Housing?"': {
    '[{much, fee, rates}]': {
      '"The housing rates depends on the housing program. Which is from $4,457 - $6,276."' : {
        '[{.*}]': {
          '"See you!"': 'start' 
        }
      }
    },
    '[{options, dorm, dorms}]' : {
      '"We have 8 residence halls for first year housing. Would you like the link to the page?"':{
        '{[yes, right], #SENT(positive)}' : {'"Here is the link:\nhttps://housing.emory.edu/housing-options/residence-halls/index.html"' : 'end'},
        '[{no, never mind}]'  : {'"See you around"': 'start'}
      }
    },
    '[{move out}]': {
      '"The move out day for Spring 2022 is May 5"': 'start'
    },
    'error':{
      '"Bye!"': 'start'
    }
  } 
}


chatbot.load_transitions(housing)
chatbot.run(debugging=False)