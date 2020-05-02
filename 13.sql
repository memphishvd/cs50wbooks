SELECT DISTINCT name FROM people
WHERE name IS NOT "Kevin Bacon"
AND id IN
                (SELECT stars.person_id FROM stars WHERE stars.movie_id IN
					(SELECT stars.movie_id FROM stars where stars.person_id IN
						(Select people.id FROM people where name = "Kevin Bacon" and birth = 1958)
					)
				)