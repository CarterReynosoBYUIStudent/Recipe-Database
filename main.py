from sqlalchemy import create_engine, text

# -------------------- Database Setup --------------------
USERNAME = "postgres"
PASSWORD = "password"
DATABASE_NAME = "recipedb"
HOST = "localhost"
PORT = "5432"

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}")

# -------------------- User Functions -------------------
def user_new_meal():
    """Get input from user to create a new meal"""
    name = input("Enter meal name: ").strip()
    description = input("Enter meal description: ").strip()

    ingredients = []
    while True:
        item = input("Enter ingredient name (or press enter to finish): ").strip()
        if not item:
            break
        quantity = input(f"Enter quantity for {item}: ").strip()
        measurement = input(f"Enter measurement for {item} (e.g., tsp, lbs): ").strip()
        ingredients.append({"item": item, "quantity": float(quantity), "measurement": measurement})

    # Format data into a JSON-like dictionary
    return {"name": name, "description": description, "ingredients": ingredients}


def user_update_meal():
    """Get user input to update a meal"""
    meal_id = int(input("Enter the meal ID to update: "))
    name = input("Enter new name (or leave blank to skip): ").strip()
    description = input("Enter new description (or leave blank to skip): ").strip()

    ingredients = []
    update_ingredients = input("Do you want to update ingredients? (y/n): ").strip().lower()
    if update_ingredients == "y":
        while True:
            item = input("Enter ingredient name (or press enter to finish): ").strip()
            if not item:
                break
            quantity = input(f"Enter quantity for {item}: ").strip()
            measurement = input(f"Enter measurement for {item} (e.g., tsp, lbs): ").strip()
            ingredients.append({"item": item, "quantity": float(quantity), "measurement": measurement})

    return {
        "meal_id": meal_id,
        "name": name if name else None,
        "description": description if description else None,
        "ingredients": ingredients if ingredients else None
    }


def user_delete_meal():
    """Get user input to delete a meal"""
    meal_id = int(input("Enter the meal ID to delete: "))
    return {"meal_id": meal_id}


# -------------------- SQL System Functions --------------------
def system_show_meal(meal_id):
    with engine.connect() as connection:
        # Get meal name
        meal_result = connection.execute(
            text("SELECT name FROM meals WHERE id = :meal_id"),
            parameters={"meal_id": meal_id}
        ).fetchone()
        
        if not meal_result:
            print(f"No meal found with ID {meal_id}.")
            return
        
        meal_name = meal_result[0]

        # Get recipe (description + ingredients)
        recipe_result = connection.execute(
            text("SELECT description, ingredients FROM recipes WHERE meal_id = :meal_id"),
            parameters={"meal_id": meal_id}
        ).fetchone()
        
        if not recipe_result:
            print(f"No recipe found for meal ID {meal_id}.")
            return
        
        description, ingredients = recipe_result  # ingredients is already a list

        # Display meal info
        print(f"\n--- Meal ID {meal_id}: {meal_name} ---")
        print(f"Description: {description}")
        print("Ingredients:")
        for ing in ingredients:
            print(f" - {ing['quantity']} {ing['measurement']} {ing['item']}")
        print("\n")


def system_add_meal(name, description, ingredients):
    import json
    with engine.connect() as connection:
        # Insert meal into meals table
        insert_meal_query = text("""
            INSERT INTO meals (name)
            VALUES (:name)
            RETURNING id
        """)
        result = connection.execute(insert_meal_query, parameters={"name": name})
        meal_id = result.fetchone()[0]

        # Insert recipe into recipes table with JSONB ingredients
        insert_recipe_query = text("""
            INSERT INTO recipes (meal_id, description, ingredients)
            VALUES (:meal_id, :description, :ingredients)
        """)
        connection.execute(insert_recipe_query, parameters={
            "meal_id": meal_id,
            "description": description,
            "ingredients": json.dumps(ingredients)  # convert Python list to JSON
        })

        connection.commit()
    print(f"Meal '{name}' added with ID {meal_id}.")



def system_update_meal(meal_id, name=None, description=None, ingredients=None):
    import json
    with engine.connect() as connection:
        if name:
            connection.execute(text("UPDATE meals SET name = :name WHERE id = :meal_id"),
                               parameters={"meal_id": meal_id, "name": name})
        if description or ingredients:
            update_fields = []
            params = {"meal_id": meal_id}
            if description:
                update_fields.append("description = :description")
                params["description"] = description
            if ingredients is not None:
                update_fields.append("ingredients = :ingredients")
                params["ingredients"] = json.dumps(ingredients)
            query = text(f"UPDATE recipes SET {', '.join(update_fields)} WHERE meal_id = :meal_id")
            connection.execute(query, parameters=params)

        connection.commit()
    print(f"Meal ID {meal_id} updated.")


def system_delete_meal(meal_id):
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM meals WHERE id = :meal_id"), parameters={"meal_id": meal_id})
        connection.commit()
    print(f"Meal ID {meal_id} deleted.")


# -------------------- Main Program --------------------
def main():
    while True:
        print("\n--- Recipe Database ---")
        print("1. Add new meal")
        print("2. Update existing meal")
        print("3. Delete meal")
        print("4. Show meal and recipe")
        print("5. Exit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            data = user_new_meal()
            system_add_meal(**data)
        elif choice == "2":
            data = user_update_meal()
            system_update_meal(**data)
        elif choice == "3":
            data = user_delete_meal()
            system_delete_meal(**data)
        elif choice == "4": 
            meal_id = int(input("Enter meal ID to show: ").strip())
            system_show_meal(meal_id)
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()


