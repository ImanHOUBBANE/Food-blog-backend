import sys
import sqlite3

def main():
    args = sys.argv
    if len(args) != 2:
        print("No DB name found.")
    data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
            "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
            "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
    name_DB = str(args[1])
    Conn = sqlite3.connect(name_DB)
    Cur = Conn.cursor()
    Cur.execute(f"PRAGMA foreign_keys = ON;")
    Cur.execute(f"create table if not exists meals (meal_id integer primary key autoincrement not null, meal_name text unique not null);")
    Cur.execute(f"create table if not exists ingredients  (ingredient_id integer primary key autoincrement, ingredient_name text unique not null);")
    Cur.execute(f"create table if not exists measures (measure_id integer primary key autoincrement, measure_name text unique);")
    Conn.commit()
    fill = False
    while not fill:


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

    Cur.execute(f"create table if not exists recipes (recipe_id integer primary key autoincrement  , recipe_name text not null, recipe_description text);")
    Cur.execute(f"create table if not exists serve (serve_id integer primary key autoincrement , meal_id integer not null, recipe_id integer  not null ,foreign key (meal_id) REFERENCES meals (meal_id) on delete cascade on update cascade, foreign key (recipe_id) REFERENCES recipes (recipe_id) on delete cascade on update cascade);")
    Cur.execute(f"create table if not exists quantity (quantity_id integer primary key autoincrement , quantity integer not null ,recipe_id integer not null, measure_id integer not null ,ingredient_id integer  not null ,foreign key (measure_id) REFERENCES measures (measure_id) on delete cascade on update cascade, foreign key (recipe_id) REFERENCES recipes (recipe_id) on delete cascade on update cascade,foreign key (ingredient_id) REFERENCES ingredients (ingredient_id) on delete cascade on update cascade);")
    Conn.commit()
    while True:
        print("Pass the empty recipe name to exit.")
        print("Recipe name: ")
        name = str(input())
        if len(name) != 0:
            print("Recipe description: ")
            description = str(input())
            Cur.execute("insert into recipes (recipe_name,recipe_description) values(?,?)", (name, description))
            Conn.commit()
            available_meals = ""
            for mealtimes_indices in range(4):
                meal_id = Cur.execute(f"select meal_id from meals where meal_name=?", (data['meals'][mealtimes_indices],)).fetchall()
                available_meals += str(meal_id[0][0])
                Conn.commit()
                available_meals += ") "
                meal_name = Cur.execute(f"select meal_name from meals where meal_id=?", (meal_id[0][0],)).fetchall()
                available_meals += str(meal_name[0][0])
                available_meals += " "
                Conn.commit()
            print(available_meals)
            print("When the dish can be served:")
            good_option = False
            while not good_option:
                try:
                    input_client = input().split()
                except Exception :
                    print("Choose a valid option.")
                    input_client = input().split()
                else:
                    good_option = True
            for indice in range(len((input_client))):
                recipe_identifier=Cur.execute("select recipe_id from recipes where recipe_name=? and recipe_description=?",(name, description)).fetchall()
                Cur.execute(f"insert into serve (meal_id,recipe_id) values (?,?)", (int(input_client[indice]), int(recipe_identifier[0][0])))
                Conn.commit()

            while True:
                print("Input quantity of ingredient <press enter to stop>:")
                quantity = input().split()
                if len(quantity) != 0:
                    if len(quantity) == 2:
                        quantity.insert(1, '')
                        ingredients_name = Cur.execute("select ingredient_name from ingredients").fetchall()
                        count_ingredient = 0
                        get_ingredient = list()
                        for ingredient in ingredients_name:
                            if quantity[2] in ingredient[0]:
                                count_ingredient += 1
                                get_ingredient.append(ingredient[0])
                        if count_ingredient == 1 :
                            measure_id = Cur.execute("select measure_id from measures where measure_name=?",(quantity[1],)).fetchall()
                            ingredient_id = Cur.execute("select ingredient_id from ingredients where ingredient_name=? ", (str(quantity[2]),)).fetchall()
                            Cur.execute("insert into quantity (quantity,recipe_id,measure_id,ingredient_id)values(?,?,?,?)", (int(quantity[0]), int(recipe_identifier[0][0]), int(measure_id[0][0]),int(ingredient_id[0][0])))
                            Conn.commit()
                        else:
                            print("The ingredient is not conclusive!")



                    else:
                        measures_name = Cur.execute("select measure_name from measures ").fetchall()
                        count_measure = 0
                        get_measure = list()
                        for measure in measures_name:
                            if quantity[1] in measure[0]:
                                count_measure += 1
                                get_measure.append(measure[0])
                        if count_measure != 1:
                            print("The measure is not conclusive!")
                        ingredients_name = Cur.execute("select ingredient_name from ingredients").fetchall()
                        count_ingredient = 0
                        get_ingredient = list()
                        for ingredient in ingredients_name:
                            if quantity[2] in ingredient[0]:
                                count_ingredient += 1
                                get_ingredient.append(ingredient[0])
                        if count_ingredient == 1 and count_measure== 1:
                            measure_id=Cur.execute("select measure_id from measures where measure_name=?", (get_measure[0],)).fetchall()
                            ingredient_id=Cur.execute("select ingredient_id from ingredients where ingredient_name=? ",(str(get_ingredient[0]),)).fetchall()
                            Cur.execute("insert into quantity (quantity,recipe_id,measure_id,ingredient_id)values(?,?,?,?)", (int(quantity[0]), int(recipe_identifier[0][0]), int(measure_id[0][0]), int(ingredient_id[0][0])))
                            Conn.commit()

                        if count_ingredient != 1:
                            print("The ingredient is not conclusive!")


                else:
                    break

            Conn.commit()

        else:
            Conn.close()
            exit(1)
if __name__ == '__main__':
    main()















