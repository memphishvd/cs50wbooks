SELECT DISTINCT name FROM people
WHERE name IS NOT "Kevin Bacon"
AND id IN
                (SELECT stars.person_id FROM stars WHERE stars.movie_id IN
					(SELECT stars.movie_id FROM stars WHERE stars.person_id IN
						(SELECT people.id FROM people WHERE name = "Kevin Bacon" AND birth = 1958)
					)
				)