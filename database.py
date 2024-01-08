import sqlite3

# Создаем таблицу
connection = sqlite3.connect('Money.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()

# Таблица пользователей
sql.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, id INTEGER, phone_number TEXT, location TEXT);")


# Регистрация
def registration(name, id, phone_number, location):
    sql.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (name, id, phone_number, location))
    connection.commit()


# Проверка на наличие пользователя в БД
def checker(id):
    check = sql.execute("SELECT id FROM users WHERE id = ?", (id, ))
    if check.fetchone():
        return True
    else:
        return False