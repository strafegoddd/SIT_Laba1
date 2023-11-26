import pandas as pd
import sqlite3


con = sqlite3.connect("library.sqlite")

cursor = con.cursor()

df = pd.read_sql(
    """SELECT
    br.reader_id AS reader_id,
    SUM(
        CASE
            WHEN (br.return_date - br.borrow_date) < 14 THEN 5
            WHEN (br.return_date - br.borrow_date) BETWEEN 14 AND 30 THEN 2
            WHEN (br.return_date - br.borrow_date) > 30 THEN -2
            ELSE 1
        END
    ) AS total_points
FROM
    book_reader br
GROUP BY
    br.reader_id;
""",
    con,
)

print(df)

con.close()
