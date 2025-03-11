import mysql.connector

# Database connection settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Zukaata_1245"
DB_NAME = "demologin"

# Connect to MySQL server
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = db.cursor()

# Create database if it doesn't exist
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
print(f"Database '{DB_NAME}' is ready.")

# Connect to the newly created database
db.database = DB_NAME

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL
    )
""")
print("Table 'users' is ready.")

# Commit and close
db.commit()
cursor.close()
db.close()
print("Database setup complete!")
