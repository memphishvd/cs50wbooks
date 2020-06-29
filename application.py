import os
import requests
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date, time, datetime
from dateutil import tz
import json


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

# Default Root

@app.route("/")
def index():

    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():
# Redirect to registration page of trying to access /register directly
    if request.method == "GET":
        return render_template("index.html", msgmarker="fail", alert="So to get in here you can either touch your nose with your tongue OR register for an account below, your choice!")
 # Populate variables values with corresponding form data
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
# Query DB to check if a user with given email already exists  otherwise insert new user data in table and redirect to INDEX page with a success/failure message
        if db.execute("SELECT email FROM cs50wusers where email=:email", {"email":email}).rowcount!=0:
            return render_template("index.html", msgmarker="fail", alert="Woahhh hold on smarty pants! There is already an account associated with this email")
        db.execute("INSERT INTO cs50wusers (name, email, password) VALUES (:name, :email, :password)",
                    {"name":name, "email":email, "password":password})
        db.commit()
        return render_template("index.html", msgmarker="success", alert="Howdy Partner! Y`all can login now!")


# Login Function
@app.route("/login", methods=["POST"])
def login():

# Get Form Data
    email = request.form.get("email")
    password = request.form.get("password")
    logindate = datetime.now(tz=tz.tzlocal())

# Match Login Credentials With DB and Redirect to DASHBOARD for success and INDEX for failure with respective messages accordingly.   
    dbdata = db.execute("select Email, name, userid, last_logged_in from cs50wusers WHERE email=:email AND password=:password", {"email":email, "password":password}).fetchone()
    if dbdata:
        db.execute("UPDATE cs50wusers SET last_logged_in=:logindate where userid=:userid", {"logindate":logindate, "userid":dbdata.userid})
        db.commit()
# Getting additional data for Navigation Bar Stats
        userreviews=db.execute("SELECT COUNT(reviewid) FROM cs50wreviews WHERE userid=:userid", {"userid":dbdata.userid}).fetchone()
        totalreviews=db.execute("SELECT COUNT(reviewid) FROM cs50wreviews").fetchone()
        totalbooks=db.execute("SELECT COUNT(bookid) FROM cs50wbooks").fetchone()
        totalauthors=db.execute("SELECT COUNT(DISTINCT author) FROM cs50wbooks").fetchone()
        
# Storing data in session to access across different functions later on
        session['Active']=True
        session['email'] = dbdata.email
        session['name'] = dbdata.name
        session['userid'] = dbdata.userid
        session['userreviews'] = userreviews
        session['totalreviews'] = totalreviews
        session['totalbooks'] = totalbooks
        session['totalauthors'] = totalauthors

# If logging in for the first time set login/time as current otherwise get the last logged in date/time from database and store in session
        if dbdata.last_logged_in==None:
            session["lastloggedin"] = logindate
        session["lastloggedin"] = dbdata.last_logged_in

# Redirect to dashboard on successfully logging in         
        return render_template("dashboard.html")

# Redirect to index with a failure message if login credentials are unverified
    return render_template("index.html", msgmarker="fail", alert="Incorrect Login Details")

@app.route("/logout")
def logout():
    if 'Active' in session:
        session.clear()
        return render_template("index.html", msgmarker="fail", alert="Out Of Sight, Out Of Mind? Nah We Still Love Ya, You`re Just Logged Out!")
    else:
        return render_template("index.html",msgmarker="fail", alert="You`re Already Logged Out <insert_helpless_emoji_here_:P>")


# Restricting access to dashboard unless logged in
@app.route("/dashboard")
def dashboard():
    if 'Active' in session:
        return render_template("dashboard.html")
    else:
        return render_template("index.html", msgmarker="fail", alert="So to get in here you can either touch your nose with your tongue OR login below, your choice!")

# Book Search Function
@app.route("/search", methods=["POST"])
def search():
 
# Check what search parameter (ISBN/TITLE/AUTHOR) was used and set it as criteriaparameter
    criteriaparameter = request.form.get("criteria")
# Get the value of the user input for criteria
    criteriavalue = request.form.get("criteriainput")
# Set variable to use for a LIKE query
    criteriavaluelowercase = "%" + criteriavalue + "%"
# Convert criteria input to lower case
    criteriavaluelowercase = criteriavaluelowercase.lower()
