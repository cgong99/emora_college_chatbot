
# from emora._pets.pets import df as pet, State as pet_states

pet_str = '{pet,pets,animals,animal,cat,cats,dog,dogs}'

def add_components_to(cdf):
    # cdf.add_component(pet, 'pet')
    cdf.add_system_transition('root', 'pet_intro', '#GATE(petv:None)')

    #already talked about topic
    cdf.add_system_transition('pet_intro', 'pet_repeat_switch',
                              '#IF($petv=True) `You want to talk about animals again? `',
                              score=2.0)
    cdf.add_system_transition('pet_repeat_switch', 'pet_to_music', '`You know, ` #GATE(musicv:None)')
    cdf.add_system_transition('pet_repeat_switch', 'pet_to_sports', '`You know, ` #GATE(sportsv:None)')
    cdf.add_system_transition('pet_repeat_switch', 'pet_to_vr', '`You know, ` #GATE(virtual_realityv:None)')
    cdf.add_system_transition('pet_repeat_switch', 'pet_topic_switch',
                              '`There\'s not much more that I know about them unfortunately. Anyway, `', score=0.0)
    cdf.controller().update_state_settings('pet_repeat_switch', system_multi_hop=True)

    # cdf.add_system_transition('pet_intro', ('pet', pet_states.START_PET), '#SET($petv=True,$original_pet=True) #IF($new_pet=None)')
    cdf.controller().update_state_settings('pet_intro', system_multi_hop=True)
    # cdf.controller().update_state_settings(('pet', pet_states.START_PET), system_multi_hop=True)
    # pet.add_system_transition(pet_states.END, ('SYSTEM', 'pet_topic_switch'), '"Anyways, "')
    # pet.update_state_settings(('SYSTEM', 'pet_topic_switch'), system_multi_hop=True)
    # pet.add_system_transition(pet_states.STOP_FINAL, ('SYSTEM', 'intermediate_topic_switch'), '')
    # if all planned transitions are used
    cdf.controller().add_system_transition('pet_topic_switch', 'intermediate_topic_switch',
                                           '[!"It has been fun talking to you about animals. "]', score=0.0)

    cdf.add_system_transition('pet_intro', 'animals:start', '#SET($petv=True,$new_pet=True) #IF($original_pet=None)')

    add_transitions(cdf)

