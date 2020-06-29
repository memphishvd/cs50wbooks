import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

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


def main():
    f = open("books.csv")
    reader = csv.reader(f)
#ignore header in books1.csv
    next(reader, None)
#setting a counter just to keep track of number of books added
    count=0
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO cs50wbooks (ISBN, TITLE, AUTHOR, YEAR) VALUES (:isbn, :title, :author, :year)",
                    {"isbn":isbn, "title":title, "author":author, "year":year})
        db.commit()
#incrementing counter
        count+=1
#printing counter output
        print(str(count) + "books added")


if __name__ == "__main__":
   main()