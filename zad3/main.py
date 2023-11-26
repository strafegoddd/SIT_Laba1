import pandas as pd
import sqlite3


con = sqlite3.connect("library.sqlite")

cursor = con.cursor()

df = pd.read_sql(
    """WITH Поп_Изд AS (
    SELECT
        p.publisher_id,
        p.publisher_name,
        COUNT(br.book_id) AS borrow_count
    FROM
        publisher p
    JOIN
        book b ON p.publisher_id = b.publisher_id
    JOIN
        book_reader br ON b.book_id = br.book_id
    GROUP BY
        p.publisher_id, p.publisher_name
    ORDER BY
        borrow_count DESC
    LIMIT 1
)

SELECT
    b.title AS book_title,
    GROUP_CONCAT(a.author_name, ', ') AS authors
FROM
    book b
JOIN
    book_author ba ON b.book_id = ba.book_id
JOIN
    author a ON ba.author_id = a.author_id
JOIN
    Поп_Изд pp ON b.publisher_id = pp.publisher_id
GROUP BY
    b.book_id, b.title
ORDER BY
    b.title;""",
    con,
)

print(df)

con.close()
