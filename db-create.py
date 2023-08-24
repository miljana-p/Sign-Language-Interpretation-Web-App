import sqlite3

db_locale = 'signLanguage.db'
connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
CREATE TABLE SignList
(
id integer primary key autoincrement,
sign text,
name text
)
""")

c.execute("""
CREATE TABLE LanguageScore
(
id integer primary key autoincrement,
name text,
highScore integer
)
""")

c.execute("""
CREATE TABLE FraseList
(
id integer primary key autoincrement,
name text,
savedFrase string
)
""")

connie.commit()
connie.close()
