import sqlite3

db_locale = 'signLanguage.db'

def get_libraries():
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute("""
    SELECT distinct name FROM SignList
    """)
    data = c.fetchall()
    return_data = []
    for name in data:
        charlist = []
        fraseList=[]
        query = f"""
            SELECT sign FROM SignList
            WHERE name = '{name[0]}'
        """
        c.execute(query)
        charlistdata = c.fetchall()
        query = f"""
            SELECT savedFrase FROM FraseList
            WHERE name = '{name[0]}'
        """
        c.execute(query)
        fraselistdata = c.fetchall()
        for ch in charlistdata:
            charlist.append(ch[0])
        for fr in fraselistdata:
            fraseList.append(fr[0])
        return_data.append((name[0], charlist, fraseList))
    return return_data

def get_Signs(name):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    charlist = []
    query = f"""
            SELECT sign FROM SignList
            WHERE name = '{name}'
        """
    c.execute(query)
    charlistdata = c.fetchall()
    for ch in charlistdata:
        charlist.append(ch[0])
    return charlist

def get_HighScore(name):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    query = f"""
            SELECT highScore FROM LanguageScore
            WHERE name = '{name}'
        """
    c.execute(query)
    highScore = c.fetchall()
    print(highScore)
    return highScore[0][0]

def change_HighScore(name, new_Points):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    query_select = f"""
        SELECT highScore FROM LanguageScore
        WHERE name = '{name}'
    """
    c.execute(query_select)
    current_high_score = c.fetchall()
    if current_high_score is None or new_Points > current_high_score[0][0]:
        query_update = f"""
            UPDATE LanguageScore
            SET highScore = {new_Points}
            WHERE name = '{name}'
        """
        c.execute(query_update)
        connie.commit()
    connie.close()

def saveFrase(name, frase):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    save = f"""
        INSERT INTO FraseList
        (
        savedFrase,
        name
        )
        values
        ('{frase}', '{name}')
    """
    c.execute(save)
    connie.commit()
    connie.close()

def get_Frases(name):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    charlist = []
    query = f"""
            SELECT savedFrase FROM FraseList
            WHERE name = '{name}'
        """
    c.execute(query)
    charlistdata = c.fetchall()
    for ch in charlistdata:
        charlist.append(ch[0])
    return charlist
