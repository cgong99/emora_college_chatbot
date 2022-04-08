from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random




class BREED(Macro):
    """Generate breed name from database.

    Attributes:
        path: Path of database.
        db: Database.
    """

    def __init__(self, path):
        """Inits BREED with path"""
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        """Performs operation"""
        # lemmatizer = WordNetLemmatizer()
        # new_ngrams = set()
        # # print(ngrams)
        # for item in ngrams:
        #     # print(item)
        #     new_item = lemmatizer.lemmatize(item)
        #     # item = lemmatizer.lemmatize(item)
        #     new_ngrams.add(new_item)
            # print(new_item)
        # print("new ngrams",new)
        # print(set(self.db.keys()))
        # print("catch",new_ngrams & set(self.db.keys()))
        # return new_ngrams & set(self.db.keys())
        print("**** BREED ****")
        print("N grams: ", ngrams)
        print(type(ngrams))
        print(type(self.db.keys()))
        print("vars: ", vars)
        print("args: ", args)
        print("ngrams & self.db.keys()")
        return ngrams & self.db.keys()


dog_breed = 'dog_breed_database.json'
# BREED(dog_breed)
#
# BREED.run()
with open(dog_breed, 'r') as f:
    db = json.load(f)

print(db)