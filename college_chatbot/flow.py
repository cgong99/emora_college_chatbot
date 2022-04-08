
class topic_classifier():
    def __init__(self):
        self.model  # can load classifier here
        pass
    def predict(self, sentence):
        # type = self.model.predict(sentence)
        # preprocess sentence
        type = self.model.predict(sentence)
        return type


