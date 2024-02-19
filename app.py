from dotenv import load_dotenv
load_dotenv() ## load all the environement variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Model and provide SQL query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    return response.text

## Function to retrieve query from the sql database
def read_sql_query(sql, db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        # Debugging line to print the SQL command
        # st.write(f"Executing SQL query: {sql}")
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except sqlite3.OperationalError as e:
        # Print the SQL error if any
        st.error(f"SQL error: {e}")
        return None
    finally:
        cur.close()
        conn.close()
## define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database is named crime and has the following columns - "S. No", "Category", "State/UT", "2016", "2017", "2018", "Percentage Share of State/UT (2018)", "Mid-Year Projected Population (in Lakhs) (2018)", & "Rate of Total Cyber Crimes (2018)".
    
    Example 1: What is the total number of cyber crimes recorded in 2017?
    SQL command will be: SELECT SUM("2017") FROM crime;
    
    Example 2: Which state has the highest percentage share of cyber crimes in 2018?
    SQL command will be: SELECT "State/UT" FROM crime ORDER BY "Percentage Share of State/UT (2018)" DESC LIMIT 1;
    
    Example 3: What are the average cyber crimes reported from 2016 to 2018?
    SQL command will be: SELECT AVG("2016"), AVG("2017"), AVG("2018") FROM crime;
    
    Example 4: How many states have a cyber crime rate of more than 2 in 2018?
    SQL command will be: SELECT COUNT(*) FROM crime WHERE "Rate of Total Cyber Crimes (2018)" > 2;
    
    Example 5: List all the states with a mid-year projected population of over 500 lakhs in 2018.
    SQL command will be: SELECT "State/UT" FROM crime WHERE "Mid-Year Projected Population (in Lakhs) (2018)" > 500;
    
    Example 6: What was the total number of cyber crimes in 'Kerala' over the years 2016 to 2018?
    SQL command will be: SELECT "2016" + "2017" + "2018" AS total_crimes FROM crime WHERE "State/UT" = 'Kerala';
    """
]


## Streamlit APP
# Set page config with page title
st.set_page_config(page_title="NetPatrol Hub")

# Set up custom styles for the background and logo
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/YSW1XqC3/net-Patrol.jpg');
        background-size: cover;
    }
  </style>
    """, unsafe_allow_html=True)

# Your header
st.header("Gemini App to Retrieve SQL Data from our cyber crime database  of year 2016-2018")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    full_response = get_gemini_response(question, prompt)
    
    # Extract the actual SQL command by ensuring it starts with "SELECT"
    sql_command_start = full_response.find("SELECT")
    
    if sql_command_start != -1:
        # Extract the SQL command from the full response
        sql_command = full_response[sql_command_start:]
        
        # Ensure the command is a single statement (optional step, see note below)
        sql_statements = sql_command.split(';')
        sql_command_clean = sql_statements[0].strip()

        # Debug: Print the clean SQL command for verification
        st.write(f"Executing SQL query: {sql_command_clean}")
        
        try:
            # Execute the extracted SQL command
            data = read_sql_query(sql_command_clean, "cyber_crime_data.db")
            if data is not None:
                st.subheader("The Response is")
                for row in data:
                    st.write(row)
            else:
                st.error("Failed to execute SQL query.")
        except sqlite3.ProgrammingError as e:
            st.error(f"SQL execution error: {e}")
    else:
        st.error("Valid SQL command not found in the response.")
