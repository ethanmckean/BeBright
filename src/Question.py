from typing import List
# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword"
# )

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

    def get_key(self):
        return self.key
    
    def __str__(self):
        return self.get_question() + '\n' + self.get_choices()

# def add_to_database(q: Question):
#     with mydb.cursor() as cursor:
#         query = "INSERT INTO table(name, data, ans) VALUES(%s, %s, %s)"
#         params = {"name": q.get_question(), "data": q.get_choices(), "ans": q.get_key()}
#         cursor.execute(query, params)

# def parse_database():
#     question: List[Question] = []
#     with mydb.cursor() as cursor:
#         query = "SELECT * FROM table(name, data, ans)"
#         for i in cursor.execute(query).fetch_all():
#             question.append(Question(i[0], [s[3:] for s in i[1].split("\n")], i[2]))
