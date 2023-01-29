from Interfaces.question import Question
from typing import List, Any
from google.cloud.sql.connector import Connector
import sqlalchemy


# initialize parameters
# spartahacks8:us-central1:be-bright-da
INSTANCE_CONNECTION_NAME = f"spartahacks8:us-central1:be-bright-da"  # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "swesik"
# DB_PASS = "robin"
DB_NAME = "bbdb"

# initialize Connector object
connector = Connector()

# function to return the database connection object
def get_connection() -> Any:
    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        # password=DB_PASS,
        db=DB_NAME,
    )


# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=get_connection,
)

# with pool.connect() as db_conn:
#     drop_query = sqlalchemy.text("DROP TABLE questions")
#     query = sqlalchemy.text(
#         "CREATE TABLE questions("
#         "user VARCHAR(50) NOT NULL, tag VARCHAR(50), question VARCHAR(1000) NOT NULL, "
#         "ans VARCHAR(10) NOT NULL, choices VARCHAR(10000) NOT NULL)"
#     )

#     db_conn.execute(drop_query)
#     db_conn.execute(query)
#     db_conn.commit()
# exit(0)


def add_to_database(user: str, q: Question, tag: str = None) -> None:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "INSERT INTO questions(user, tag, question, ans, choices) "
            "VALUES(:user, :tag, :question, :ans, :choices)",
        )

        query = query.bindparams(
            user=user,
            tag=tag,
            question=q.get_question(),
            ans=q.get_ans(),
            choices=q.get_choices(),
        )

        db_conn.execute(query)
        db_conn.commit()


def get_database_questions(user: str = None, tag: str = None) -> List[Question]:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "SELECT question, choices, ans FROM questions WHERE "
            "(user=:user OR :user IS NULL) AND (tag=:tag OR :tag IS NULL)"
        )

        query = query.bindparams(user=user, tag=tag)

        return [
            Question(i[0], i[1].split("\n"), i[2])
            for i in db_conn.execute(query).fetchall()
        ]


if __name__ == "__main__":
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "DELETE FROM questions WHERE 1",
        )

        db_conn.execute(query)
        db_conn.commit()

    with open("src/Exam.txt", "r") as file:
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
            add_to_database("me", q)

for i in get_database_questions():
    print(str(i))
    print(i.answer(input()))
    print()
