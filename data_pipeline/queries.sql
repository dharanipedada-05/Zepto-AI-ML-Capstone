-- Query 1 - SELECT and WHERE
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4;

-- Query 2 - ORDER BY
SELECT title, price_gbp, rating
FROM books
ORDER BY price_gbp DESC;

-- Query 3 - LIMIT
SELECT title, price_gbp, rating
FROM books
ORDER BY price_gbp DESC
LIMIT 10;

-- Query 4 - DISTINCT
SELECT DISTINCT rating
FROM books
ORDER BY rating;

-- Query 5 - BETWEEN
SELECT title, price_gbp, price_inr
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp;

-- Query 6 - JOIN
SELECT
    b.title,
    c.category_name,
    b.price_gbp,
    b.rating,
    b.in_stock
FROM books AS b
JOIN categories AS c
    ON b.category_id = c.category_id
ORDER BY b.rating DESC, b.price_gbp DESC
LIMIT 10;

