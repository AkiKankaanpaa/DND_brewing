from tkinter import *
import random
import json
import string

# Used to determine the time units
TIME_UNITS = {"0": 0, "Rounds": 1, "Minutes": 2, "Hours": 3, "Days": 4, "Weeks": 5, "Months": 6, "Infinite": 7}
BIOMES = ["All", "Arctic", "Coastal", "Deserts", "Forests", "Hills", "Jungles", "Lakes", "Mountain Peaks",
          "Plains", "Ocean", "Swamps", "Volcanic"]
RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Myth"]
AMOUNTS = [2, 3, 4, 5]
PORTIONS = [1, 2, 3, 4]


class Window:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Brewing Apparatus")
        self.__window.configure(bg='dark goldenrod')

        # Used in calculation of the final crafting DC
        self.__dc_calc = {"Die": 0, "Plant Amount": 0, "Attribute Amount": 0, "Effect Amount": 0}

        # Information labels for the created potion

        self.__errorlabel = Message(text="", fg="black", bg="dark goldenrod", aspect=1500, justify=CENTER)

        self.__errorlabel.grid(row=7, column=0, sticky=N + W + E + S)

        # Clickdown-menus for the biome and rarity
        self.__biome_variable = StringVar()
        self.__biome_variable.set(BIOMES[0])
        self.__biome_option = OptionMenu(self.__window, self.__biome_variable, *BIOMES)
        self.__biome_option.configure(height=1, bg='dark goldenrod', width=15)
        self.__biome_option.grid(row=0, column=1, sticky=N + W + E + S, columnspan=1)

        self.__rarity_variable = StringVar()
        self.__rarity_variable.set(RARITIES[0])
        self.__rarity_option = OptionMenu(self.__window, self.__rarity_variable, *RARITIES)
        self.__rarity_option.configure(height=1, bg='dark goldenrod', width=15)
        self.__rarity_option.grid(row=0, column=2, sticky=N + W + E + S, columnspan=1)

        self.__potion_rarity_variable = StringVar()
        self.__potion_rarity_variable.set(RARITIES[0])
        self.__potion_rarity_option = OptionMenu(self.__window, self.__potion_rarity_variable, *RARITIES)
        self.__potion_rarity_option.configure(height=1, bg='dark goldenrod', width=15)
        self.__potion_rarity_option.grid(row=7, column=2, sticky=N + W + E + S, columnspan=1)

        self.__potion_amount_variable = StringVar()
        self.__potion_amount_variable.set(AMOUNTS[0])
        self.__potion_amount_potion = OptionMenu(self.__window, self.__potion_amount_variable, *AMOUNTS)
        self.__potion_amount_potion.configure(height=1, bg='dark goldenrod', width=15)
        self.__potion_amount_potion.grid(row=7, column=1, sticky=N + W + E + S, columnspan=1)

        self.__random_plant = Label(text="", fg="black", bg="dark olive green", height=1, width=21)
        self.__randomized_effect_attribute = Label(text="", fg="black", bg="dark olive green", height=1, width=21)

        self.__random_plant.grid(row=2, column=1, columnspan=2, sticky=N + W + E + S)
        self.__randomized_effect_attribute.grid(row=4, column=1, columnspan=2, sticky=N + W + E + S)

        # Choose to either show the desired bases or not
        self.__formvalue = IntVar()
        self.__formcheck = Checkbutton(text="Show Suitable Bases", bg='dark goldenrod',
                                       variable=self.__formvalue, onvalue=1, offvalue=0)
        self.__formcheck.grid(column=0, row=0, sticky=W)

        # Entry-windows for the user to enter the plant names
        self.__entry1 = Entry(self.__window, width=40, fg="black", bg="lemon chiffon")
        self.__entry2 = Entry(self.__window, width=40, fg="black", bg="lemon chiffon")
        self.__entry3 = Entry(self.__window, width=40, fg="black", bg="lemon chiffon")
        self.__entry4 = Entry(self.__window, width=40, fg="black", bg="lemon chiffon")
        self.__entry5 = Entry(self.__window, width=40, fg="black", bg="lemon chiffon")
        self.__entry6 = Entry(self.__window, width=40, fg="black", bg="lemon chiffon")
        self.__info_entry = Entry(self.__window, width=35, fg="black", bg="lemon chiffon")

        self.__entry1.grid(row=1, column=0)
        self.__entry2.grid(row=2, column=0)
        self.__entry3.grid(row=3, column=0)
        self.__entry4.grid(row=4, column=0)
        self.__entry5.grid(row=5, column=0)
        self.__entry6.grid(row=6, column=0)
        self.__info_entry.grid(row=6, column=1, columnspan=2)

        self.__defined_button = Button(self.__window, text="Create Potion", command=self.press_potion,
                                       height=1, fg="black", bg="chartreuse4")

        self.__effect_button = Button(self.__window, text="Random Effect", command=self.assign_random_effect,
                                      height=1, width=20, fg="black", bg="chartreuse4")

        self.__attribute_button = Button(self.__window, text="Random Attribute", command=self.assign_random_attribute,
                                         height=1, width=20, fg="black", bg="chartreuse4")

        self.__plant_button = Button(self.__window, text="Random Plant", command=self.assign_random_plant,
                                     height=1, width=40, fg="black", bg="chartreuse4")

        self.__randomized_button = Button(self.__window, text="Random Potion", command=self.create_random_potion,
                                          height=1, width=40, fg="black", bg="chartreuse4")

        self.__info_button = Button(self.__window, text="Retrieve Information", command=self.retrieve_information,
                                    height=1, width=40, fg="black", bg="chartreuse4")

        self.__defined_button.grid(row=8, column=0, sticky=N + W + E + S, columnspan=1)
        self.__effect_button.grid(row=3, column=1, columnspan=1, sticky=N + W + E + S)
        self.__attribute_button.grid(row=3, column=2, columnspan=1, sticky=N + W + E + S)
        self.__plant_button.grid(row=1, column=1, columnspan=2, sticky=N + W + E + S)
        self.__randomized_button.grid(row=8, column=1, columnspan=2, sticky=N + W + E + S)
        self.__info_button.grid(row=5, column=1, columnspan=2, sticky=N + W + E + S)

        # Reads the plants.json file to generate the data structure for the plants
        # does the same with effect and attributes as well
        with open("plants.json", "r") as plant_json:
            plants = json.load(plant_json)
        self.__PLANTS = plants

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
        else:
            self.color_entry(1, 2)
        if self.__entry2.get() != "":
            namelist.append(self.__entry2.get().lower())
            plant_amount += 1
        else:
            self.color_entry(2, 2)
        if self.__entry3.get() != "":
            namelist.append(self.__entry3.get().lower())
            plant_amount += 1
        else:
            self.color_entry(3, 2)
        if self.__entry4.get() != "":
            namelist.append(self.__entry4.get().lower())
            plant_amount += 1
        else:
            self.color_entry(4, 2)
        if self.__entry5.get() != "":
            namelist.append(self.__entry5.get().lower())
            plant_amount += 1
        else:
            self.color_entry(5, 2)
        if self.__entry6.get() != "":
            namelist.append(self.__entry6.get().lower())
            plant_amount += 1
        else:
            self.color_entry(6, 2)

        # Checking if the plant-name given exists within the database
        counter = 1
        for name in namelist:
            plant_has_not_been_found = True
            for plant in self.__PLANTS:
                if plant["Name"] == name:
                    plantlist.append(plant)
                    self.color_entry(counter, 1)
                    plant_has_not_been_found = False
                    break
            if plant_has_not_been_found:
                self.color_entry(counter, 3)
            counter += 1

        # Checking if the given plant amount is the same as the verified amount
        if len(plantlist) == len(namelist):
            self.make_potion(plantlist, plant_amount)

        # If it isnt, show an error to the user
        else:
            self.make_potion_error()

    def make_potion(self, plantlist, plant_amount):
        self.__errorlabel.configure(text="",
                                    fg="black", bg="dark goldenrod")
        new_window = Toplevel(self.__window)

        # sets the title of the
        # Toplevel widget
        new_window.title("Finished Potion")

        form = Label(new_window, text="", fg="black", bg="olive drab", width=70)
        damage = Message(new_window, text="", fg="black", bg="dark olive green", aspect=1500, justify=CENTER)
        dc = Message(new_window, text="", fg="black", bg="olive drab", aspect=1500, justify=CENTER)
        time = Message(new_window, text="", fg="black", bg="dark olive green", aspect=1500, justify=CENTER)
        effects = Message(new_window, text="", fg="black", bg="olive drab", aspect=1500, justify=CENTER)
        attributes = Message(new_window, text="", fg="black", bg="dark olive green", aspect=1500, justify=CENTER)
        crafting_dc = Message(new_window, text="", fg="black", bg="olive drab", aspect=1500, justify=CENTER)

        form.grid(row=0, column=1, sticky=N + W + E + S)
        damage.grid(row=1, column=1, sticky=N + W + E + S)
        dc.grid(row=2, column=1, sticky=N + W + E + S)
        time.grid(row=3, column=1, sticky=N + W + E + S)
        effects.grid(row=4, column=1, sticky=N + W + E + S)
        attributes.grid(row=5, column=1, sticky=N + W + E + S)
        crafting_dc.grid(row=6, column=1, sticky=N + W + E + S)

        self.calculate_dc(plantlist, dc)
        self.calculate_damage(plantlist, damage)
        self.calculate_time(plantlist, time)
        self.determine_effects(plantlist, effects)
        self.determine_attributes(plantlist, attributes)

        self.__dc_calc["Plant Amount"] = plant_amount
        self.calculate_final_dc(crafting_dc)

        if self.__formvalue.get() == 1:
            self.determine_form(plantlist, form)
        else:
            form.configure(text="")

    def make_potion_error(self):
        self.__errorlabel.configure(text="Unrecognized Ingredients.",
                                    fg="black", bg="firebrick")

    def create_random_potion(self):
        self.__errorlabel.configure()
        chosen_plants = []
        allowed_plants = []
        max_rarity = self.__potion_rarity_variable.get()
        amount_of_plants = int(self.__potion_amount_variable.get())

        for plant in self.__PLANTS:
            add_to_list = self.check_rarity(plant, max_rarity)
            if add_to_list:
                allowed_plants.append(plant)

        current_amount_of_plants = 1
        while current_amount_of_plants <= amount_of_plants:
            random_choice = random.randint(0, (len(allowed_plants) - 1))
            if allowed_plants[random_choice] not in chosen_plants:
                current_amount_of_plants += 1
                chosen_plants.append(allowed_plants[random_choice])

        counter = 1
        while counter < 7:
            self.clear_entry(counter)
            if len(chosen_plants) >= counter:
                self.insert_plant(counter, chosen_plants[counter-1]["Name"])
            counter += 1

        self.make_potion(chosen_plants, amount_of_plants)

    def check_rarity(self, plant, max_rarity):
        maximum = RARITIES.index(max_rarity)
        if RARITIES.index(plant["Rarity"]) <= maximum:
            return TRUE
        else:
            return FALSE

    def transform_rarity(self, rarity):
        rarities = {
            "Common": 1,
            "Uncommon": 2,
            "Rare": 3,
            "Very Rare": 4,
            "Myth": 5,
        }
        return rarities.get(rarity)

    def insert_plant(self, counter, name):
        entries = {
            1: self.__entry1,
            2: self.__entry2,
            3: self.__entry3,
            4: self.__entry4,
            5: self.__entry5,
            6: self.__entry6,
        }
        entries[counter].insert(END, string.capwords(name))
        entries[counter].configure(bg="yellow green")

    def clear_entry(self, counter):
        entries = {
            1: self.__entry1,
            2: self.__entry2,
            3: self.__entry3,
            4: self.__entry4,
            5: self.__entry5,
            6: self.__entry6,
        }
        entries[counter].delete(0, END)
        entries[counter].configure(bg="lemon chiffon")

    def color_entry(self, counter, plant_found):
        entries = {
            1: self.__entry1,
            2: self.__entry2,
            3: self.__entry3,
            4: self.__entry4,
            5: self.__entry5,
            6: self.__entry6,
        }
        if plant_found == 1:
            entries[counter].configure(bg="green yellow")
        elif plant_found == 2:
            entries[counter].configure(bg="lemon chiffon")
        else:
            entries[counter].configure(bg="firebrick")

    def calculate_dc(self, plantlist, dc):
        if len(plantlist) != 0:
            max_dc = 0
            for plant in plantlist:
                if int(plant["DC"]) > int(max_dc):
                    max_dc = int(plant["DC"])
            dc.configure(text="Save DC: " + str(max_dc))

    def calculate_damage(self, plantlist, damage):
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
            damage.configure(text="Damage: " + value)

    def calculate_time(self, plantlist, time):
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
            time.configure(text="Duration: " + current_best[1])
        elif current_best[0] == "0":
            time.configure(text="Duration: None")
        else:
            time.configure(text="Duration: " + current_best[0] + " " + current_best[1])

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

    def determine_effects(self, plantlist, effect_con):
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
        effect_con.configure(text="Effects, " + str(len(effects)) + " in total: " + effectstring)

    def determine_attributes(self, plantlist, attribute_con):
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
        attribute_con.configure(text="Attributes, " + str(len(attributes)) + " in total: " + attributestring)

    def determine_form(self, plantlist, form_con):
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
            form_con.configure(text="Suitable Bases: " + formstring)
        else:
            form_con.configure(text="The chosen plants are not compatible with each other.")

    def calculate_final_dc(self, dc_con):
        if self.__dc_calc["Plant Amount"] > 3:
            plant_increase = 3 * (self.__dc_calc["Plant Amount"] - 3)
        else:
            plant_increase = self.__dc_calc["Plant Amount"] * 2

        dc = 6 + plant_increase + self.__dc_calc["Effect Amount"] + self.__dc_calc["Attribute Amount"]
        if self.__dc_calc["Die"] != 0:
            dc += random.randint(1, self.__dc_calc["Die"])
        dc_con.configure(text="Crafting DC: " + str(dc))

    def start(self):
        self.__window.mainloop()

    def assign_random_attribute(self):
        random_attribute = random.randint(0, (len(self.__ATTRIBUTES) - 1))
        additional_list = self.__ATTRIBUTES[random_attribute]["Additional"].split(", ")
        additional_string = ""
        if len(additional_list) > 1:
            random_value = random.randint(0, (len(additional_list) - 1))
            additional_string = " (" + str(additional_list[random_value]) + ")"
        self.__randomized_effect_attribute.configure(text=str(self.__ATTRIBUTES[random_attribute]["Attribute"])
                                                          + additional_string)

    def assign_random_effect(self):
        random_effect = random.randint(0, (len(self.__EFFECTS) - 1))
        additional_string = ""
        additional_list = self.__EFFECTS[random_effect]["Additional"].split(", ")
        if len(additional_list) > 1:
            random_value = random.randint(0, (len(additional_list) - 1))
            additional_string = " (" + str(additional_list[random_value]) + ")"
        self.__randomized_effect_attribute.configure(text=str(self.__EFFECTS[random_effect]["Effect"])
                                                          + additional_string)

    def assign_random_plant(self):
        chosen_biome = self.__biome_variable.get()
        chosen_rarity = self.__rarity_variable.get()
        plants_in_biome = []
        for plant in self.__PLANTS:
            if (plant["Biomes"].split(", ").count(chosen_biome) > 0
                or plant["Biomes"].split(", ").count("All") > 0 or chosen_biome == "All")\
                    and (plant["Rarity"] == chosen_rarity):
                plants_in_biome.append(plant["Name"])
        if len(plants_in_biome) > 0:
            randomly_chosen_plant = plants_in_biome[random.randint(0, (len(plants_in_biome) - 1))]
            random_portion = random.choices(PORTIONS, weights=(10, 6, 3, 1), k=1)
            self.__random_plant\
                .configure(text=str(string.capwords(randomly_chosen_plant)) + ", " + str(random_portion) + " Portions")
        else:
            self.__random_plant.configure(text="No plant found with current parameters.")

    def retrieve_information(self):
        desired_plant = None
        name = self.__info_entry.get()
        for plant in self.__PLANTS:
            if plant["Name"] == name:
                desired_plant = plant
                break
        if desired_plant is None:
            self.__errorlabel.configure(text="No plant found with current parameters.", bg="firebrick")
        else:
            new_window = Toplevel(self.__window)
            new_window.title(string.capwords(name))
            name = Label(new_window, text=string.capwords(desired_plant["Name"]), anchor="w", width=12,
                         font=('Helvetica', 18, 'bold'))
            name.grid(row=0, column=0, sticky=N + W + E + S, columnspan=2)

            rarity = Label(new_window, text=desired_plant["Rarity"] + " plant", anchor="w", width=12,
                         font=('Helvetica', 12, 'italic'))
            rarity.grid(row=1, column=0, sticky=N + W + E + S, columnspan=2)

            final_forms = Label(new_window, text="Suitable Bases: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            final_forms_info = Label(new_window, text=desired_plant["Final Form"], anchor="w", width=70,
                                font=('Helvetica', 12))
            final_forms.grid(row=2, column=0, sticky=N + W + E + S)
            final_forms_info.grid(row=2, column=1, sticky=N + W + E + S)

            dc = Label(new_window, text="Save DC: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            dc_info = Label(new_window, text=desired_plant["DC"], anchor="w", width=70,
                                font=('Helvetica', 12))
            dc.grid(row=3, column=0, sticky=N + W + E + S)
            dc_info.grid(row=3, column=1, sticky=N + W + E + S)

            damage = Label(new_window, text="Damage: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            damage_info = Label(new_window, text=desired_plant["Damage"], anchor="w", width=70,
                                font=('Helvetica', 12))
            damage.grid(row=4, column=0, sticky=N + W + E + S)
            damage_info.grid(row=4, column=1, sticky=N + W + E + S)

            time = Label(new_window, text="Time: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            time_info = Label(new_window, text=desired_plant["Time"], anchor="w", width=70,
                                font=('Helvetica', 12))
            time.grid(row=6, column=0, sticky=N + W + E + S)
            time_info.grid(row=6, column=1, sticky=N + W + E + S)

            unit = Label(new_window, text="Unit: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            unit_info = Label(new_window, text=desired_plant["Unit"], anchor="w", width=70,
                                font=('Helvetica', 12))
            unit.grid(row=7, column=0, sticky=N + W + E + S)
            unit_info.grid(row=7, column=1, sticky=N + W + E + S)

            effects = Label(new_window, text="Effects: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            effects_info = Label(new_window, text=desired_plant["Effects"], anchor="w", width=70,
                                font=('Helvetica', 12))
            effects.grid(row=8, column=0, sticky=N + W + E + S)
            effects_info.grid(row=8, column=1, sticky=N + W + E + S)


            attributes = Label(new_window, text="Attributes: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            attributes_info = Label(new_window, text=desired_plant["Attributes"], anchor="w", width=70,
                                font=('Helvetica', 12))
            attributes.grid(row=9, column=0, sticky=N + W + E + S)
            attributes_info.grid(row=9, column=1, sticky=N + W + E + S)

            biomes = Label(new_window, text="Biomes: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            biomes_info = Label(new_window, text=desired_plant["Biomes"], anchor="w", width=70,
                                font=('Helvetica', 12))
            biomes.grid(row=9, column=0, sticky=N + W + E + S)
            biomes_info.grid(row=9, column=1, sticky=N + W + E + S)

            # FINISH ADDING DESCRIPTIONS TO plants.json AND THE IMPLEMENT
            description = Label(new_window, text="Description: ", anchor="w", width=12,
                         font=('Helvetica', 12, 'bold'))
            description_info = Label(new_window, text="Placeholder", anchor="w", width=70,
                                font=('Helvetica', 12))
            description.grid(row=10, column=0, sticky=N + W + E + S)
            description_info.grid(row=10, column=1, sticky=N + W + E + S)


def main():
    ui = Window()
    ui.start()


main()
