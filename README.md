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

1. Launch the program
2. Use the menu to: Add a new meal and its recipe. Update an existing meal or its ingredients. Delete a meal. View a meal’s description and ingredients.
3. Follow the on-screen prompts for entering meal names, descriptions, and ingredient quantities.

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.10+
* PostgreSQL 15+
* SQLAlchemy 2.x
* psycopg2 2.x (PostgreSQL adapter for Python)

## Useful Websites to Learn More

I found these websites useful in developing this software:

* https://www.postgresql.org/docs/
* https://docs.sqlalchemy.org/en/20/
* https://youtu.be/skHrcqRRWLs?si=4MMnPcQ5BPaPHViF

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* Add/Edit instructions
* View Common Ingredients between recipes.
