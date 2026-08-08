import sqlite3
import pandas as pd

#connect to the SQLite database
conn = sqlite3.connect("employees.db")

#Load the data
df = pd.read_csv("employees_full.csv")

#Save the data into SQLite
df.to_sql("employees", conn, if_exists = "replace", index = False)
print("Employee data successfully loaded into sqlite!")

#Close the connection
conn.close()