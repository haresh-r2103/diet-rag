import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gym"
)
cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS diet_chatbot")
cursor.execute("USE diet_chatbot")

# Create table for user storage
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        weight FLOAT,
        height FLOAT,
        goal VARCHAR(255),
        diet_preference VARCHAR(255)
    )
""")

conn.commit()
cursor.close()
conn.close()
print("✅ User database setup completed.")
