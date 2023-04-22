with q as
(
	SELECT a.rating,
				 u.id,
			   u.username,
			   case 
		       when row_number() over(partition by u.id, p.id)  = 1 
				     then p.rating * 3
				   else null
				 end as post_rating,
			   CASE when p.id = c.post_id then c.rating else 0 END as post_comments_rating
		FROM news_post p 
		     INNER JOIN news_author a on p.author_id =  a.id 
				 INNER JOIN auth_user u on u.id = a.user_id  
				 INNER JOIN news_comment c on p.id = c.post_id
)
SELECT username, rating as python_calculated_rating,
	     SUM(post_rating) + SUM(post_comments_rating) + 
	       (SELECT SUM(rating) FROM news_comment c where c.user_id = q.id) as SQL_calculated_rating
	FROM q
	GROUP BY id, username, rating