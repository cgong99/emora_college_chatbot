###################################
# Import your DialogueFlow object
###################################
from pets import df

###################################
# Add an ending loop if
# you do not already have one
###################################
df.add_state('unit_test_end', 'unit_test_end')
df.add_system_transition('transition_out','unit_test_end','" END"')
df.add_system_transition('unit_test_end','unit_test_end','" END"')

if __name__ == '__main__':

    # debug = True
    debug = False
    df.precache_transitions()
    # Case 1:
    # ASK_PETS-ASK_PETS_Y-ASK_PETS-FIRST_PET_DOG_BREED-FIRST_PET_DOG_NAME
    sequence = ["test","yes","a husky","max"]
    # ASK_PETS-ASK_PETS_N
    sequence = ["test", "no", ]
    # ASK_PETS-FIRST_PET_DOG
    sequence = ["test", "i have a dog", ]
    # ASK_PETS-FIRST_PET_CAT
    sequence = ["test", "i have a cat", ]
    # ASK_PETS-FIRST_PET_OTHER
    sequence = ["test", "i have other animal", ]
    # ASK_PETS-FIRST_PET_OTHER_BREED
    sequence = ["test", "i have bird", ]
    # ASK_PETS-FIRST_PET_DOG_BREED
    sequence = ["test", "i have husky", ]
    # ASK_PETS-FIRST_PET_CAT_BREED
    sequence = ["test", "i have toyger", ]
    # ASK_PETS-FAVORITE_PET_DOG_DONTKNOW
    sequence = ["test", "i dont know", ]
    # ASK_PETS-NO_PETS_Y
    sequence = ["test", "i have kjkjb", ]



    # sequence = ["dog", "yes","husky","max", "fit", "no", "no", "yes", "yes", "no", "no", "yes", "father"]
    # sequence = ["test", "yes", "husky"]
    # sequence = ["dog", "yes", "husky", "max", "fit", "no", "no", "yes", "yes", "no", "no", "yes", "what"]
    # sequence = ["dog", "yes", "husky", "max", "fit", "no", "no", "yes", "yes", "no", "no", "max", "no", "what"]

    # don't have pets, don't want to have
    # sequence = ["dog", "no", "yes, a husky", "no", "no", "yes", "no", "joke"]

    # don't have pets, don't want to have
    # sequence = ["dog", "no", "no", "mess"]

    # offense
    # sequence = ["dog", "yes","husky","nigger"]

    # test from transition component
    # sequence = ["test", "yes","husky","nigger"]

    sequence = ["test", "yes", "a husky", "max"]

    turn = 0
    for utter in sequence:
        print("New utter: ", utter, "\n\n")
        df.user_turn(utter, debugging=debug)
        print("U: %s (%s)"%(utter,df.state()))

        response = df.system_turn(debugging=debug)
        print("E: %s (%s)"%(response,df.state()))

        turn += 1
