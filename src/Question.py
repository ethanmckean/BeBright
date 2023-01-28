from typing import List

# import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword"
# )

chars = "abcdefghijklmnopqrstuvwxyz"


class Question:
    def __init__(self, qs: str, choices: List[str], key: str) -> None:
        self.qs = qs
        self.choices = choices
        self.key = key

        if len(choices) > 26:
            raise Exception(
                "Let me BeReal with you; the english language does not support this feature."
            )

    def answer(self, sol: str) -> bool:
        return sol == self.key

    def iterate_choice(self) -> str:
        for choice in self.choices:
            yield choice

    def get_choices(self) -> str:
        return "\n".join(chars[i] + ") " + text for i, text in enumerate(self.choices))

    def get_question(self) -> str:
        return self.qs

    def get_key(self) -> str:
        return self.key

    def __str__(self) -> str:
        return self.get_question() + "\n" + self.get_choices()


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

if __name__ == "__main__":
    with open("Exam.txt", "r") as file:
        lines = file.readlines()
        question: List[Question] = []

        line = 0
        while line < len(lines):
            question.append(
                Question(
                    lines[line].strip(),
                    [lines[line + 3 + j].strip() for j in range(int(lines[line + 2]))],
                    lines[line + 1].strip(),
                )
            )

            line += 3 + int(lines[line + 2])

        for q in question:
            print(q)
            print(q.answer(input()))
