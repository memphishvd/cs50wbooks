# About
Project 1
CS50 Web Programming with Python and JavaScript
A Book Review Website

# Descripton:
    The project objective was to make me more comfortable Python, FLASK and Databases via SQL. The main requirement was a book review website with login funcitonality, ability to add/view reviews, import and export API data. I did add a couple of things of my own just to show off such as the my reviews page, stats on the nav bar and some personalization features like the title and greeting on nav bar after login!



# Requirements:
    
    The instructions to complete CS50W Project 1 were to complete a few key requirements which can be found alongwith the config details on the below link:
    https://docs.cs50.net/web/2020/x/projects/0/project0.html

        a. Import/Db Creation - 
            1. Create necessary tables
                (i) Created 3 tables using dbcreation.py:
                    - CS50WUSERS - For storing user data
                    - CS50WREVIEWS - for storing reviews data
                    - CS50WBOOKS - For storing books data
            2. Import book data in to the database from books.csv
                (i) Imported data from books.csv in to CS50WBOOKS table using import.py:


        b. Registration, Login and Logout - 
            1. Users should be able to register for your website, providing (at minimum) a username and password.
                (i)   Users can both register and login on the same page (index.html)
                (ii)  Form validation is in place (browser default), empty fields cannot be submitted and email syntax is enforced.
            2. Users, once registered, should be able to log in to your website with their username and password.
                (i)   Users can logout by clicking on the logout link on the top left of the navigation bar, this will clear the session and redirect them to the index page with a confirmation message. If they are already logged out they will still be redirected to index.html and will get an updated message informing them they are already logged out.

        c. Book Search - 
            1. Users should be able to search for a book by isbn/title/author and results partially matching the query should be displayed too alongwith a no results message if there are no results.
                (i) DASHBOARD: After logging in users are taken to dashboard.html which has two main parts:
                    - Navigation Bar: Shows useful statistics such as User's total submitted reviews, total reviews in database, total books and total authors in daabase. It also shows a personalized greeting with the user's name as well as the last time they logged in. It shows a different message if they are logging in for the first time. At the end there is also the log out button.
                    - The other part of the dashboard page has the search form and the option for the user to search by ISBN, TITLE or AUTHOR using the pulldown menu.
                (ii) SEARCH RESULTS:
                    - A searched yielding no results will redirect the user to the dashboard page with an error message under the navigation bar advising no results were found against the search criteria, it will also display what search parameter was used i.e ISBN, TITLE or AUTHOR.
                    - A successful search will redirect user to the searchresults.html page with three pieces of information:
                        - A message displaying what the search criteria was
                        - Count of returned search results
                        - A list of the books returned as a result of the search with a clickable button for details on each book.

        d. Book Info Page - 
            1. On the book info page the user should be able to see the title, author, publication year, ISBN number and any reviews.
                (i) Clicking on the DETAILS button on each row of the results on the searchresults.html page will the user to bookinfo.html with the above mentioned details of the book. Each review row will show the review date, rating out of 5 along with stars and review comments.

            2. Users should be able to submit a review if they have not already done so before for that book. Review options should include a rating out of 5 as well as a text component.
                (i) bookinfo.html has the option for a review submission. If the the review is submitted successfully the user will be redirected to the bookinfo.html page with an updated list of the reviews including the one just submitted and success message confirming it, if the submission fails because the user has already submitted the review for this book before, they will be alerted with a message telling them the same and the previously submitted review will be highlighted in the review list below in amber colour. 

             3. Book Info page should show average rating and number of ratings the book has recieved at Goodreads.com if available.
                (i) bookinfo.html shows this detail

             
        e. API Access - 
            1. If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, the website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
                {
                    "title": "Memory",
                    "author": "Doug Lloyd",
                    "year": 2015,
                    "isbn": "1632168146",
                    "review_count": 28,
                    "average_score": 5.0
                }

                (i) A GET request to /api/<isbn> returns the required info in JSON format, if a record matching the ISBN does not exist it returns an error message and a 404 status code. If there are no reviews for the book in the database the average score is reset to 0. Please bear in mind this is the average score and number of reviews submitted on this website NOT Goodreads. The same JSON response can also be seen by clicking on the API Details button on the book info page.

        f. EXTRA FUNCTIONALITY:
            1. This was not part of the requirement but just as a personal touch I have added another section titled My Reviews, this will list all the reviews the current user has submitted for any books. A message will be displayed if the user has not submitted any reviews.




# Attribution:
    1. Source code from different bootstrap example templates has been utilized. Namely offcanvas, sign-in and cover among others. This has then been customized for usage where needed. (https://getbootstrap.com/docs/4.0/examples/)
    2. Some techniques referenced from research done on google.com, stackoverflow.com and w3schools.com
    3. Got the idea to add book cover thumbnail from this post, although it has not been added to this project at this time however it might be in the future so adding the attribution here anyway. 
    (https://www.reddit.com/r/cs50/comments/d38yau/cs50web_neat_trick_for_project_1_book_covers/?utm_source=share&utm_medium=web2x)
    (https://openlibrary.org/dev/docs/api/covers)
    4. API data courtesy www.goodreads.com
    5. Various images used from the following resources:
            https://www.pexels.com/@sound-on?filter=photos
            <a href='https://www.freepik.com/free-photos-vectors/background'>Background photo created by freepik - www.freepik.com</a>
        <a href='https://www.freepik.com/free-photos-vectors/school'>School photo created by freepik - www.freepik.com</a>
        <a href='https://www.freepik.com/free-photos-vectors/book'>Book photo created by freepik - www.freepik.com</a>
        <a href='https://www.freepik.com/free-photos-vectors/cover'>Cover photo created by freepik - www.freepik.com</a>
        Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
        Icons made by <a href="https://www.flaticon.com/free-icon/bookshelf_1470368?term=book%20shelf&page=1&position=80" title="Linector">Linector</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
        Icons made by <a href="https://www.flaticon.com/authors/prosymbols" title="Prosymbols">Prosymbols</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
        Image by <a href="https://pixabay.com/users/DavidRockDesign-2595351/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3107939">DavidRockDesign</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3107939">Pixabay</a>
        Image by <a href="https://pixabay.com/users/Schueler-Design-530319/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1404310">Alfons Schüler</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1404310">Pixabay</a>
        Photo by Alana Sousa from Pexels


# Youtube Link and Timestamps
https://youtu.be/wYj5e-SAGOM

1. Database Tables Creation: 00:10
2. Import Data From Books.csv: 00:18
3. Register For New Account: 00:26
4. Login: 00:45
5. Dashboard: 00:53
6. Logout: 1:13
7. Search Fields: 1:32
8. Multiple Search Results: 2:09
9. Book Info Page: 2:29
10. Review Submission: 2:50
11. Multiple Review Validation: 3:08
12. API Page: 3:28
13. EXTRA: 3:54


