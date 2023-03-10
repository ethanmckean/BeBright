from Interfaces.question import Question
from typing import List, Tuple, Any
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


def add_to_database(q: Question, cluster: str, time: datetime) -> None:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "INSERT INTO questions(question, ans, choices, cluster, post_time) "
            "VALUES(:question, :ans, :choices, :cluster, :post_time)",
        )

        query = query.bindparams(
            question=q.get_question(),
            ans=q.get_ans(),
            choices=q.get_choices(),
            cluster=cluster,
            post_time=time,
        )

        db_conn.execute(query)
        db_conn.commit()


def get_database_questions(
    cluster: str, time: datetime = datetime.now()
) -> List[Tuple[Question, str, datetime]]:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "SELECT question, choices, ans, cluster, post_time FROM questions WHERE "
            "cluster = :cluster AND post_time < :time"
        )

        query = query.bindparams(cluster=cluster, time=time)

        return [
            (Question(i[0], i[1].split("\n"), i[2]), i[3], [4])
            for i in db_conn.execute(query).fetchall()
        ]


def remove_database_questions(
    cluster: str, question: str = None, time: datetime = datetime.now()
) -> None:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "DELETE FROM questions WHERE cluster = :cluster AND post_time < :time "
            "AND (question = :question OR :question IS NULL)"
        )

        query = query.bindparams(cluster=cluster, question=question, time=time)

        db_conn.execute(query)
        db_conn.commit()
