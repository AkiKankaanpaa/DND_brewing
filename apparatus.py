from tkinter import *
import random
import json
import string

# Used to determine the time units
TIME_UNITS = {"0": 0, "Rounds": 1, "Minutes": 2, "Hours": 3, "Days": 4, "Months": 5, "Infinite": 6}
BIOMES = ["All", "Arctic", "Coastal", "Deserts", "Forests", "Hills", "Jungles", "Lakes", "Mountain Peaks",
          "Plains", "Ocean", "Swamps", "Volcanic" ]
RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Myth"]
PORTIONS = [1, 2, 3, 4]


class Window:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Brewing Apparatus")

        self.__form = Label(text="", fg="black", bg="powder blue", height=1, width=100)
        self.__damage = Label(text="", fg="black", bg="sky blue", height=1, width=100)
        self.__dc = Label(text="", fg="black", bg="powder blue", height=1, width=100)
        self.__time = Label(text="", fg="black", bg="sky blue", height=1, width=100)
        self.__effects = Label(text="", fg="black", bg="powder blue", height=1, width=100)
        self.__attributes = Label(text="", fg="black", bg="sky blue", height=1, width=100)
        self.__crafting_dc = Label(text="", fg="black", bg="powder blue", height=1, width=100)

        self.__biome_variable = StringVar()
        self.__biome_variable.set(BIOMES[0])
        self.__biome_option = OptionMenu(self.__window, self.__biome_variable, *BIOMES)

        self.__rarity_variable = StringVar()
        self.__rarity_variable.set(RARITIES[0])
        self.__rarity_option = OptionMenu(self.__window, self.__rarity_variable, *RARITIES)

        self.__shameless_self_promotionlabel = Label(text="Brought to you by an underpaid intern",
                                                     fg="black", bg="sky blue", height=1, width=42)

        self.__shameless_self_promotionlabel2 = Label(text="Version 1.3 Alpha (Form Additions)",
                                                     fg="black", bg="powder blue", height=1, width=42)

        self.__shameless_self_promotionlabel3 = Label(text="This is not a finalized version of the product.",
                                                     fg="black", bg="teal", height=1, width=100)

        self.__errorlabel = Label(text="", fg="black", bg="sky blue", height=1, width=100)

        self.__formvalue = IntVar()

        self.__random_attribute = Label(text="", fg="black", bg="sky blue", height=1, width=42)
        self.__random_effect = Label(text="", fg="black", bg="sky blue", height=1, width=42)
        self.__random_plant = Label(text="", fg="black", bg="sky blue", height=1, width=42)

        self.__formcheck = Checkbutton(text="Show Suitable Bases", variable=self.__formvalue, onvalue=1, offvalue=0)\
            .grid(column=2, row=0, sticky=W)

        self.__e1 = Entry(self.__window, width=50, fg="black", bg="light grey")
        self.__e1.grid(row=0, column=0)

        self.__e2 = Entry(self.__window, width=50, fg="black", bg="light grey")
        self.__e2.grid(row=1, column=0)

        self.__e3 = Entry(self.__window, width=50, fg="black", bg="light grey")
        self.__e3.grid(row=2, column=0)

        self.__e4 = Entry(self.__window, width=50, fg="black", bg="light grey")
        self.__e4.grid(row=3, column=0)

        self.__e5 = Entry(self.__window, width=50, fg="black", bg="light grey")
        self.__e5.grid(row=4, column=0)

        self.__e6 = Entry(self.__window, width=50, fg="black", bg="light grey")
        self.__e6.grid(row=5, column=0)

        self.__form.grid(row=0, column=1, sticky=N + W + E + S)
        self.__damage.grid(row=1, column=1, sticky=N + W + E + S)
        self.__dc.grid(row=2, column=1, sticky=N + W + E + S)
        self.__time.grid(row=3, column=1, sticky=N + W + E + S)
        self.__effects.grid(row=4, column=1, sticky=N + W + E + S)
        self.__attributes.grid(row=5, column=1, sticky=N + W + E + S)
        self.__crafting_dc.grid(row=6, column=1, sticky=N + W + E + S)
        self.__errorlabel.grid(row=7, column=1, sticky=N + W + E + S)

        self.__shameless_self_promotionlabel.grid(row=6, column=0, sticky=N + W + E + S)
        self.__shameless_self_promotionlabel2.grid(row=7, column=0, sticky=N + W + E + S)
        self.__shameless_self_promotionlabel3.grid(row=8, column=1, sticky=N + W + E + S)

        self.__random_effect.grid(row=6, column=2, sticky=N + W + E + S)
        self.__random_attribute.grid(row=8, column=2, sticky=N + W + E + S)
        self.__random_plant.grid(row=4, column=2, sticky=N + W + E + S)

        self.__biome_option.grid(row=1, column=2, sticky=N + W + E + S)
        self.__rarity_option.grid(row=2, column=2, sticky=N + W + E + S)

        Button(self.__window, text="Create Potion", command=self.press_potion, height=1, width=42,
               fg="black", bg="teal").grid(row=8, column=0, sticky=N)

        Button(self.__window, text="Random Effect", command=self.assign_random_effect, height=1, width=42,
               fg="black", bg="teal").grid(row=5, column=2, sticky=N)

        Button(self.__window, text="Random Attribute", command=self.assign_random_attribute, height=1, width=42,
               fg="black", bg="teal").grid(row=7, column=2, sticky=N)

        Button(self.__window, text="Random Plant", command=self.assign_random_plant, height=1, width=42,
               fg="black", bg="teal").grid(row=3, column=2, sticky=N)

        # Used in calculation of the final crafting DC
        self.__dc_calc = {"Die": 0, "Plant Amount": 0, "Attribute Amount": 0, "Effect Amount": 0}

        # Reads the plants.json file to generate the data structure for the plants
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

        if self.__e1.get() != "":
            namelist.append(self.__e1.get().lower())
            plant_amount += 1

        if self.__e2.get() != "":
            namelist.append(self.__e2.get().lower())
            plant_amount += 1

        if self.__e3.get() != "":
            namelist.append(self.__e3.get().lower())
            plant_amount += 1

        if self.__e4.get() != "":
            namelist.append(self.__e4.get().lower())
            plant_amount += 1

        if self.__e5.get() != "":
            namelist.append(self.__e5.get().lower())
            plant_amount += 1

        if self.__e6.get() != "":
            namelist.append(self.__e6.get().lower())
            plant_amount += 1

        for name in namelist:
            for plant in self.__PLANTS:
                if plant["Name"] == name:
                    plantlist.append(plant)

        if len(plantlist) == len(namelist):
            self.__errorlabel.configure(text="", fg="black", bg="sky blue")
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

        else:
            self.__damage.configure(text="")
            self.__dc.configure(text="")
            self.__time.configure(text="")
            self.__effects.configure(text="")
            self.__attributes.configure(text="")
            self.__crafting_dc.configure(text="")
            self.__form.configure(text="")
            self.__errorlabel.configure(text="Unrecognized Ingredients or No Plants Entered.", fg="black", bg="red")

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
        additional_string = ""
        additional_list = self.__ATTRIBUTES[random_attribute]["Additional"].split(", ")
        if len(additional_list) > 0:
            random_value = random.randint(0, (len(additional_list) - 1))
            additional_string = " (" + str(additional_list[random_value]) + ")"
        self.__random_attribute.configure(text=str(self.__ATTRIBUTES[random_attribute]["Effect"]) + additional_string)

    def assign_random_effect(self):
        random_effect = random.randint(0, (len(self.__EFFECTS) - 1))
        additional_string = ""
        additional_list = self.__EFFECTS[random_effect]["Additional"].split(", ")
        if len(additional_list) > 0:
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
        self.__random_plant.configure(text=str(string.capwords(randomly_chosen_plant)) + ", " + str(random_portion) + " Portions")


def main():
    ui = Window()
    ui.start()


main()
