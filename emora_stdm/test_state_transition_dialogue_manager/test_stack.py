
import pytest
from emora_stdm.state_transition_dialogue_manager.dialogue_flow import DialogueFlow

def test_stack():
    df = DialogueFlow('root')
    transitions = {
        'state': 'root',

        '#GOAL(grandma_hospital) '
        '`I cannot concentrate on a lot of things right now. '
        'My grandma is in the hospital. `'
        '$__goal_return_phrase__=`What should I do?`':{
            '[{[{dont,shouldnt,not},worry],calm,relax,distract,[mind,off]}]':{
                'state': 'dont_worry',

                '#SET($__goal_return_state__=dont_worry) #GATE '
                '"Okay, I will try my best not to worry. It\'s hard because she lives by '
                'herself and won\'t let anyone help her very much, so I feel like this '
                'will just happen again."':{
                    '[{sorry,sucks,hard}]':{
                        '"yeah, thanks."': {}
                    },
                    '[will,better]':{
                        '"I really hope you are right."': {}
                    },
                    'error': {
                        'state': 'feel_better',
                        '"I actually feel a little bit better after talking with you. Thanks for listening. "'
                    }
                },
                'default': 'feel_better'
            },
            '#IDK':{
                '"yeah, i dont know either. Its so tough."': {}
            }
        }
    }

    gma = {
        '#GOAL(why_grandma_hospital) '
        '[{[why,hospital],wrong,happened}]': {
            '"She is just so frail. I can hardly believe it. '
            'She fell off of a stool in the kitchen and broke her hip."': {
                '[dont worry]':{
                    '#GRET(grandma_hospital,dont_worry)'
                },
                'error':{
                    '#GRET': 'return'
                }
            }
        },
        '#GOAL(grandma_hospital_before) '
        '[{has,was},{she,grandma},hospital,{before,earlier,previously}]': {
            '"No, this is the first time, thank goodness."': {
                'error':{
                    '#GRET': 'return'
                }
            }
        }
    }

    df.load_transitions(transitions)
    r = df.system_turn()
    assert df.vars()['__goal__'] == 'grandma_hospital'

    df.user_turn("what happened")
    assert df.vars()['__goal__'] == 'why_grandma_hospital'
    assert len(df.vars()['__stack__']) == 2
    assert df.vars()['__stack__'][1][0] == 'why_grandma_hospital'
    assert df.vars()['__stack__'][0][0] == 'grandma_hospital'

    assert "fell off of a stool" in df.system_turn()
    assert df.vars()['__goal__'] == 'grandma_hospital'
    assert len(df.vars()['__stack__']) == 1
    assert df.vars()['__stack__'][0][0] == 'grandma_hospital'

    df.user_turn("oh no")
    assert "What should I do" in df.system_turn()

    df.user_turn("dont worry")
    assert df.vars()['__goal_return_state__'] == "dont_worry"

    assert "she lives by herself" in df.system_turn()
    df.user_turn("has your grandma been in the hospital before this")
    assert df.vars()['__goal__'] == 'grandma_hospital_before'
    assert len(df.vars()['__stack__']) == 2
    assert df.vars()['__stack__'][1][0] == 'grandma_hospital_before'
    assert df.vars()['__stack__'][0][0] == 'grandma_hospital'

    assert "this is the first time" in df.system_turn()
    assert df.vars()['__goal__'] == 'grandma_hospital'
    assert len(df.vars()['__stack__']) == 1
    assert df.vars()['__stack__'][0][0] == 'grandma_hospital'
    assert df.state() == 'feel_better'