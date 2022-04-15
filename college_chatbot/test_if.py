import emora_stdm
from emora_stdm import Macro
from emora_stdm import DialogueFlow
from typing import Union, Set, List, Dict, Callable, Tuple, NoReturn, Any
from emora_stdm.state_transition_dialogue_manager.ngrams import Ngrams

class CheckIF(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        print("args:" , args)
        print("vars: ", vars)
        for arg in args:
            if not _term_op_term(arg, vars):
                return False
        return True
      
      
def _term_op_term(arg, vars):
    if isinstance(arg, str):
        if '<=' in arg:
            operator = '<='
            t1, t2 = _get_terms(arg, operator, vars)
            return float(t1) <= float(t2)
        elif '>=' in arg:
            operator = '>='
            t1, t2 = _get_terms(arg, operator, vars)
            return float(t1) >= float(t2)
        elif '!=' in arg:
            operator = '!='
            t1, t2 = _get_terms(arg, operator, vars)
            return t1 != t2
        elif '<' in arg:
            operator = '<'
            t1, t2 = _get_terms(arg, operator, vars)
            return float(t1) < float(t2)
        elif '>' in arg:
            operator = '>'
            t1, t2 = _get_terms(arg, operator, vars)
            return float(t1) > float(t2)
        elif '=' in arg:
            operator = '='
            t1, t2 = _get_terms(arg, operator, vars)
            print("T1: ", t1)
            print("T2: ", t1)
            return t1 == t2
        elif '$' == arg[0]:
            if arg[1:] not in vars:
                return False
            return bool(vars[arg[1:]])
        else:
            return None
    else:
        return bool(arg and arg != 'None')
      
def _get_terms(arg, operator, vars):
    t1, t2 = arg.split(operator)
    if t1[0] == '$':
        var = t1[1:]
        t1 = vars[var] if var in vars else 'None'
    if t2[0] == '$':
        var = t2[1:]
        t2 = vars[var] if var in vars else 'None'
    return t1, t2
  
  
macros = {
  "CHECKIF" : CheckIF()
}
chatbot = DialogueFlow('start', macros=macros)

transitions = {
    'state': 'start',
    '"Hello. How are you?"': {
        '[$type={rates, housing}]': {
          '$type':'start'
        },
        '[$type={rates, housing}]#CHECKIF($type=\'rates\')': {
            '"Rates!"': {
                'error': {
                    '"See you later!"': 'start'
                }
            }
        },
        '[$type={rates, housing}]#CHECKIF($type=\'housing\')':{
          '"Housing!"': 'end'
        },
        'error': {
            '"Well I hope your day gets better!"': {
                'error': {
                    '"Bye!"': 'start'
                }
            }
        }
    }
}

chatbot.load_transitions(transitions)
chatbot.run()