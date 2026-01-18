import sqlite3
import datetime

DB_FILE = "chat_database.db"

def init_db():
    con = sqlite3.connect(DB_FILE)
    
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            ip_address TEXT
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS user_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            timestamp TEXT,
            token TEXT
        )
    """)
    
    con.commit()
    con.close()
    print("db initialized")

def update_user_ip(name, ip):
    try:
        con = sqlite3.connect(DB_FILE)

        # ip adress and name
        con.execute("INSERT OR REPLACE INTO users (username, ip_address) VALUES (?, ?)", (name, ip))
        
        con.commit()
        con.close()
    except:
        print("error saving ip")

def save_message(name, msg, token):
    con = sqlite3.connect(DB_FILE)
    
    # gets date
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    
    con.execute("INSERT INTO user_messages (username, message, timestamp, token) VALUES (?, ?, ?, ?)", 
               (name, msg, today, token))
    
    con.commit()
    con.close()

def get_conversation(token):
    con = sqlite3.connect(DB_FILE)
    
    # get msgs for the specificv token
    cur = con.execute("SELECT * FROM user_messages WHERE token = ?", (token,))
    data = cur.fetchall()
    
    con.close()
    return data