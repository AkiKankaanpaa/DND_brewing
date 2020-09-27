from tkinter import *
import random
import json
import string
import csv

# Used to determine the time units


class Window:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Brewing Apparatus")
        self.__window.configure(bg='PaleVioletRed4')

        # Used in calculation of the final crafting DC
        self.__dc_calc = {"Die": 0, "Plant Amount": 0, "Attribute Amount": 0, "Effect Amount": 0}

        with open("plants.json", "r") as plant_json:
            self.__PLANTS = json.load(plant_json)

        with open("effects.json", "r") as effect_json:
            self.__EFFECTS = json.load(effect_json)

        with open("attributes.json", "r") as attribute_json:
            self.__ATTRIBUTES = json.load(attribute_json)

        with open("timeunits.json", "r") as timeunit_json:
            timeunits = json.load(timeunit_json)

        self.__TIMEUNITS = {}
        for index in timeunits[0]:
            self.__TIMEUNITS[index] = timeunits[0][index]

        self.__biomes = []
        self.__rarities = []
        self.__baseforms = []
        self.__amounts = []
        self.__portions = []

        readable_data = [self.__biomes, self.__rarities, self.__baseforms, self.__amounts, self.__portions]

        row_counter = 0
        with open("basevalues.txt") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                for value in row:
                    readable_data[row_counter].append(value)
                row_counter += 1

        # Information labels for the created potion

        self.__errorlabel = Label(text="", fg="black", bg="PaleVioletRed4")
        self.__errorlabel.grid(row=7, column=0, sticky=N + W + E + S)

        self.__enterlabel = Label(text="Please enter the plants below.", fg="black", bg="PaleVioletRed4")
        self.__enterlabel.grid(row=0, column=0, sticky=N + W + E + S)

        # Used for assigning random plants
        self.__biome_variable = StringVar()
        self.__biome_variable.set(str(self.__biomes[0]))
        self.__biome_option = OptionMenu(self.__window, self.__biome_variable, *self.__biomes)
        self.__biome_option.configure(height=1, bg='PaleVioletRed4', width=24)
        self.__biome_option.grid(row=0, column=1, sticky=N + W + E + S, columnspan=3)

        self.__rarity_variable = StringVar()
        self.__rarity_variable.set(self.__rarities[0])
        self.__rarity_option = OptionMenu(self.__window, self.__rarity_variable, *self.__rarities)
        self.__rarity_option.configure(height=1, bg='PaleVioletRed4', width=24)
        self.__rarity_option.grid(row=0, column=4, sticky=N + W + E + S, columnspan=3)

        # Used for creating random potions
        self.__potion_rarity_variable = StringVar()
        self.__potion_rarity_variable.set(self.__rarities[0])
        self.__potion_rarity_option = OptionMenu(self.__window, self.__potion_rarity_variable, *self.__rarities)
        self.__potion_rarity_option.configure(height=1, bg='PaleVioletRed4')
        self.__potion_rarity_option.grid(row=7, column=1, sticky=N + W + E + S, columnspan=2)

        self.__potion_base_variable = StringVar()
        self.__potion_base_variable.set(self.__baseforms[0])
        self.__potion_base_option = OptionMenu(self.__window, self.__potion_base_variable, *self.__baseforms)
        self.__potion_base_option.configure(height=1, bg='PaleVioletRed4')
        self.__potion_base_option.grid(row=7, column=3, sticky=N + W + E + S, columnspan=2)

        self.__potion_amount_variable = StringVar()
        self.__potion_amount_variable.set(self.__amounts[0])
        self.__potion_amount_option = OptionMenu(self.__window, self.__potion_amount_variable, *self.__amounts)
        self.__potion_amount_option.configure(height=1, bg='PaleVioletRed4')
        self.__potion_amount_option.grid(row=7, column=5, sticky=N + W + E + S, columnspan=2)

        self.__random_plant = Label(text="", fg="black", bg="lavender", height=1)
        self.__randomized_effect_attribute = Label(text="", fg="black", bg="lavender", height=1)

        self.__random_plant.grid(row=2, column=1, columnspan=6, sticky=N + W + E + S)
        self.__randomized_effect_attribute.grid(row=4, column=1, columnspan=6, sticky=N + W + E + S)

        # Choose to either show the desired bases or not

        # Entry-windows for the user to enter the plant names
        self.__entry1 = Entry(self.__window, width=40, fg="black", bg="lavender")
        self.__entry2 = Entry(self.__window, width=40, fg="black", bg="lavender")
        self.__entry3 = Entry(self.__window, width=40, fg="black", bg="lavender")
        self.__entry4 = Entry(self.__window, width=40, fg="black", bg="lavender")
        self.__entry5 = Entry(self.__window, width=40, fg="black", bg="lavender")
        self.__entry6 = Entry(self.__window, width=40, fg="black", bg="lavender")
        
        self.__info_entry = Entry(self.__window, width=40, fg="black", bg="lavender")

        self.__entry1.grid(row=1, column=0)
        self.__entry2.grid(row=2, column=0)
        self.__entry3.grid(row=3, column=0)
        self.__entry4.grid(row=4, column=0)
        self.__entry5.grid(row=5, column=0)
        self.__entry6.grid(row=6, column=0)
        self.__info_entry.grid(row=6, column=1, columnspan=6)

        self.__defined_button = Button(self.__window, text="Create Potion", command=self.press_potion,
                                       height=1, fg="black", bg="slate gray")

        self.__effect_button = Button(self.__window, text="Random Effect", command=self.assign_random_effect,
                                      height=1, fg="black", bg="slate gray")

        self.__attribute_button = Button(self.__window, text="Random Attribute", command=self.assign_random_attribute,
                                         height=1, fg="black", bg="slate gray")

        self.__plant_button = Button(self.__window, text="Random Plant", command=self.assign_random_plant,
                                     height=1, fg="black", bg="slate gray")

        self.__randomized_button = Button(self.__window, text="Random Potion", command=self.create_random_potion,
                                          height=1, fg="black", bg="slate gray")

        self.__info_button = Button(self.__window, text="Retrieve Information", command=self.retrieve_information,
                                    height=1, fg="black", bg="slate gray")

        self.__defined_button.grid(row=8, column=0, columnspan=1, sticky=N + W + E + S)
        self.__effect_button.grid(row=3, column=1, columnspan=3, sticky=N + W + E + S)
        self.__attribute_button.grid(row=3, column=4, columnspan=3, sticky=N + W + E + S)
        self.__plant_button.grid(row=1, column=1, columnspan=6, sticky=N + W + E + S)
        self.__randomized_button.grid(row=8, column=1, columnspan=6, sticky=N + W + E + S)
        self.__info_button.grid(row=5, column=1, columnspan=6, sticky=N + W + E + S)

        # Reads the plants.json file to generate the data structure for the plants
        # does the same with effect and attributes as well

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
                                    fg="black", bg="PaleVioletRed4")
        new_window = Toplevel(self.__window)

        new_window.title("Finished Potion")

        form = Label(new_window, text="", fg="black", bg="lavender", width=70)
        damage = Message(new_window, text="", fg="black", bg="lavender", aspect=1500, justify=CENTER)
        dc = Message(new_window, text="", fg="black", bg="lavender", aspect=1500, justify=CENTER)
        time = Message(new_window, text="", fg="black", bg="lavender", aspect=1500, justify=CENTER)
        effects = Message(new_window, text="", fg="black", bg="lavender", aspect=1500, justify=CENTER)
        attributes = Message(new_window, text="", fg="black", bg="lavender", aspect=1500, justify=CENTER)
        crafting_dc = Message(new_window, text="", fg="black", bg="lavender", aspect=1500, justify=CENTER)

        form.grid(row=0, column=1, sticky=N + W + E + S)
        damage.grid(row=1, column=1, sticky=N + W + E + S)
        dc.grid(row=2, column=1, sticky=N + W + E + S)
        time.grid(row=3, column=1, sticky=N + W + E + S)
        effects.grid(row=4, column=1, sticky=N + W + E + S)
        attributes.grid(row=5, column=1, sticky=N + W + E + S)
        crafting_dc.grid(row=6, column=1, sticky=N + W + E + S)

        calculate_dc(plantlist, dc)
        self.calculate_damage(plantlist, damage)
        self.calculate_time(plantlist, time)
        self.determine_effects(plantlist, effects)
        self.determine_attributes(plantlist, attributes)
        determine_form(plantlist, form)

        self.__dc_calc["Plant Amount"] = plant_amount
        self.calculate_final_dc(crafting_dc)

    def make_potion_error(self):
        self.__errorlabel.configure(text="Unrecognized Ingredients.",
                                    fg="black", bg="firebrick4")

    def create_random_potion(self):
        chosen_plants = []
        allowed_plants = []
        max_rarity = transform_rarity(self.__potion_rarity_variable.get())
        amount_of_plants = int(self.__potion_amount_variable.get())
        chosen_base = self.__potion_base_variable.get()

        for plant in self.__PLANTS:
            if (self.__rarities.index(plant["Rarity"]) <= max_rarity) and (chosen_base in plant["Final Form"]):
                allowed_plants.append(plant)

        current_amount_of_plants = 1

        if len(allowed_plants) < amount_of_plants:
            self.__errorlabel.configure(text="Cannot create potion with parameters.", bg="firebrick4")
        else:
            while current_amount_of_plants <= amount_of_plants:
                random_choice = random.randint(0, (len(allowed_plants) - 1))
                if allowed_plants[random_choice] not in chosen_plants:
                    current_amount_of_plants += 1
                    chosen_plants.append(allowed_plants[random_choice])

            entry_counter = 1
            while entry_counter < 7:
                self.clear_entry(entry_counter)
                if len(chosen_plants) >= entry_counter:
                    self.insert_plant(entry_counter, chosen_plants[entry_counter - 1]["Name"])
                entry_counter += 1

            self.make_potion(chosen_plants, amount_of_plants)

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
        entries[counter].configure(bg="lavender")
        return

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
        entries[counter].configure(bg="lavender")
        return

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
            entries[counter].configure(bg="lavender")
        elif plant_found == 2:
            entries[counter].configure(bg="lavender")
        else:
            entries[counter].configure(bg="firebrick4")
        return

    def calculate_damage(self, plantlist, damage):
        valuedict = {}
        largest_die = 0
        for plant in plantlist:
            damage_listed = list(str(plant["Damage"]))
            # If it is 0
            if len(damage_listed) == 1:
                valuedict[plant["Damage"]] = 0
            elif len(damage_listed) == 3:
                valuedict[plant["Damage"]] = float(damage_listed[0]) * (int(damage_listed[2]) / 2 + 0.5)
                if largest_die < int(damage_listed[2]):
                    largest_die = int(damage_listed[2])
            else:
                die = str(damage_listed[2]) + str(damage_listed[3])
                valuedict[plant["Damage"]] = float(damage_listed[0]) * (int(die) / 2 + 0.5)
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
                if check_die(current[0], current_best[0]):
                    current_best[0] = current[0]
                    current_best[1] = current[1]
        if current_best[1] == "Infinite":
            time.configure(text="Duration: " + current_best[1])
        elif current_best[0] == "0":
            time.configure(text="Duration: None")
        else:
            time.configure(text="Duration: " + current_best[0] + " " + current_best[1])

    def check_unit(self, current, best):
        if self.__TIMEUNITS[current] > self.__TIMEUNITS[best]:
            return 1
        elif int(self.__TIMEUNITS[current]) == int(self.__TIMEUNITS[best]):
            return 2
        else:
            return 3

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
        self.__randomized_effect_attribute.configure(
            text=str(self.__ATTRIBUTES[random_attribute]["Attribute"]) + additional_string)

    def assign_random_effect(self):
        random_effect = random.randint(0, (len(self.__EFFECTS) - 1))
        additional_string = ""
        additional_list = self.__EFFECTS[random_effect]["Additional"].split(", ")
        if len(additional_list) > 1:
            random_value = random.randint(0, (len(additional_list) - 1))
            additional_string = " (" + str(additional_list[random_value]) + ")"
        self.__randomized_effect_attribute.configure(
            text=str(self.__EFFECTS[random_effect]["Effect"]) + additional_string)

    def assign_random_plant(self):
        chosen_biome = self.__biome_variable.get()
        chosen_rarity = self.__rarity_variable.get()
        plants_in_biome = []
        for plant in self.__PLANTS:
            if (plant["Biomes"].split(", ").count(chosen_biome) > 0
                or plant["Biomes"].split(", ").count("All") > 0 or chosen_biome == "All") \
                    and (plant["Rarity"] == chosen_rarity):
                plants_in_biome.append(plant["Name"])
        if len(plants_in_biome) > 0:
            randomly_chosen_plant = plants_in_biome[random.randint(0, (len(plants_in_biome) - 1))]
            random_portion = random.choices(self.__portions, weights=(10, 6, 3, 1), k=1)
            self.__random_plant \
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
            self.__errorlabel.configure(text="No plant found with current parameters.", bg="firebrick4")
        else:
            new_window = Toplevel(self.__window)
            new_window.title(string.capwords(name))

            name = Label(new_window, text=string.capwords(desired_plant["Name"]), bg="lavender", anchor="w",
                         width=12, font=('Helvetica', 18, 'bold'))
            name.grid(row=0, column=0, sticky=N + W + E + S, columnspan=2)

            rarity = Label(new_window, text=desired_plant["Rarity"] + " plant", bg="lavender", anchor="w",
                           width=12, font=('Helvetica', 10, 'italic'))
            rarity.grid(row=1, column=0, sticky=N + W + E + S, columnspan=2)

            i = 0

            formatlist = [["Suitable Bases: ", "Final Form"], ["Save DC: ", "DC"], ["Damage:", "Damage"],
                          ["Time: ", "Time"], ["Unit: ", "Unit"], ["Effects: ", "Effects"],
                          ["Attributes: ", "Attributes"], ["Biomes: ", "Biomes"]]

            while i < 8:
                current_label = Label(new_window, text=formatlist[i][0], bg="lavender", anchor="w", width=12,
                                      font=('Helvetica', 12, 'bold'))
                current_label_info = Label(new_window, text=desired_plant[formatlist[i][1]], bg="lavender",
                                           anchor="w", width=70, font=('Helvetica', 12))
                current_label.grid(row=i+2, column=0, sticky=N + W + E + S)
                current_label_info.grid(row=i+2, column=1, sticky=N + W + E + S)
                i = i + 1


def check_die(current, best):
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


def transform_rarity(rarity):
    rarities = {
        "Common": 1,
        "Uncommon": 2,
        "Rare": 3,
        "Very Rare": 4,
        "Myth": 5,
    }
    return rarities.get(rarity)


def calculate_dc(plantlist, dc):
    if len(plantlist) != 0:
        max_dc = 0
        for plant in plantlist:
            if int(plant["DC"]) > int(max_dc):
                max_dc = int(plant["DC"])
        dc.configure(text="Save DC: " + str(max_dc))


def determine_form(plantlist, form_con):
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


def main():
    ui = Window()
    ui.start()


main()
