SELECT title,rating from movies
JOIN ratings on movies.id=ratings.movie_id
WHERE year = 2010 AND rating IS NOT NULL 
ORDER BY rating DESC , title ASC;