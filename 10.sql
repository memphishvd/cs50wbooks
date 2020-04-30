SELECT DISTINCT name from people JOIN
directors ON people.id = directors.person_id JOIN
ratings ON directors.movie_id = ratings.movie_id
WHERE rating >= 9.0