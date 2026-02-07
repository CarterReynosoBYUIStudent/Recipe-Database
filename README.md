# Recipe-Database

Recipe software that stores ingredients in a PostgreSQL database.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Download PostgreSQL from https://www.postgresql.org/download/ and install it.
2. Open pgAdmin or your preferred PostgreSQL client and create a new database named recipedb.
3. Create the required tables by running the following SQL commands:
"  -- Table for meals
CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table for recipes with JSONB ingredients
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    meal_id INT REFERENCES meals(id) ON DELETE CASCADE,
    description TEXT,
    ingredients JSONB
);"

4. Install Python and required libraries:
  "pip install sqlalchemy psycopg2"
5. Download the provided Python file
6. Run the Python file in VSCode


Instructions for using the software:

1. First step here
2.
3.

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* First thing here
*
*

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Website Title](Link)
*
*

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] First thing here
* [ ]
* [ ]
