import pandas as pd
import sqlite3


con = sqlite3.connect("library.sqlite")

cursor = con.cursor()

df = pd.read_sql(
    """SELECT reader.reader_name AS Reader_Name, book.title AS Book_Name, book_reader.borrow_date, book_reader.return_date, CASE WHEN julianday(book_reader.return_date) - julianday(book_reader.borrow_date) <= 14 THEN 0 ELSE (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) - 14) * 2
END AS Пеня
FROM book_reader JOIN reader ON book_reader.reader_id = reader.reader_id
JOIN book ON book_reader.book_id = book.book_id
WHERE book_reader.return_date IS NOT NULL
AND julianday(book_reader.return_date) - julianday(book_reader.borrow_date) > 14 
ORDER BY Reader_Name ASC, Пеня DESC, Book_Name ASC""",
    con,
)

print(df)

con.close()
