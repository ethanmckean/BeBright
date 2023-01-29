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


def login(username: str, password: str) -> None:
    with pool.connect() as db_conn:
        query = sqlalchemy.text(
            "SELECT password FROM user_data WHERE username = :username"
        )

        query = query.bindparams(
            username=username,
        )

        login_data = db_conn.execute(query).fetchone()
        print(login_data)
        if login_data is None or len(login_data) == 0:
            query = sqlalchemy.text(
                "INSERT INTO user_data(username, password) "
                "VALUES(:username, :password)"
            )
            query = query.bindparams(
                username=username,
                password=password[len(password) % 7 :] + password[: len(password) % 7],
            )
            db_conn.execute(query)
        else:
            return (
                login_data[0]
                == password[len(password) % 7 :] + password[: len(password) % 7]
            )

        db_conn.commit()
        return True


print(login(input(), input()))
