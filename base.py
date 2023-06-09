import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="test"
)

# Create a cursor object
mycursor = mydb.cursor()

# Execute a SQL query to delete all the rows from a specific table
sql = "DELETE FROM attendance"
mycursor.execute(sql)

# Commit the changes to the database
mydb.commit()

# Print the number of rows that were deleted
print(mycursor.rowcount, "rows deleted")
