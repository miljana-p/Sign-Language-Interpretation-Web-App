import sqlite3

db_locale = 'signLanguage.db'
connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
INSERT INTO SignList
(
sign,
name
)
values 
('A', 'Serbian Sign Language'),
('B', 'Serbian Sign Language'),
('V', 'Serbian Sign Language'),
('G', 'Serbian Sign Language'),
('D', 'Serbian Sign Language'),
('Dj', 'Serbian Sign Language'),
('E', 'Serbian Sign Language'),
('Zj', 'Serbian Sign Language'),
('Z', 'Serbian Sign Language'),
('I', 'Serbian Sign Language'),
('J', 'Serbian Sign Language'),
('K', 'Serbian Sign Language'),
('L', 'Serbian Sign Language'),
('Lj', 'Serbian Sign Language'),
('M', 'Serbian Sign Language'),
('N', 'Serbian Sign Language'),
('Nj', 'Serbian Sign Language'),
('O', 'Serbian Sign Language'),
('P', 'Serbian Sign Language'),
('R', 'Serbian Sign Language'),
('S', 'Serbian Sign Language'),
('T', 'Serbian Sign Language'),
('Cj', 'Serbian Sign Language'),
('U', 'Serbian Sign Language'),
('F', 'Serbian Sign Language'),
('H', 'Serbian Sign Language'),
('C', 'Serbian Sign Language'),
('Cz', 'Serbian Sign Language'),
('Dz', 'Serbian Sign Language'),
('Sj', 'Serbian Sign Language'),
('Ja sam', 'Serbian Sign Language'),
('Cao', 'Serbian Sign Language')      
""")

c.execute("""
INSERT INTO SignList
(
sign,
name
)
values 
('A', 'American Sign Language'),
('B', 'American Sign Language'),
('C', 'American Sign Language'),
('D', 'American Sign Language'),
('E', 'American Sign Language'),
('F', 'American Sign Language'),
('G', 'American Sign Language'),
('H', 'American Sign Language'),
('I', 'American Sign Language'),
('J', 'American Sign Language'),
('K', 'American Sign Language'),
('L', 'American Sign Language'),
('M', 'American Sign Language'),
('N', 'American Sign Language'),
('O', 'American Sign Language'),
('P', 'American Sign Language'),
('Q', 'American Sign Language'),
('R', 'American Sign Language'),
('S', 'American Sign Language'),
('T', 'American Sign Language'),
('U', 'American Sign Language'),
('V', 'American Sign Language'),
('W', 'American Sign Language'),
('X', 'American Sign Language'),
('Y', 'American Sign Language'),
('Z', 'American Sign Language'),
('Hello', 'American Sign Language'),
('My name', 'American Sign Language'),
('How are you', 'American Sign Language')
""")

c.execute("""
INSERT INTO LanguageScore
(
highScore,
name
)
values 
(0, 'Serbian Sign Language'),
(0, 'American Sign Language')
""")

connie.commit()
connie.close()
