import pandas as pd
import sqlite3


con = sqlite3.connect("library.sqlite")

cursor = con.cursor()

df = pd.read_sql(
    """SELECT
    reader.reader_name AS Reader_Name,
    CASE
        WHEN EXISTS (SELECT 1 FROM book_reader WHERE book_reader.reader_id = reader.reader_id AND julianday('now') - julianday(borrow_date) > 21) THEN 'Чёрный список'
        WHEN NOT EXISTS (SELECT 1 FROM book_reader WHERE book_reader.reader_id = reader.reader_id) THEN 'Неактивный читатель'
        ELSE 'Добросовестный читатель'
    END AS Статус
FROM
    reader;
""",
    con,
)

print(df)

con.close()
