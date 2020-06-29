import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Setting up a main function which will encapsulate the table creation queries
def main():
        db.execute("CREATE TABLE IF NOT EXISTS cs50wusers (UserID SERIAL PRIMARY KEY, Name VARCHAR NOT NULL, Email VARCHAR NOT NULL, Password VARCHAR NOT NULL, last_logged_in TIMESTAMP )")
        db.execute("CREATE TABLE IF NOT EXISTS cs50wbooks (BookID SERIAL PRIMARY KEY, ISBN VARCHAR NOT NULL, Title VARCHAR NOT NULL, Author VARCHAR NOT NULL, Year INTEGER NOT NULL )")
        db.commit()
# Needed to split this in to two db.commits because cs50reviews is dependant on the creation of the other two tables first
        db.execute("CREATE TABLE IF NOT EXISTS cs50wreviews (ReviewID SERIAL PRIMARY KEY, DateofReview DATE NOT NULL, BookID INTEGER NOT NULL REFERENCES cs50wbooks, UserID INTEGER NOT NULL REFERENCES cs50wusers, review_comments VARCHAR, Rating INTEGER NOT NULL )")
        db.commit()

        print(f"If a table with the specified name didn't exist it has now been created otherwise no table has been created, please change the table name and try again")



if __name__ == "__main__":
   main()