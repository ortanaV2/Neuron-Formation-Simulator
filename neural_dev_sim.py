import json
import tkinter as tk
import random

class NeuronSim:
    #* Simulation settings and thresholds
    tempset = [[(165, 100), "N", "FF0F", 1, 1.0], [(135, 100), "N", "FF1F", 2, 1.0], [(142, 125), "N", "FF2F", 3, 1.0]] #? Simulation Starting Point Structure
    mutation_threshold: int = 6 #? mutation threshold for nucleus formation (default=6) (Lower number --> Higher frequency)
    calculation_speed: int = 250 #Simulation updating-speed (in ms)
    dendrite_formation_speed: int = 4 #Dendrite-tree location choosing tries (default=4)
    dendrite_formation_threshold: float = 0.97 #? Energy loss when dendrites are formatting (default=0.97) (Higher number --> Longer dendrites)
    nucleus_formation_distance: int = 15 #? The minimum distance to another neuron to format a new one
    neuron_network_expansion: bool = True
    branching: bool = False #! (default=False) EXPERIMENTAL
    branching_chance: int = 80    #! (default=80) EXPERIMENTAL
    branching_chaotic_threshold: int = 3 #? Threshold for the entanglement of the branches (default=3) (Lower number --> Less entanglement)
    connection_tightness: int = 4 #? Threshold for the dendrite- and axon-connection tightness (default=4) (Lower number = More tight)

    signal_target: int = 1 #Listening to target origin

    #* Simulation Graphics
    nucleus_color: str = "#333333"
    soma_color: str = "#4a4a4a"
    dendrite_color: str = "#616161"
    axon_color: str = "#4f4f4f"
    terminal_color: str = "#8a8888"

    #* Program logic (do not change)
    first_text = True #program logic (ignore)
    text = None #program logic (ignore)
    tribes_data = {} #program logic (ignore) (structure = {origin:[tribes]}
    tribe_to_origin_library = {} #program logic (ignore) (structure = {tribe:origin} "Which tribe belongs to which origin"
    origin_to_origin_library = {} #program logic (ignore) (structure = {origin:[origin]}
    nucleus_expansion = [] #program logic (ignore)
    interaction_signal_data = [] #interaction logic (ignore)
    time = 0 #interaction logic (ignore)
    signal_pings = 0 #target_interaction logic (ignore)
    signal_freq = 0 #target_interaction logic (ignore)
    signal_e = 0 #target_interaction logic (ignore)

    def __init__(self, root):
        self.root = root
        self.root.title("Neuron Growing Simulator")
        self.root.configure(bg="#0f0f0f")

        self.canvas = tk.Canvas(root, width=900, height=600, borderwidth=0, highlightthickness=0, bg="#0f0f0f")
        self.canvas.pack(expand=True, anchor="center")

        self.cell_width = 3 #Default=2
        self.cell_height = 3 #Default=2

        self.loop_interval = NeuronSim.calculation_speed #loop-time-sleep in milliseconds
        self.start_loop()

    #Draws a pixel on the canvas and raises the title text 
    def manage_cell(self, color: str, neuron_data):
        x, y = neuron_data[0][0], neuron_data[0][1] #Extract coords
        x1 = x * self.cell_width
        y1 = y * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        rect = self.canvas.create_oval(x1, y1, x2, y2, outline=color, fill=color) #Create pixel

        #Update tempset
        try:
            part, tribe, origin, energy = neuron_data[1], neuron_data[2], neuron_data[3], neuron_data[4] #Extract cell-data
            for cell_data in NeuronSim.tempset: 
                if cell_data[0][0] == x and cell_data[0][1] == y: (NeuronSim.tempset).remove(cell_data)
            (NeuronSim.tempset).append([(x, y), part, tribe, origin, energy])
        except Exception: pass

        #Info text (upper left)
        if NeuronSim.first_text:
            NeuronSim.text = self.canvas.create_text(5, 20, anchor="nw", text="N-G-S", font=("Bold Consolas", 12), fill="white")
            NeuronSim.text = self.canvas.create_text(5, 40, anchor="nw", text="210µm - 360µm", font=("Italic Consolas", 9), fill="white")

            NeuronSim.text = self.canvas.create_text(5, 80, anchor="nw", text=f"[N]-Mutation Threshold: {NeuronSim.mutation_threshold}", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(5, 100, anchor="nw", text=f"[N]-Formation Distance: {NeuronSim.nucleus_formation_distance}µm", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(5, 120, anchor="nw", text=f"[D]-EnergyLoss Threshold: {NeuronSim.dendrite_formation_threshold}e", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(5, 140, anchor="nw", text=f"Branching-Mess: {NeuronSim.branching_chaotic_threshold}", font=("Consolas", 9), fill="white")

            NeuronSim.text = self.canvas.create_text(5, 180, anchor="nw", text=f"Step-Interval: {NeuronSim.calculation_speed}ms", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(5, 200, anchor="nw", text=f"Network-Expansion: {NeuronSim.neuron_network_expansion}", font=("Consolas", 9), fill="white")
            NeuronSim.interaction = self.canvas.create_text(450, 580, anchor="center", text=f"Signal-Target({NeuronSim.signal_target}) -> pings:{NeuronSim.signal_pings} -> frequency:{NeuronSim.signal_freq} -> impulse energy:{NeuronSim.signal_e}", font=("Consolas", 9), fill="white")
            NeuronSim.first_text = False
        else:
            self.canvas.delete(NeuronSim.interaction)
            NeuronSim.interaction = self.canvas.create_text(450, 580, anchor="center", text=f"Signal-Target({NeuronSim.signal_target}) -> pings:{NeuronSim.signal_pings} -> frequency:{NeuronSim.signal_freq} -> impulse energy:{round(NeuronSim.signal_e, 4)}", font=("Consolas", 9), fill="white")
            self.canvas.tag_raise(NeuronSim.text, rect) #raise text over pixels

    #Returns the raw neuron_data from neighbors in a specific radius (radius=quadratic with rounded corners)
    def neighbor_in_radius(self, rx: int, ry: int, radius: int):
        neighbor_cell_data = []
        for cell in NeuronSim.tempset:
            x, y = cell[0][0], cell[0][1]
            if (x, y) != (rx, ry):
                if ((rx-radius) <= x <= (rx+radius)) and ((ry-radius) <= y <= (ry+radius)):
                    if (x != ((rx+radius) or (rx-radius))) and (y != ((ry+radius) or (ry-radius))): neighbor_cell_data.append(cell)
        return neighbor_cell_data
    
    def start_loop(self): self.root.after(self.loop_interval, self.loop)
    #Returns a generated tribe-code for dendrite-trees
    def gen_tribe_code(self):
        code_characters = ["F", "H", "A", "C", "Q", 0, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        return f"{random.choice(code_characters)}{random.choice(code_characters)}{random.choice(code_characters)}{random.choice(code_characters)}"
    #Returns the cell_data with the coords that were given
    def get_cell_data(self, x: int, y: int): return [cell_data for cell_data in NeuronSim.tempset if cell_data[0][0] == x and cell_data[0][1] == y][0] #[0] for preventing list in list
    #Returns the coords of the radius (1) around the cell
    def radius_surrounding_coords(self, x: int, y: int): return [(x+i, y+j) for i in range(-1, 2) for j in range(-1, 2) if (x+i, y+j) != (x, y)]
    #Extracts coords from raw neuron_data and only returns a list of coord-tuples
    def extract_coord(self, neuron_data): return [(data[0][0], data[0][1]) for data in neuron_data]
    @staticmethod
    def energy_split(e_amount: float, structures: int): return round(e_amount/structures, 3)

    #Main simulation loop for developing neurons
    def loop(self):
        NeuronSim.time += 1
        for neuron_data in NeuronSim.tempset:
            print() #better visual    
            x, y = neuron_data[0][0], neuron_data[0][1] #Coordinates extracted from tempset
            part, tribe, origin, energy = neuron_data[1], neuron_data[2], neuron_data[3], neuron_data[4] #Neuron_data extracted from tempset
            print(x, y, part, f"[t:{tribe} Origin:{origin}] {energy}e") #Calculation Step Vis
            
            used_coords: list[tuple[int, int]] = self.extract_coord(NeuronSim.tempset) #all used coords
            radius_coords = self.radius_surrounding_coords(x, y) #coords (radius=1)
            free_coords = [coords for coords in radius_coords if coords not in used_coords] #free space coords (radius=1)
            used_radius_coords = [coords for coords in radius_coords if coords in used_coords] #used coords (radius=1)

            print(f"free-coords: {free_coords}")
            print("Terminal-origins: "+str(NeuronSim.tribes_data.keys()))

            #? PROGRAM LOGIC
            if tribe not in NeuronSim.tribe_to_origin_library.keys(): NeuronSim.tribe_to_origin_library[tribe] = origin

            #* Nucleus Formation (color=purple)
            if part == "N":
                #create bigger nucleus if energy is given
                if energy == 1.0:
                    energy_portion = self.energy_split(energy, 9) #Energy split (9) -> 8 Radius around itself + itself
                    self.manage_cell(NeuronSim.nucleus_color, [(x, y), part, tribe, origin, energy_portion]) #Change energy level 
                    for coords in radius_coords: self.manage_cell(NeuronSim.nucleus_color, [coords, part, tribe, origin, energy_portion]) #Create more nucleus cells
                    print("step: nucleus enlargement")
                    continue
                        
                #create soma shell if nucleus is structured
                if free_coords != [] and energy >= 0.1:
                    for coords in free_coords:
                        if random.randint(0, NeuronSim.mutation_threshold) == 0: self.manage_cell(NeuronSim.nucleus_color, [coords, "N", tribe, origin, energy]) #create nucleus instead of soma for mutation
                        else: self.manage_cell(NeuronSim.soma_color, [coords, "S", tribe, origin, 0]) #create soma but with no energy                
                    print("step: creating soma-shell")
                    continue
                
            #* Soma Formation (color=orange)
            if part == "S":
                dendrites_build = any(self.get_cell_data(coords[0], coords[1])[1] == "D" for coords in used_radius_coords) #check if dendrite is already developed (searching for dendrite in range(1))
                if not dendrites_build and free_coords != []: 
                    self.manage_cell(NeuronSim.dendrite_color, [random.choice(free_coords), random.choice(["D", "A"]), self.gen_tribe_code(), origin, 0.2]) #create dendrite if not already developed
                    print("step: creating dendrite-branches")
                    continue
                else: 
                    if origin in NeuronSim.tribes_data.keys() and origin not in NeuronSim.nucleus_expansion: 
                        if len(list(set(NeuronSim.tribes_data[origin]))) >= 3: #checks if terminal_count of origin is 3+. If so replace self with nucleus core
                            self.manage_cell(NeuronSim.nucleus_color, [(x, y), "N", tribe, origin, 1.0])
                            NeuronSim.nucleus_expansion.append(origin)

            #* Axon Formation (color=red)
            if part == "A":
                if energy >= 0.01 and free_coords != []: #Axon is able to grow
                    for _ in range(NeuronSim.dendrite_formation_speed):
                        random_coords_choose = random.choice(free_coords)
                        range_check = self.radius_surrounding_coords(random_coords_choose[0], random_coords_choose[1])
                        multiplier = NeuronSim.dendrite_formation_threshold #threshold setting for energy level decrease when formatting axon
                        #Axon tree growth 
                        if sum(1 for coords in range_check if coords in used_coords) == 1: #checks if amount of structures found in range of random chosen coord is 1
                            if sum(1 for data in self.neighbor_in_radius(random_coords_choose[0], random_coords_choose[1], 3) if data[1] == "A") <= NeuronSim.connection_tightness:
                                if len(self.neighbor_in_radius(random_coords_choose[0], random_coords_choose[1], 2)) <= NeuronSim.branching_chaotic_threshold: #checks structure amount in range of 2. (Prevents chaotic branching)
                                    self.manage_cell(NeuronSim.axon_color, [(x, y), part, tribe, origin, energy * (1-multiplier)]) #changing energy level from origin axon
                                    self.manage_cell(NeuronSim.axon_color, [random_coords_choose, "A", tribe, origin, energy * multiplier]) #enlarge axon tree
                                    break
                        #Axon and Dendrite tribes connecting and creating a terminal
                        else:
                            for coords in range_check:
                                if coords in used_coords:
                                    cell_data = self.get_cell_data(coords[0], coords[1])
                                    if cell_data[2] != tribe and cell_data[3] != origin: #checks if dendrite tribe is in range
                                        usage_range = [coords for coords in self.radius_surrounding_coords(random_coords_choose[0], random_coords_choose[1]) if coords in used_coords]
                                        terminal_range_amount = sum(1 for coords in usage_range if self.get_cell_data(coords[0], coords[1])[1] == "T")
                                        if terminal_range_amount == 0:
                                            self.manage_cell(NeuronSim.axon_color, [(x, y), part, tribe, origin, energy * (1-multiplier)]) #changing energy level from origin axon
                                            self.manage_cell(NeuronSim.terminal_color, [random_coords_choose, "T", tribe, origin, multiplier]) #creating terminal connection
                                            #Add tribes with terminal to origin list (self)
                                            if origin in NeuronSim.tribes_data.keys(): NeuronSim.tribes_data[origin].append(tribe)
                                            else: NeuronSim.tribes_data[origin] = [tribe]
                                            #Add tribes with terminal to origin list (neighbor)
                                            if cell_data[3] in NeuronSim.tribes_data.keys(): NeuronSim.tribes_data[cell_data[3]].append(cell_data[2])
                                            else: NeuronSim.tribes_data[cell_data[3]] = [cell_data[2]]
                                            #Add origin to oto_library
                                            if cell_data[3] not in NeuronSim.origin_to_origin_library.keys(): NeuronSim.origin_to_origin_library[cell_data[3]] = [origin]
                                            else: NeuronSim.origin_to_origin_library[cell_data[3]].append(origin)
                                            if origin not in NeuronSim.origin_to_origin_library.keys(): NeuronSim.origin_to_origin_library[origin] = [cell_data[3]]
                                            else: NeuronSim.origin_to_origin_library[origin].append(cell_data[3])


                #If range is big enough --> create nucleus
                if NeuronSim.neuron_network_expansion:
                    if origin in NeuronSim.tribes_data.keys():
                        if sum(1 for coords in used_radius_coords if self.get_cell_data(coords[0], coords[1])[2] == tribe) == 1: #checks if it's the axon tree-end (axon connection amount)
                            if len(set(tribes for tribes in NeuronSim.tribes_data[origin])) >= 2: #checks if tribe terminal is bigger or equal 2
                                if sum(1 for cell_data in self.neighbor_in_radius(x, y, NeuronSim.nucleus_formation_distance) if cell_data[1] == "N") == 0: #checks if nucleus amount in range of 10 is equal to 0
                                    origin_count = max(cell_data[3] for cell_data in NeuronSim.tempset)+1
                                    self.manage_cell(NeuronSim.nucleus_color, [(x, y), "N", self.gen_tribe_code(), origin_count, 1.0])
                                    print("step: nucleus expansion")
                                    continue

            #* Dendrite Formation (color=yellow)
            if part == "D":
                if energy >= 0.05 and free_coords != []: #dendrite is able to grow
                    for _ in range(NeuronSim.dendrite_formation_speed):
                        random_coords_choose = random.choice(free_coords)
                        range_check = self.radius_surrounding_coords(random_coords_choose[0], random_coords_choose[1])
                        multiplier = NeuronSim.dendrite_formation_threshold #threshold setting for energy level decrease when formatting dendrite
                        #Dendrite tree growth 
                        if sum(1 for coords in range_check if coords in used_coords) == 1: #checks if amount of structures found in range of random chosen coord is 1
                            if sum(1 for data in self.neighbor_in_radius(random_coords_choose[0], random_coords_choose[1], 3) if data[1] == "D") <= NeuronSim.connection_tightness:
                                if len(self.neighbor_in_radius(random_coords_choose[0], random_coords_choose[1], 2)) <= NeuronSim.branching_chaotic_threshold: #checks structure amount in range of 2. (Prevents chaotic branching)
                                    self.manage_cell(NeuronSim.dendrite_color, [(x, y), "D", tribe, origin, energy * (1-multiplier)]) #changing energy level from origin dendrite
                                    self.manage_cell(NeuronSim.dendrite_color, [random_coords_choose, "D", tribe, origin, energy * multiplier]) #enlarge dendrite tree
                                    break                        
                    print("step: dendrite formation")
                    continue

                #Branching setting
                if energy <= 0.7 and random.randint(1, NeuronSim.branching_chance) == 77 and free_coords != [] and NeuronSim.branching:
                    choosed_coords = random.choice(free_coords)
                    surroundings = [coords for coords in self.radius_surrounding_coords(choosed_coords[0], choosed_coords[1]) if coords in used_coords]
                    if sum(1 for coords in surroundings if self.get_cell_data(coords[0], coords[1])[1] == "D") <= 2: #checks if amount of dendrite is less or equal 2
                        self.manage_cell(NeuronSim.dendrite_color, [choosed_coords, "D", tribe, origin, energy/2])
                        print("step: branching dendrite")
                        continue

        #* Neuronal Interaction
        for origin_ in NeuronSim.origin_to_origin_library.keys():
            origin_to_origin_connection = list(set(NeuronSim.origin_to_origin_library[origin_]))
            NeuronSim.interaction_signal_data.append((NeuronSim.time, (origin, origin_to_origin_connection)))
            with open("./interaction_data.json", "w") as file:
                json.dump(NeuronSim.interaction_signal_data, file, indent=2)
            #Processing/Creating Signal Data
            if int(origin_) == NeuronSim.signal_target: 
                NeuronSim.signal_pings = len(origin_to_origin_connection)
                NeuronSim.signal_freq = round(((len(origin_to_origin_connection)*NeuronSim.signal_pings)*(random.uniform(0.9, 1.1))), 4)
                NeuronSim.signal_e = random.uniform(0.5, 1.0)/NeuronSim.signal_pings

        self.start_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuronSim(root)
    root.mainloop()
