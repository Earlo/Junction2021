import os

from app.main import app
import psycopg2

try:
  DATABASE_URL = os.environ['DATABASE_URL']
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except:
    print("I am unable to connect to the database") 

cur = conn.cursor()
try:
  cur.execute("CREATE TABLE chatUser (username text PRIMARY KEY, password text);")
  
  cur.execute("CREATE TABLE comments (id serial PRIMARY KEY, content text, poster text);")
except:
  print("I can't drop our test database!")
conn.commit()

try:  
  cur.execute("CREATE TABLE comments (id serial PRIMARY KEY, content text, poster text);")
except:
  print("I can't drop our test database!")
conn.commit()

cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cur.fetchall():
    print(table)

conn.close()
cur.close()

if __name__ == "__main__":
  app.run()

