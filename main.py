#This is the main
import pandas as pd
from sqlalchemy import create_engine, text
# Create a connection to the database
USERNAEME = "postgres"
PASSWORD = "password"
DATABASE_NAME = "recipedb"
HOST = "localhost"
PORT = "5432"

engine = create_engine(f"postgresql://{USERNAEME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}")

with engine.connect() as connection:
    # Execute a simple query to test the connection
    result = connection.execute(text("SELECT version();"))
    version = result.fetchone()
    print(f"Connected to database: {version[0]}")

with engine.connect() as connection:
    # Execute a simple query to test the connection
    result = connection.execute(text("SELECT * FROM meals;"))
    meals = result.fetchall()
    for meal in meals:
        print(meal)