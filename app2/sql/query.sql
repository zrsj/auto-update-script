CREATE TABLE retvals2;
SELECT * INTO TABLE retvals2
FROM categories
WHERE categories.category_id%2 = 0;
