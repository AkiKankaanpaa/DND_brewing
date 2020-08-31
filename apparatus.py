from tkinter import *
import random
import json
import string

# Used to determine the time units
TIME_UNITS = {"0": 0, "Rounds": 1, "Minutes": 2, "Hours": 3, "Days": 4, "Months": 5, "Infinite": 6}

BIOMES = ["All", "Arctic", "Coastal", "Deserts", "Forests", "Hills", "Jungles", "Lakes", "Mountain Peaks",
          "Plains", "Ocean", "Swamps", "Volcanic"]
RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Myth"]
PORTIONS = [1, 2, 3, 4]


class Window:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Brewing Apparatus")
        self.__window.configure(bg='dark goldenrod')

        # Used in calculation of the final crafting DC
        self.__dc_calc = {"Die": 0, "Plant Amount": 0, "Attribute Amount": 0, "Effect Amount": 0}

        # Information labels for the created potion
        self.__form = Label(text="", fg="black", bg="olive drab", height=1, width=100)
        self.__damage = Label(text="", fg="black", bg="dark olive green", height=1, width=100)
        self.__dc = Label(text="", fg="black", bg="olive drab", height=1, width=100)
        self.__time = Label(text="", fg="black", bg="dark olive green", height=1, width=100)
        self.__effects = Message(text="", fg="black", bg="olive drab", aspect=1500, justify=CENTER)
        self.__attributes = Message(text="", fg="black", bg="dark olive green", aspect=1500, justify=CENTER)
        self.__crafting_dc = Label(text="", fg="black", bg="olive drab", height=1, width=100)
        self.__errorlabel = Label(text="", fg="black", bg="dark olive green", height=1, width=100)

        self.__form.grid(row=0, column=1, sticky=N + W + E + S)
        self.__damage.grid(row=1, column=1, sticky=N + W + E + S)
        self.__dc.grid(row=2, column=1, sticky=N + W + E + S)
        self.__time.grid(row=3, column=1, sticky=N + W + E + S)
        self.__effects.grid(row=4, column=1, sticky=N + W + E + S)
        self.__attributes.grid(row=5, column=1, sticky=N + W + E + S)
        self.__crafting_dc.grid(row=6, column=1, sticky=N + W + E + S)
        self.__errorlabel.grid(row=7, column=1, sticky=N + W + E + S)

        # Clickdown-menus for the biome and rarity
        self.__biome_variable = StringVar()
        self.__biome_variable.set(BIOMES[0])
        self.__biome_option = OptionMenu(self.__window, self.__biome_variable, *BIOMES)
        self.__biome_option.configure(height=1, bg='dark goldenrod', width=15)
        self.__biome_option.grid(row=0, column=3, sticky=N + W + E + S, columnspan=1)

        self.__rarity_variable = StringVar()
        self.__rarity_variable.set(RARITIES[0])
        self.__rarity_option = OptionMenu(self.__window, self.__rarity_variable, *RARITIES)
        self.__rarity_option.configure(height=1, bg='dark goldenrod', width=15)
        self.__rarity_option.grid(row=0, column=4, sticky=N + W + E + S, columnspan=1)

        self.__shameless_self_promotionlabel = Label(text="This is not a finalized version of the product.",
                                                     fg="black", bg="chartreuse4", height=1, width=100)
        self.__shameless_self_promotionlabel.grid(row=8, column=1, sticky=N + W + E + S)

        self.__random_plant = Label(text="", fg="black", bg="dark olive green", height=1, width=21)
        self.__random_effect = Label(text="", fg="black", bg="dark olive green", height=1, width=21)
        self.__random_attribute = Label(text="", fg="black", bg="dark olive green", height=1, width=21)

        self.__random_plant.grid(row=2, column=3, columnspan=2, sticky=N + W + E + S)
        self.__random_effect.grid(row=4, column=3, columnspan=2, sticky=N + W + E + S)
        self.__random_attribute.grid(row=6, column=3, columnspan=2, sticky=N + W + E + S)

        # Choose to either show the desired bases or not
        self.__formvalue = IntVar()
        self.__formcheck = Checkbutton(text="Show Suitable Bases", bg='dark goldenrod',
                                       variable=self.__formvalue, onvalue=1, offvalue=0)
        self.__formcheck.grid(column=0, columnspan=1, row=0, sticky=W)

        # Entry-windows for the user to enter the plant names
        self.__entry1 = Entry(self.__window, width=50, fg="black", bg="lemon chiffon")
        self.__entry2 = Entry(self.__window, width=50, fg="black", bg="lemon chiffon")
        self.__entry3 = Entry(self.__window, width=50, fg="black", bg="lemon chiffon")
        self.__entry4 = Entry(self.__window, width=50, fg="black", bg="lemon chiffon")
        self.__entry5 = Entry(self.__window, width=50, fg="black", bg="lemon chiffon")
        self.__entry6 = Entry(self.__window, width=50, fg="black", bg="lemon chiffon")

        self.__entry1.grid(row=1, column=0)
        self.__entry2.grid(row=2, column=0)
        self.__entry3.grid(row=3, column=0)
        self.__entry4.grid(row=4, column=0)
        self.__entry5.grid(row=5, column=0)
        self.__entry6.grid(row=6, column=0)

        self.__defined_button = Button(self.__window, text="Create Potion", command=self.press_potion,
                                       height=1, width=42, fg="black", bg="chartreuse4")

        self.__effect_button = Button(self.__window, text="Random Effect", command=self.assign_random_effect,
                                      height=1, width=42, fg="black", bg="chartreuse4")

        self.__attribute_button = Button(self.__window, text="Random Attribute", command=self.assign_random_attribute,
                                         height=1, width=42, fg="black", bg="chartreuse4")

        self.__plant_button = Button(self.__window, text="Random Plant", command=self.assign_random_plant,
                                     height=1, width=42, fg="black", bg="chartreuse4")

        self.__defined_button.grid(row=8, column=0, sticky=N + W + E + S)
        self.__effect_button.grid(row=3, column=3, columnspan=2, sticky=N + W + E + S)
        self.__attribute_button.grid(row=5, column=3, columnspan=2, sticky=N + W + E + S)
        self.__plant_button.grid(row=1, column=3, columnspan=2, sticky=N + W + E + S)

        # Reads the plants.json file to generate the data structure for the plants
        # does the same with effect and attributes as well
        with open("plants.json", "r") as plant_json:
            self.__PLANTS = json.load(plant_json)

        with open("effects.json", "r") as effect_json:
            self.__EFFECTS = json.load(effect_json)

        with open("attributes.json", "r") as attribute_json:
            self.__ATTRIBUTES = json.load(attribute_json)

    def press_potion(self):
        namelist = []
        plant_amount = 0
        plantlist = []

        # Retrieving the strings from the Entry-windows
        if self.__entry1.get() != "":
            namelist.append(self.__entry1.get().lower())
            plant_amount += 1
        if self.__entry2.get() != "":
            namelist.append(self.__entry2.get().lower())
            plant_amount += 1
        if self.__entry3.get() != "":
            namelist.append(self.__entry3.get().lower())
            plant_amount += 1
        if self.__entry4.get() != "":
            namelist.append(self.__entry4.get().lower())
            plant_amount += 1
        if self.__entry5.get() != "":
            namelist.append(self.__entry5.get().lower())
            plant_amount += 1
        if self.__entry6.get() != "":
            namelist.append(self.__entry6.get().lower())
            plant_amount += 1

        # Checking if the plant-name given exists within the database
        counter = 1
        for name in namelist:
            plant_has_not_been_found = True
            for plant in self.__PLANTS:
                if plant["Name"] == name:
                    plantlist.append(plant)
                    self.color_entry(counter, True)
                    plant_has_not_been_found = False
                    break
            if plant_has_not_been_found:
                self.color_entry(counter, False)
            counter += 1

        # Checking if the given plant amount is the same as the verified amount
        if len(plantlist) == len(namelist):
            self.make_potion(plantlist, plant_amount)

        # If it isnt, show an error to the user
        else:
            self.make_potion_error()

    def make_potion(self, plantlist, plant_amount):
        self.__errorlabel.configure(text="", fg="black", bg="dark olive green")
        self.__dc_calc["Plant Amount"] = plant_amount
        self.calculate_save(plantlist)
        self.calculate_damage(plantlist)
        self.calculate_time(plantlist)
        self.determine_effects(plantlist)
        self.determine_attributes(plantlist)
        self.calculate_dc()

        if self.__formvalue.get() == 1:
            self.determine_form(plantlist)
        else:
            self.__form.configure(text="")

    def make_potion_error(self):
        self.__damage.configure(text="")
        self.__dc.configure(text="")
        self.__time.configure(text="")
        self.__effects.configure(text="")
        self.__attributes.configure(text="")
        self.__crafting_dc.configure(text="")
        self.__form.configure(text="")
        self.__errorlabel.configure(text="Unrecognized Ingredients or No Plants Entered.",
                                    fg="black", bg="firebrick")

    def color_entry(self, counter, plant_found):
        entries = {
            1: self.__entry1,
            2: self.__entry2,
            3: self.__entry3,
            4: self.__entry4,
            5: self.__entry5,
            6: self.__entry6,
        }
        if plant_found:
            entries[counter].configure(bg="green yellow")
        else:
            entries[counter].configure(bg="firebrick")

    def calculate_save(self, plantlist):
        if len(plantlist) != 0:
            max_dc = 0
            for plant in plantlist:
                if int(plant["DC"]) > int(max_dc):
                    max_dc = int(plant["DC"])
            self.__dc.configure(text="Save DC: " + str(max_dc))

    def calculate_damage(self, plantlist):
        valuedict = {}
        largest_die = 0
        for plant in plantlist:
            damage_listed = list(str(plant["Damage"]))
            # If it is 0
            if len(damage_listed) == 1:
                valuedict[plant["Damage"]] = 0
            elif len(damage_listed) == 3:
                valuedict[plant["Damage"]] = float(damage_listed[0])*(int(damage_listed[2])/2+0.5)
                if largest_die < int(damage_listed[2]):
                    largest_die = int(damage_listed[2])
            else:
                die = str(damage_listed[2]) + str(damage_listed[3])
                valuedict[plant["Damage"]] = float(damage_listed[0]) * (int(die)/2+0.5)
                if largest_die < int(die):
                    largest_die = int(die)
        self.__dc_calc["Die"] = largest_die
        if len(valuedict) != 0:
            value = max(valuedict, key=valuedict.get)
            self.__damage.configure(text="Damage: " + value)

    def calculate_time(self, plantlist):
        current_best = ["0", "Rounds"]
        for plant in plantlist:
            current = [plant["Time"], plant["Unit"]]
            checker = self.check_unit(current[1], current_best[1])
            if checker == 1:
                current_best[0] = current[0]
                current_best[1] = current[1]
            elif checker == 2:
                if self.check_die(current[0], current_best[0]):
                    current_best[0] = current[0]
                    current_best[1] = current[1]
        if current_best[1] == "Infinite":
            self.__time.configure(text="Duration: " + current_best[1])
        elif current_best[0] == "0":
            self.__time.configure(text="Duration: None")
        else:
            self.__time.configure(text="Duration: " + current_best[0] + " " + current_best[1])

    def check_unit(self, current, best):
        if TIME_UNITS[current] > TIME_UNITS[best]:
            return 1
        elif TIME_UNITS[current] == TIME_UNITS[best]:
            return 2
        else:
            return 3

    def check_die(self, current, best):
        current_split = list(current)
        best_listed = list(best)
        if len(current_split) <= 2:
            current = float(current)
        elif len(current_split) == 3:
            current = float(current_split[0]) * float(int(current_split[2]) / 2 + 0.5)
        else:
            die = str(current_split[2]) + str(current_split[3])
            current = float(current_split[0]) * (int(die) / 2 + 0.5)

        if len(best_listed) <= 2:
            best = float(best)
        elif len(best_listed) == 3:
            best = float(best_listed[0]) * (int(best_listed[2]) / 2 + 0.5)
        else:
            die = str(best_listed[2]) + str(best_listed[3])
            best = float(best_listed[0]) * (int(die) / 2 + 0.5)

        if current > best:
            return True
        else:
            return False

    def determine_effects(self, plantlist):
        effects = []
        effectstring = ""
        for plant in plantlist:
            if plant["Effects"] != "":
                plant_effects = plant["Effects"].split(", ")
                for effect in plant_effects:
                    if effects.count(effect) == 0:
                        effects.append(effect)
        i = 1
        for effect in effects:
            effectstring += effect
            if i < len(effects):
                effectstring += ", "
            i = i + 1
        self.__dc_calc["Effect Amount"] = len(effects)
        self.__effects.configure(text="Effects, " + str(len(effects)) + " in total: " + effectstring)

    def determine_attributes(self, plantlist):
        attributes = []
        attributestring = ""
        for plant in plantlist:
            if plant["Attributes"] != "":
                for attribute in plant["Attributes"].split(", "):
                    if attributes.count(attribute) == 0:
                        attributes.append(attribute)
        i = 1
        for attribute in attributes:
            attributestring += attribute
            if i < len(attributes):
                attributestring += ", "
            i = i + 1
        self.__dc_calc["Attribute Amount"] = len(attributes)
        self.__attributes.configure(text="Attributes, " + str(len(attributes)) + " in total: " + attributestring)

    def determine_form(self, plantlist):
        forms = []
        unique_forms = []
        final_forms = []
        formstring = ""
        for plant in plantlist:
            for form in plant["Final Form"].split(", "):
                forms.append(form)
        for value in forms:
            if value not in unique_forms:
                unique_forms.append(value)
        for unique_value in unique_forms:
            if forms.count(unique_value) == len(plantlist):
                final_forms.append(unique_value)
        i = 1
        for form in final_forms:
            formstring += form
            if i < len(final_forms):
                formstring += ", "
            i = i + 1
        if len(final_forms) != 0:
            self.__form.configure(text="Suitable Bases: " + formstring)
        else:
            self.__form.configure(text="The chosen plants are not compatible with each other.")

    def calculate_dc(self):
        if self.__dc_calc["Plant Amount"] > 3:
            plant_increase = 3 * (self.__dc_calc["Plant Amount"] - 3)
        else:
            plant_increase = self.__dc_calc["Plant Amount"] * 2

        dc = 6 + plant_increase + self.__dc_calc["Effect Amount"] + self.__dc_calc["Attribute Amount"]
        if self.__dc_calc["Die"] != 0:
            dc += random.randint(1, self.__dc_calc["Die"])
        self.__crafting_dc.configure(text="Crafting DC: " + str(dc))

    def start(self):
        self.__window.mainloop()

    def assign_random_attribute(self):
        random_attribute = random.randint(0, (len(self.__ATTRIBUTES) - 1))
        additional_list = self.__ATTRIBUTES[random_attribute]["Additional"].split(", ")
        additional_string = ""
        if len(additional_list) > 1:
            random_value = random.randint(0, (len(additional_list) - 1))
            additional_string = " (" + str(additional_list[random_value]) + ")"
        self.__random_attribute.configure(text=str(self.__ATTRIBUTES[random_attribute]["Attribute"]) + additional_string)

    def assign_random_effect(self):
        random_effect = random.randint(0, (len(self.__EFFECTS) - 1))
        additional_string = ""
        additional_list = self.__EFFECTS[random_effect]["Additional"].split(", ")
        if len(additional_list) > 1:
            random_value = random.randint(0, (len(additional_list) - 1))
            additional_string = " (" + str(additional_list[random_value]) + ")"
        self.__random_effect.configure(text=str(self.__EFFECTS[random_effect]["Effect"]) + additional_string)

    def assign_random_plant(self):
        chosen_biome = self.__biome_variable.get()
        chosen_rarity = self.__rarity_variable.get()
        plants_in_biome = []
        for plant in self.__PLANTS:
            if (plant["Biomes"].split(", ").count(chosen_biome) > 0
                or plant["Biomes"].split(", ").count("All") > 0 or chosen_biome == "All")\
                    and (plant["Rarity"] == chosen_rarity):
                plants_in_biome.append(plant["Name"])
        randomly_chosen_plant = plants_in_biome[random.randint(0, (len(plants_in_biome) - 1))]
        random_portion = random.choices(PORTIONS, weights=(10, 6, 3, 1), k=1)
        self.__random_plant\
            .configure(text=str(string.capwords(randomly_chosen_plant)) + ", " + str(random_portion) + " Portions")


def main():
    ui = Window()
    ui.start()


main()
