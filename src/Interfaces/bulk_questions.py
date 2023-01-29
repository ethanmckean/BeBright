from Interfaces.question import Question
from typing import List
import json

if __name__ == "__main__":
    with open("Exam.txt", "r") as file:
        lines = file.readlines()
        questions: List[Question] = []

        line = 0
        while line < len(lines):
            questions.append(
                Question(
                    lines[line].strip(),
                    [lines[line + 3 + j].strip() for j in range(int(lines[line + 2]))],
                    lines[line + 1].strip(),
                )
            )

            line += 3 + int(lines[line + 2])

        for i in range(len(questions)):
            with open("../bin/out" + str(i).zfill(4) + ".json", "w") as f:
                json.dump(questions[i].get_dict(), f)
