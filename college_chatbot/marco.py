# state for each of the residence hall?
from emora_stdm import DialogueFlow, Macro

hall_names = {"alabama", "complex", "eagle", 
              "hamilton holmes", "raoul", "turman", "dobbs", "haris"}

rates = {
  "alabama" : 100
}

housing_options_phrase = {"options", "dorms", "residence hall"}

class CATCH_HALL_OPTIONS(Macro):
  def __init__(self):
    pass
  
  def run(self, ngrams, vars, args):
    pass

class CATCH_HALL(Macro):
  def __init__(self):
      """hall name list"""
      self.halls = hall_names

  def run(self, ngrams, vars, args):
      """Performs operation"""
      print("**test catch hall**")
      print(ngrams)
      # print(self.halls)
      print(ngrams & self.halls)
      for token in ngrams:
        for hall_name in hall_names:
          if token in hall_name:
            return hall_name
          
      return ngrams & self.halls
    
    
class GENERATE_HALL_RESPONSE(Macro):
  def __init__(self):
      """Inits CATCH with list"""
      self.halls = hall_names

  def run(self, ngrams, vars, args):
      """Performs operation"""
      res = "\n"
      rate = rates[vars[args[0]]]
      return rate
    

class AMENITIES(Macro):
  # generate amenities response to each specific hall
    def __init__(self):
      """init knowledge graph here"""
      pass
    
    def run(self, ngrams, vars, args):
      """use arguments to query for data"""
      pass