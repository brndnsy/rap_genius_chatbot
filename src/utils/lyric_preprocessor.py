from nltk import re

def get_blank_spaces_pattern():
    return re.compile(r'\s{2,}|\t')

class LyricPreprocessor:

    def __init__(self, text: str):
        self.text = text

    def fully_preprocess(self):
        return self \
            .remove_blank_spaces()\
            .remove_excess_quotes()
        # .remove_escape_char()\
        

    def remove_blank_spaces(self):
        self.text = re.sub(pattern=get_blank_spaces_pattern(), repl=' ', string=self.text)
        return self

    def remove_escape_char(self):
        self.text = self.text.replace("\\'", "") 
        return self
    
    def remove_excess_quotes(self):
        self.text = self.text.replace('""', '"') 
        return self