def add_transitions(cdf):

    cdf.add_system_transition('pet_topic_switch', 'house:start', '')

    cdf.add_system_transition('pet_topic_switch', 'worklife:start', '`You know, you seem like a pretty interesting person. `')
    cdf.add_system_transition('pet_topic_switch', 'worklife:start->worklife:remember_is_employed_open', '', score=9.0)
    cdf.add_system_transition('pet_topic_switch', 'worklife:start->worklife:like_job_answer', '', score=10.0)

    cdf.add_system_transition('pet_topic_switch', 'school_new:start', '`Hey by the way, `', score=2.0)
    cdf.add_system_transition('pet_topic_switch', 'sibling:start', '`You know, I can\'t put my finger on why, but you kind of seem like you have a sister.`')

    cdf.add_system_transition('pet_topic_switch', 'relationships:dating', '')
    cdf.add_system_transition('pet_topic_switch', 'relationships:dating->relationships:relationship_length', '', score=10.0)
    cdf.add_system_transition('pet_topic_switch', 'relationships:marriage', '')
    cdf.add_system_transition('pet_topic_switch', 'relationships:marriage->relationships:how_long_married', '', score=10.0)

    cdf.add_system_transition('pet_topic_switch', 'baby:start', '')
    cdf.add_system_transition('pet_topic_switch', 'baby:start->baby:asked_kids_age', '', score=10.0)

    cdf.add_system_transition('pet_topic_switch', 'hobby:start', '')
    cdf.add_system_transition('pet_topic_switch', 'hobby:today_flow', '')

    cdf.add_system_transition('pet_topic_switch', 'cv_final:start', '')

    cdf.add_system_transition('pet_topic_switch', 'movies_return:start', '', score=15.0)
    cdf.add_system_transition('pet_topic_switch', 'pets_return:start', '', score=15.0)
    cdf.add_system_transition('pet_topic_switch', 'baby:returning', '', score=15.0)
    cdf.add_system_transition('pet_topic_switch', 'relationships:returning', '', score=15.0)
    cdf.add_system_transition('pet_topic_switch', 'school_new:returning', '', score=15.0)
    cdf.add_system_transition('pet_topic_switch', 'worklife:returning', '', score=15.0)

    # PET -> MUSIC

    cdf.add_system_transition('pet_topic_switch', 'pet_to_music', '#GATE(musicv:None)')
    cdf.controller().update_state_settings('pet_to_music', system_multi_hop=True)
    cdf.add_system_transition('pet_to_music', 'ask_pet_music',
                              '"My friends always sing to their pets. Do you think animals like music in the same way people do?"')
    cdf.add_user_transition('ask_pet_music', 'yes_pet_music',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_pet_music', 'no_pet_music',
                            '[{#DISAGREE,[{dont,not},{really,likely}]}]')
    cdf.controller().set_error_successor('ask_pet_music', 'unknown_pet_music')
    cdf.add_system_transition('yes_pet_music', 'music_intro',
                              '"Yeah, it may be likely that a pleasant melody is soothing to every creature. "')
    cdf.add_system_transition('no_pet_music', 'music_intro',
                              '"Yeah, maybe music is something uniquely enjoyable to people. "')
    cdf.add_system_transition('unknown_pet_music', 'music_intro',
                              '"Ok. Well, I think a pleasant sound is enjoyable to every creature, but what is considered to be pleasant may vary among species. "')

    # PET -> SPORTS

    cdf.add_system_transition('pet_topic_switch', 'pet_to_sports', '#GATE(sportsv:None)')
    cdf.controller().update_state_settings('pet_to_sports', system_multi_hop=True)
    cdf.add_system_transition('pet_to_sports', 'ask_pet_sports',
                              '"I heard that some sporting events let pets attend. Many professional baseball games welcome dog owners and their dogs at Bark in the Park events during the regular season. Do you think this is a good idea?"')
    cdf.add_user_transition('ask_pet_sports', 'yes_pet_sports',
                            '[{#AGREE, probably, [#NOT(not,dont), likely]}]')
    cdf.add_user_transition('ask_pet_sports', 'no_pet_sports',
                            '[{#DISAGREE,[{dont,not},{really,likely,want,like}], distracting,distraction,messy,disruptive,disruption,annoying,loud,annoy,noisy}]')
    cdf.controller().set_error_successor('ask_pet_sports', 'unknown_pet_sports')
    cdf.add_system_transition('yes_pet_sports', 'sports_intro',
                              '"Me too. Some people may find it annoying, but I think it is good to socialize your dogs while doing something fun yourself. "')
    cdf.add_system_transition('no_pet_sports', 'sports_intro',
                              '"Yeah, I think a lot of people would agree with you on that. It is probably too disruptive and noisy for others who want to watch the games. "')
    cdf.add_system_transition('unknown_pet_sports', 'sports_intro',
                              '"Yeah, maybe. I think it is hard to say. Some people may find it annoying, but others would enjoy taking their dogs out. "')

    # PET -> VIRTUAL REALITY

    cdf.add_system_transition('pet_topic_switch', 'pet_to_vr', '#GATE(virtual_realityv:None)')
    cdf.controller().update_state_settings('pet_to_vr', system_multi_hop=True)
    cdf.add_system_transition('pet_to_vr', 'ask_pet_vr',
                              '"Once augmented reality becomes advanced, I can imagine that companies will come out with virtual pets. I think I would still prefer a real one. What about you?"')
    cdf.add_user_transition('ask_pet_vr', 'yes_pet_vr',
                            '[{#AGREE, [me,too], [#NOT(not),{real,living,alive}], [not,{virtual,electric,electronic,fake}]}]')
    cdf.add_user_transition('ask_pet_vr', 'no_pet_vr',
                            '[{#DISAGREE, [#NOT(not),{virtual,electric,electronic,fake}]}]')
    cdf.add_user_transition('ask_pet_vr', 'dislike_pet',
                            '[{hate,dislike,[{dont,not},{like,want,wish,love,need,care}]}, {pet,pets,animal,animals,cat,cats,dog,dogs}]')
    cdf.controller().set_error_successor('ask_pet_vr', 'unknown_pet_vr')
    cdf.add_system_transition('yes_pet_vr', 'virtual_reality_intro',
                              '"Yeah, that makes sense. So, "')
    cdf.add_system_transition('no_pet_vr', 'virtual_reality_intro',
                              '"A virtual one would be cool. So, "')
    cdf.add_system_transition('unknown_pet_vr', 'virtual_reality_intro', '"I see. So, "')
