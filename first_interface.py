import sys
import sqlite3
import argparse
import collections


def main():

    args = sys.argv

    if len(args) < 2:
        print("No DB name found.")

    if len(args) > 2:

        name_DB = args[1]
        Conn = sqlite3.connect(name_DB)
        Cur = Conn.cursor()
        ingredients_string = str(args[2]).replace("--ingredients=", "").split(',')
        meals_string = str(args[3]).replace("--meals=", "").split(',')
        ingredient_id_liste = list()
        meal_id_input = list()
        for meal in meals_string:
            meals_id = Cur.execute(f"select meal_id from meals where meal_name=?", (meal.strip(),)).fetchall()
            if meals_id == []:
                print("There are no such recipes in the database.")
                exit(1)
            else:
                meal_id_input.append(meals_id[0][0])

        for ingredient in ingredients_string:

            ingredient_id = Cur.execute(f"select ingredient_id from ingredients where ingredient_name = ?" ,(ingredient.strip(), )).fetchall()
            if ingredient_id == []:
                print("There are no such recipes in the database.")
                exit(1)
            else:
                ingredient_id_liste.append(ingredient_id[0][0])
        liste_totale_recipe = list()
        for ingredient in ingredient_id_liste:
            liste_recipe_per_ingredient = Cur.execute(f"select recipe_id from quantity where ingredient_id=? ",(ingredient,)).fetchall()
            set_ingredient_recipe = list()
            for recipe_id in liste_recipe_per_ingredient:
                set_ingredient_recipe.append(recipe_id[0])
            liste_totale_recipe.append(set_ingredient_recipe)
        item_count = list()
        intersection = list()
        if len(liste_totale_recipe) == 1:
            intersection.extend(liste_totale_recipe[0])
        else:
            for recipe in liste_totale_recipe:
                item_count_one = [(item,count) for item, count in collections.Counter(recipe).items() if count > 1]
                item_count.extend(item_count_one)
            for recipe_liste in range(len(liste_totale_recipe)):
                liste_totale_recipe[recipe_liste] = set(liste_totale_recipe[recipe_liste])
            intersection = list(set.intersection(*liste_totale_recipe))
            for set_intersection in intersection:
                for recipe_id in item_count:
                    if set_intersection == recipe_id[0]:
                        for k in range(1, recipe_id[1]-1):
                            intersection.append(set_intersection)

        recipe_id_meal_id_ingredient_id = list()
        for recipe_id in intersection:
            found = False
            list_meal_time = list()
            list_meal_with_tuple = Cur.execute("select meal_id from serve where recipe_id = ?",(recipe_id,)).fetchall()
            for meal_id in list_meal_with_tuple:
                list_meal_time.append(meal_id[0])
            for meal_id in list_meal_time:
                if meal_id in meal_id_input:
                    found = True
                    break
            if found == True :
                recipe_id_meal_id_ingredient_id.append(recipe_id)
        recipe_name_final = list()
        for recipe_id in recipe_id_meal_id_ingredient_id:
            recipe_name = Cur.execute(f"select recipe_name from recipes where recipe_id = ?", (recipe_id,)).fetchall()[0][0]
            recipe_name_final.append(recipe_name)
        if len(recipe_name_final) != 0:
            print("Recipes selected for you:")
            resultat = ''
            for indice_recipe in range(len(recipe_name_final)):
                resultat += recipe_name_final[indice_recipe]
                if indice_recipe != len(recipe_name_final)-1:
                    resultat += ' , '
                else:
                    resultat += '.'
            print(resultat)
            Conn.close()
            exit(1)
        else:
            print("There are no such recipes in the database.")
            Conn.close()
            exit(1)

    if len(args) == 2:

        data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
                "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
                "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
        name_DB = args[1]
        Conn = sqlite3.connect(str(name_DB))
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
        print("Pass the empty recipe name to exit.")
        while True:
            print("Recipe name: ")
            name = str(input())
            if len(name) != 0:
                print("Recipe description: ")
                description = str(input())
                Cur.execute("insert into recipes (recipe_name,recipe_description) values(?,?)",(name,description))
                Conn.commit()
                available_meals = ""
                for mealtimes_indices in range(4):
                    meal_id = Cur.execute(f"select meal_id from meals where meal_name=?",(data['meals'][mealtimes_indices],)).fetchall()
                    available_meals += str(meal_id[0][0])
                    Conn.commit()
                    available_meals += ") "
                    meal_name=Cur.execute(f"select meal_name from meals where meal_id=?",(meal_id[0][0],)).fetchall()
                    available_meals += str(meal_name[0][0])
                    available_meals += " "
                    Conn.commit()
                print(available_meals)
                print("When the dish can be served:")
                good_option=False
                while not good_option:
                    try:
                        input_client=input().split()
                    except Exception:
                        print("Choose a valid option.")
                        input_client = input().split()
                    else:
                        good_option=True
                for indice in range(len((input_client))):
                    recipe_identifier=Cur.execute("select recipe_id from recipes where recipe_name=? and recipe_description=?", (name, description)).fetchall()
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
                            if count_ingredient == 1:
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
                                measure_id = Cur.execute("select measure_id from measures where measure_name=?", (get_measure[0],)).fetchall()
                                ingredient_id = Cur.execute("select ingredient_id from ingredients where ingredient_name=? ",(str(get_ingredient[0]),)).fetchall()
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















