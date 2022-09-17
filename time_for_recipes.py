import sys
import sqlite3

def main():
    args = sys.argv
    if len(args) != 2:
        print("No DB name found.")
    name_DB = str(args[1])
    Conn = sqlite3.connect(name_DB)
    Cur = Conn.cursor()
    Cur.execute(f"create table if not exists meals (meal_id integer primary key autoincrement , meal_name text unique not null);")
    Cur.execute(f"create table if not exists ingredients  (ingredient_id integer primary key autoincrement, ingredient_name text unique not null);")
    Cur.execute(f"create table if not exists measures (measure_id integer primary key autoincrement, measure_name text unique);")
    Conn.commit()
    fill = False
    while not fill:
        data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
                "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
                "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


        Cur.execute(f"insert into meals (meal_name) values('breakfast')")
        Cur.execute(f"insert into meals (meal_name) values('brunch')")
        Cur.execute(f"insert into meals (meal_name) values('lunch')")
        Cur.execute(f"insert into meals (meal_name) values('supper')")
        Conn.commit()

        Cur.execute(f"insert into ingredients (ingredient_name) values('milk')")
        Cur.execute(f"insert into ingredients (ingredient_name) values('cacao')")
        Cur.execute(f"insert into ingredients (ingredient_name) values('strawberry')")
        Cur.execute(f"insert into ingredients (ingredient_name) values('blueberry')")
        Cur.execute(f"insert into ingredients (ingredient_name) values('blackberry')")
        Cur.execute(f"insert into ingredients (ingredient_name) values('sugar')")
        Conn.commit()

        Cur.execute(f"insert into measures  (measure_name) values('ml')")
        Cur.execute(f"insert into measures  (measure_name) values('g')")
        Cur.execute(f"insert into measures  (measure_name) values('l')")
        Cur.execute(f"insert into measures  (measure_name) values('cup')")
        Conn.commit()

        Cur.execute(f"insert into measures  (measure_name) values('tbsp')")
        Cur.execute(f"insert into measures  (measure_name) values('tsp')")
        Cur.execute(f"insert into measures  (measure_name) values('dsp')")
        Cur.execute(f"insert into measures  (measure_name) values('')")
        Conn.commit()
        fill = True

    Cur.execute(f"create table if not exists recipes (recipe_id integer primary key autoincrement , recipe_name text not null, recipe_description text);")
    Conn.commit()
    print("Pass the empty recipe name to exit.")
    while True:
        print("Recipe name: ")
        name = str(input())
        if len(name) != 0:
            print("Recipe description: ")
            description = str(input())
            Cur.execute("insert into recipes (recipe_name,recipe_description) values(?,?)", (name, description))
            Conn.commit()

        else:
            Conn.close()
            exit(1)
if __name__ == '__main__':
    main()















