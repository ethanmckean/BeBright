from Interfaces.question import Question
from typing import List, Any
from google.cloud.sql.connector import Connector
from datetime import datetime
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


def add_to_database(q: Question, group: str, time: datetime) -> None:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "INSERT INTO questions(question, ans, choices, group, post_time) "
            "VALUES(:question, :ans, :choices, :group, :post_time)",
        )

        query = query.bindparams(
            question=q.get_question(),
            ans=q.get_ans(),
            choices=q.get_choices(),
            group=group,
            post_time=time,
        )

        db_conn.execute(query)
        db_conn.commit()


def get_database_questions(
    group: str, time: datetime = datetime.now()
) -> List[Question]:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "SELECT question, choices, ans, group, post_time FROM questions WHERE "
            "group = :group AND post_time < :time"
        )

        query = query.bindparams(group=group, time=time)

        return [
            (Question(i[0], i[1].split("\n"), i[2]), i[3], [4])
            for i in db_conn.execute(query).fetchall()
        ]


def remove_database_questions(group: str, time: datetime = datetime.now()) -> None:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "DELETE FROM FROM questions WHERE " "group = :group AND post_time < :time"
        )

        query = query.bindparams(group=group, time=time)

        db_conn.execute(query)
