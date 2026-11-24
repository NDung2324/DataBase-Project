INSERT INTO movies (content_id)
SELECT content_id
FROM content
WHERE content_type = 'MOVIE';
