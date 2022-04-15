


from emora_stdm.state_transition_dialogue_manager.dialogue_flow import DialogueFlow


class NewDialogueFlow(DialogueFlow):
  def add_transitions(self, json_dict, speaker=None):
    """_summary_
      input: transitions, speaker state, state
      recursive
    """
    if 'state' in json_dict:
        source = json_dict['state']
    else:
        source = DialogueFlow.autostate()    
    transitions = []
    
    # set up transitions
    expanded_transitions = []
    
    # set up transitions
    expanded_transitions = []
    for natex, target in transitions:
        natex_with_leading_digits_stripped = ''
        i = 0
        c = natex[i] if natex else ''
        while c and c.isnumeric():
            natex_with_leading_digits_stripped += c
            i += 1
            c = natex[i] if i < len(natex) else ''
        if natex == 'error':
            if isinstance(target, dict):
                if 'state' not in target:
                    target['state'] = DialogueFlow.autostate()
                expanded_transitions.append(target)
                target = target['state']
                if not self.has_state(target):
                    self.add_state(target)
            self.set_error_successor(source, target)

        else:
            score = 1.0
            if isinstance(target, dict):
                if 'state' not in target:
                    target['state'] = DialogueFlow.autostate()
                if 'score' in target:
                    score = target['score']
                expanded_transitions.append(target)
                target = target['state']
                if not self.has_state(target):
                    self.add_state(target)
            if speaker == Speaker.USER:
                if self.has_transition(source, target, Speaker.USER):
                    intermediate = '_' + self.autostate()
                    self.add_state(intermediate, target)
                    self.add_user_transition(source, intermediate, natex + ' #TARGET(%s)' % target, score=score)
                else:
                    self.add_user_transition(source, target, natex, score=score)
            elif speaker == Speaker.SYSTEM:
                if self.has_transition(source, target, Speaker.SYSTEM):
                    intermediate = '_' + self.autostate()
                    self.add_state(intermediate)
                    self.add_system_transition(source, intermediate, natex + ' #TARGET(%s)' % target, score=score)
                else:
                    self.add_system_transition(source, target, natex, score=score)

    # switch turn (will be switched back if multi hop detected on next recursive call)
    # if speaker == Speaker.USER:
    #     speaker = Speaker.SYSTEM
    # elif speaker == Speaker.SYSTEM:
    #     speaker = Speaker.USER

    # recurse to load nested turns
    for transition in expanded_transitions:
        self.load_transitions(transition, speaker)
