import pandas as pd
import sqlite3


con = sqlite3.connect("library.sqlite")

cursor = con.cursor()

df = pd.read_sql(
    """SELECT b.title AS "Название книги",
       g.genre_name AS "Жанр",
       p.publisher_name AS "Издательство",
       CASE
           WHEN b.available_numbers > ROUND(AVG(b.available_numbers) OVER (), 0) THEN 'больше на ' || (b.available_numbers - ROUND(AVG(b.available_numbers) OVER (), 0))
           WHEN b.available_numbers < ROUND(AVG(b.available_numbers) OVER (), 0) THEN 'меньше на ' || (ROUND(AVG(b.available_numbers) OVER (), 0) - b.available_numbers)
           ELSE 'равно среднему'
       END AS "Отклонение"
FROM book b
JOIN genre g ON b.genre_id = g.genre_id
JOIN publisher p ON b.publisher_id = p.publisher_id
ORDER BY b.title ASC, "Отклонение" ASC;
""",
    con,
)

print(df)

con.close()
