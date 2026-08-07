import sqlite3
import pandas as pd

# Connect to a database file (creates it if it doesn't exist yet)
conn = sqlite3.connect("employees.db")

# Load our CSV and save it INTO the database as a table
df = pd.read_csv("employees_full.csv")
df.to_sql("employees", conn, if_exists="replace", index=False)

# Now query it back using SQL
result = pd.read_sql("SELECT * FROM employees WHERE department = 'Engineering'", conn)
print(result)

# Or use pandas-style filtering after reading it all back
all_data = pd.read_sql("SELECT * FROM employees", conn)
print(all_data.groupby("department")["salary"].mean())

conn.close()