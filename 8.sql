SELECT name from People JOIN
stars on people.id=stars.person_id JOIN
movies on stars.movie_id = movies.id
WHERE title = "Toy Story"