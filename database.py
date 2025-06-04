import sqlite3

def init_db():
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS tracking (user_id INTEGER, article TEXT, last_price INTEGER, notify_levels TEXT)")
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def add_tracking(user_id, article, price):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("INSERT INTO tracking (user_id, article, last_price, notify_levels) VALUES (?, ?, ?, ?)",
              (user_id, article, price, "2,3,5"))
    conn.commit()
    conn.close()

def get_all_tracking():
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tracking")
    rows = c.fetchall()
    conn.close()
    return rows

def update_price(user_id, article, new_price):
    conn = sqlite3.connect("bot.db")
    c = conn.cursor()
    c.execute("UPDATE tracking SET last_price = ? WHERE user_id = ? AND article = ?", (new_price, user_id, article))
    conn.commit()
    conn.close()
