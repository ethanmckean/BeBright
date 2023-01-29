from google.cloud.sql.connector import Connector
import sqlalchemy


# initialize parameters
# spartahacks8:us-central1:be-bright-da
INSTANCE_CONNECTION_NAME = f"spartahacks8:us-central1:be-bright-da" # i.e demo-project:us-central1:demo-instance
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "swesik"
# DB_PASS = "robin"
DB_NAME = "bbdb"

# initialize Connector object
connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        # password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  # create ratings table in our movies database
  db_conn.execute(
      sqlalchemy.text("CREATE TABLE IF NOT EXISTS ratings ;")
    #   "( id SERIAL NOT NULL, title VARCHAR(255) NOT NULL, "
    #   "genre VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
    #   "PRIMARY KEY (id));")
  )
  # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ratings (title, genre, rating) VALUES (:title, :genre, :rating)",
  )

  # insert entries into table
  db_conn.execute(insert_stmt, title="Batman Begins", genre="Action", rating=8.5)
  db_conn.execute(insert_stmt, title="Star Wars: Return of the Jedi", genre="Action", rating=9.1)
  db_conn.execute(insert_stmt, title="The Breakfast Club", genre="Drama", rating=8.3)

  # query and fetch ratings table
  results = db_conn.execute("SELECT * FROM ratings").fetchall()

  # show results
  for row in results:
    print(row)

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
