import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#connect to the database
conn = sqlite3.connect("employees.db")

#SQL query
query = """
SELECT department, AVG(salary) AS average_salary
FROM employees
GROUP BY department
ORDER BY average_salary DESC;
"""

#Get the data
result = pd.read_sql_query(query, conn)

#Close the database connection
conn.close()

#create the chart
plt.bar(result["department"], result["average_salary"])

#add labels and title
plt.xlabel("Department")
plt.ylabel("Average salary")
plt.title("Average salary by department")

#Display the chart
plt.show()