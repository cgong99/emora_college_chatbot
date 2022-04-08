from manager_v1 import df

debug = False

df.precache_transitions()
sequence = ['what housing options do I have?', "Alabama Hall"]

for utter in sequence:
  response = df.system_turn(debugging=debug)
  print("System: %s (%s)"%(response,df.state()))
  
  df.user_turn(utter, debugging=debug)
  print("User: %s (%s)"%(utter,df.state()))