# Check if user did not enter any criteria and redirect accordingly    
    if criteriavalue == "":
        return render_template("dashboard.html", alert="You Did Not Enter A Search Criteria")
# Check the criteria parameter and run the relevant search query. LOWER(x) has been used to change case for author and title queries to match results.
    if criteriaparameter == "isbn":
        
        dbdata=db.execute("SELECT * FROM cs50wbooks where isbn LIKE :isbn", {"isbn":criteriavaluelowercase}).fetchall()
        resultcount = len(dbdata)
        if dbdata:
            return render_template("searchresults.html", alert=dbdata, criteriavalue=criteriavalue, resultcount=resultcount)
        return render_template("dashboard.html", alert="No Result Found For The Following ISBN:", criteriavalue=criteriavalue,)

    elif criteriaparameter == "title":
        
        dbdata=db.execute("SELECT * FROM cs50wbooks where LOWER(title) LIKE :title", {"title":criteriavaluelowercase}).fetchall()
        resultcount = len(dbdata)
        if dbdata:
            return render_template("searchresults.html", alert=dbdata, criteriavalue=criteriavalue, resultcount=resultcount)
        return render_template("dashboard.html", alert="No Result Found For The Following Title:", criteriavalue=criteriavalue)

    elif criteriaparameter == "author":

        dbdata=db.execute("SELECT * FROM cs50wbooks where LOWER(author) LIKE :author", {"author":criteriavaluelowercase}).fetchall()
        resultcount = len(dbdata)
        if dbdata:
            return render_template("searchresults.html", alert=dbdata, criteriavalue=criteriavalue, resultcount=resultcount)
        return render_template("dashboard.html", alert="No Result Found For The Following Author:", criteriavalue=criteriavalue)


# Function to get info for the book info page   
@app.route("/bookinfo")
def bookdetail():
    if 'Active' in session:
#Getting passed data for bookID and isbn from search results page
        bookID=request.args.get('bookID', None)
        isbn=request.args.get('isbn', None)
#Setting session lists for onward use as we will store data in these later
        session['dbdatareviews'] = []
        session['dbdatabooks'] = []

#Retrieving Goodreads Data.
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "srAQWrY6pcQQbQ3U9MqdA", "isbns": isbn})
        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")
        greadsdata = res.json() 

#Saving required Goodreads data in session for later retrieval
        session['greadsratings'] = greadsdata["books"][0]["work_ratings_count"]
        session['greadsavgratings'] = greadsdata["books"][0]["average_rating"]

#Getting book data as well as reviews for the relevant book from the two tables
        dbdatabooks = db.execute("SELECT * FROM cs50wbooks WHERE bookid=:bookID", {"bookID":bookID}).fetchall()
        dbdatareviews = db.execute("SELECT * FROM cs50wreviews WHERE bookid=:bookID", {"bookID":bookID}).fetchall()

#Storing the retrieved database reviews data in session
        for i in dbdatareviews:
            session['dbdatareviews'].append(i)

#Storing the number of reviews in session
        session['reviewcount'] = len(dbdatareviews)

#Storing the retrieved database book data in session        
        if dbdatabooks:        
            session["dbdatabooks"] = dbdatabooks
 
 #Redirect to bookinfo page with all the retrieved data OR to dashboard with failure message if no data is retrieved (not really a possibility but still there for good measure)
            return render_template("bookinfo.html", dbdatabooks=session["dbdatabooks"], dbdatareviews=session["dbdatareviews"], bookID=bookID)
        return render_template("dashboard.html", alert="No Data Available For This Book", bookID=bookID)
    else:
        return render_template("index", alert="Please Log In First")

#Function to add a review
@app.route("/addreview" , methods=["POST"])
def addreview():
    if 'Active' in session:
#Getting review form data. Setting the review submission date as current. Converting rating to an integer for storage in db.      
        userID = session["userid"]
        dates = date.today()
        bookID = request.form.get("bookID")
        rating = request.form.get("rating")
        rating = int(rating)
#Putting a placeholder value if no comments were submitted with the review, looks better than an empty field when the review is shown in search results :)
        reviewcomments = request.form.get("reviewcomments")
        if reviewcomments == "":
            reviewcomments = "No Comments Added For This Review"
#Check if this user has previously submitted a review for this book, if yes redirect back to book info page with failure message.
        dbdata=db.execute("SELECT * from cs50wreviews WHERE bookID=:bookID AND userID=:userID", {"bookID":bookID, "userID":userID}).fetchone()
