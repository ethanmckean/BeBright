from typing import List, Dict
import json

chars = "abcdefghijklmnopqrstuvwxyz"


class Question:
    def __init__(self, qs: str, choices: List[str], ans: str) -> None:
        self.qs = qs
        self.choices = choices
        self.ans = ans

        if len(choices) > 26:
            raise Exception(
                "Let me BeReal with you; the english language does not support this feature."
            )

    def answer(self, sol: str) -> bool:
        return sol == self.ans

    def iterate_choice(self) -> str:
        for choice in self.choices:
            yield choice

    def str_choices(self) -> str:
        return "\n".join(chars[i] + ") " + text for i, text in enumerate(self.choices))

    def get_choices(self) -> str:
        return "\n".join(self.choices)

    def get_question(self) -> str:
        return self.qs

    def get_ans(self) -> str:
        return self.ans

    def __str__(self) -> str:
        return self.get_question() + "\n" + self.str_choices()

    def get_dict(self) -> Dict[str, str]:
        return {"qs": self.qs, "choices": self.choices, "ans": self.ans}


def get_json_data(data: str) -> Question:
    with open(data) as json_file:
        json_data = json.load(json_file)

        return (
            Question(json_data["qs"], json_data["choices"], json_data["ans"]),
            json_data["group"],
            json_data["post_date"],
        )


def get_question(data: str) -> Question:
    return get_json_data(data)[0]
