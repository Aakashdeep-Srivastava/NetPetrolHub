import sqlite3
import pandas as pd

# Correct file path for your CSV file
file_path = "E:\\LLM Text to SQL\\cyber_crimes.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('E:\\LLM Text to SQL\\cyber_crime_data.db')  # Include the full path if needed
cursor = conn.cursor()

# Create table (if not already existing)
# Adjust data types and constraints as per your requirements
cursor.execute('''
    CREATE TABLE IF NOT EXISTS crime (
        "S. No" INTEGER PRIMARY KEY,
        "Category" TEXT,
        "State/UT" TEXT,
        "2016" INTEGER,
        "2017" INTEGER,
        "2018" INTEGER,
        "Percentage Share of State/UT (2018)" REAL,
        "Mid-Year Projected Population (in Lakhs) (2018)" REAL,
        "Rate of Total Cyber Crimes (2018)" REAL
    )
''')

# Use pandas to directly insert the DataFrame into the SQLite table
df.to_sql('crime', conn, if_exists='append', index=False, method='multi')

# Commit the changes
conn.commit()

# Retrieve and display all records to verify insertion
cursor.execute("SELECT * FROM crime")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
