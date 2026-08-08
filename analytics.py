import sqlite3
import pandas as pd

#connect to database
conn = sqlite3.connect("employees.db")

#SQLquery
query = """
SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department
ORDER BY average_salary DESC;
"""

#run the query
result = pd.read_sql_query(query, conn)

print(result)

#close the connection
conn.close()
