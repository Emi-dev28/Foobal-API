import sqlite3

# sqlite Settings
Database = "Prueba.sqlite"
# sqlite Connection
conn = sqlite3.connect(Database)
cur = conn.cursor()

