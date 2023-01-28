from typing import List

chars = 'abcdefghijklmnopqrstuvwxyz'

class Question: 
    def __init__(self, qs: str, choices: List[str], key: str):
        self.qs = qs
        self.choices = choices
        self.key = key
        
        if len(choices) > 26:
            raise Exception("Let me BeReal with you; the english language does not support this feature.")
        
    def answer(self, sol: str):
        return sol == self.key
    
    def iterate_choice(self):
        for choice in self.choices:
            yield choice
            
    def get_choices(self):
        return '\n'.join(chars[i] + ') ' + text for i, text in enumerate(self.choices))
        
    def get_question(self):
        return self.qs
    
    def __str__(self):
        return self.get_question() + '\n' + self.get_choices()
    