#If user has submitted a review previously, store the data related to the previous review to be used in the failure message and to highlight the previously submitted review on the bookinfo page.
        if dbdata:
            session['dateofreview'] = dbdata.dateofreview
            session['rating'] = dbdata.rating
            session['review_comments'] = dbdata.review_comments
#To be used to highlight the previously submitted review
            reviewvalidationid = dbdata.reviewid
            return render_template("bookinfo.html", alert=dbdata,bookID=bookID, msgmarker="fail",reviewvalidationid=reviewvalidationid, message="You Have Already Submitted A Review For This Book, It Is Now Highlighted In The Review Section Below")
#If the user has not previously reviewed this book then add the current review data to the database.
        dbdata=db.execute("INSERT into cs50wreviews (dateofreview, bookid, userid, review_comments, rating) VALUES (:dateofreview, :bookID, :userID, :reviewcomments, :rating)",{"dateofreview":dates, "bookID":bookID, "userID":userID, "reviewcomments":reviewcomments, "rating":rating})
        db.commit()
#Get updated review count for the user for the nav bar stats.
        userid = session['userid']
        userreviews=db.execute("SELECT COUNT(reviewid) FROM cs50wreviews WHERE userid=:userid", {"userid":userid}).fetchone()
        session['userreviews'] = userreviews
#Get updated review data for the book so the newly added review can be shown in the list of reviews on the bookinfo page when we redirect the user back to it.
        dbdatareviews = db.execute("SELECT * FROM cs50wreviews WHERE bookid=:bookID", {"bookID":bookID}).fetchall()

        session['dbdatareviews']=[]
        for i in dbdatareviews:
            session['dbdatareviews'].append(i)
        session['reviewcount'] = len(dbdatareviews)
        return render_template("bookinfo.html",bookID=bookID, msgmarker="success", message="Pleasure to add your two cents to the review database!")
            
    else:
        return render_template("index.html", alert="Please Log In First")


    

#Function to export our data if there is an API request to our website.
@app.route("/api/<isbn>")
def myapi(isbn):
#Convert the passed isbn value to a string (remember ISBN can be a combination of numbers and letters)
    isbn=str(isbn)
    dbdatabooks = db.execute("SELECT * FROM cs50wbooks WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
#Return an error message as well as a 404 status code if the isbn does not match a book in our database
    if dbdatabooks is None:
        return jsonify({"error": "Invalid ISBN"}), 404
#Otherwise get the required data
    bookid=dbdatabooks.bookid
    dbdatareviews = db.execute("SELECT COUNT(reviewid) FROM cs50wreviews WHERE bookid=:bookid", {"bookid":bookid}).fetchone()[0]
    dbdatarating = db.execute("SELECT AVG(rating) FROM cs50wreviews WHERE bookid=:bookid", {"bookid":bookid}).fetchone()[0]
    if dbdatarating:
#Very important to do this to get the right average value due to python's handling of decimals. Also important to plug in a 0 value if there are no reviews for the book
        avgrating = round(float(dbdatarating),2)
    else:
        avgrating="0"

#Return the required data in json format   
    return jsonify({

            "title": dbdatabooks.title,
            "author": dbdatabooks.author,
            "year": dbdatabooks.year,
            "isbn": dbdatabooks.isbn,
            "review_count": dbdatareviews,
            "average_score": avgrating

        })

#Added functionality to list all the user's reviews (NOT part of the project requirements. Fairly straightforward so not commenting below)
@app.route("/myreviews" , methods=["GET"])
def myreviews():
    if 'Active' in session:
        userID = session["userid"]

        dbdata=db.execute("SELECT * from cs50wreviews WHERE userID=:userID", {"userID":userID}).fetchall()
        if dbdata:
            session['myreviews']=[]
            for i in dbdata:
                session['myreviews'].append(i)
            return render_template("myreviews.html", alert="these are all your reviews, well done!")
        else:
            return render_template("myreviews.html", alert="Here's a fun fact: definition of LAZY by Merriam-Webster: (Disinclined to activity or exertion : not energetic or vigorous).. oh and you have not posted ANY reviews :) ")
         
    else:
        return render_template("index.html", msgmarker="fail" , alert="So to get in here you can either touch your nose with your tongue OR login below, your choice!")
