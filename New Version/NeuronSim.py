import tkinter as tk
import random

class NeuronSim:
    """
    __________________________
    > Grid Center Position: (230, 150)
    __________________________
    > Structure_types // Parts

    N = Nucleus (Core)
    D = Dendrites (Receiver)
    A = Axon (Sender)
    T = Terminal (ConnectionPoint)
    S = Soma (Cell-Body)
    __________________________
    > tempset structure:

    [(x, y), structure_type, tribe, origin, energy_level]
    [(int, int),  str,       str,    int,      float]

    Tribes -> Separates different dendrite branches
    Origin -> Separates different neurons
    Energy_level -> How much energy there is for structure distribution
    __________________________
    """

    #* Simulation Thresholds
    tempset = [[(115, 75), "N", "FF0F", 1, 1.0], [(90, 75), "N", "FF1F", 2, 1.0], [(90, 45), "N", "FF2F", 3, 1.0]] #Simulation Starting Point Structure
    mutation_threshold = 10 #mutation threshold for nucleus formation (default=10) (Lower number --> Higher frequency)
    calculation_speed = 250 #Simulation updating-speed (in ms)
    dendrite_formation_speed = 2 #Dendrite-tree location choosing tries (default=2)
    dendrite_formation_threshold = 0.97 #Energy loss when dendrites are formatting (default=0.97) (Higher number --> Longer dendrites)

    #* Simulation Graphics
    nucleus_color = "#333333"
    soma_color = "#4a4a4a"
    dendrite_color = "#616161"
    terminal_color = "#878787"

    #* Program logic (do not change)
    first_text = True #program logic (ignore)
    text = None #program logic (ignore)
    tribes_data = {} #program logic (ignore) (structure = {origin:[tribes]}

    def __init__(self, root):
        self.root = root
        self.root.title("Neuron Growing Simulator")
        self.root.configure(bg="#0f0f0f")

        self.canvas = tk.Canvas(root, width=900, height=600, borderwidth=0, highlightthickness=0, bg="#0f0f0f")
        self.canvas.pack(expand=True, anchor="center")

        self.cell_width = 4 #Default=2
        self.cell_height = 4 #Default=2

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

        #Info text (upper right)
        if NeuronSim.first_text:
            text_x = 850
            text_y = 20
            NeuronSim.text = self.canvas.create_text(text_x+14, text_y, text="N-G-S", font=("Bold Consolas", 12), fill="white")
            NeuronSim.text = self.canvas.create_text(text_x-10, text_y+20, text="210µm - 360µm", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(text_x-30, text_y+40, text=f"[N]-M Threshold: {NeuronSim.mutation_threshold}", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(text_x-37, text_y+60, text=f"[D]-e Threshold: {NeuronSim.dendrite_formation_threshold}", font=("Consolas", 9), fill="white")
            NeuronSim.text = self.canvas.create_text(text_x-25, text_y+80, text=f"Step-Interval: {NeuronSim.calculation_speed}", font=("Consolas", 9), fill="white")
            NeuronSim.first_text = False
        else:
            self.canvas.tag_raise(NeuronSim.text, rect) #raise text over pixels

    #Returns the raw neuron_data from neighbors in a specific radius (radius=quadratic with rounded corners)
    def neighbor_in_radius(self, rx: int, ry: int, radius: int):
        neighbor_cell_data = []
        for cell in NeuronSim.tempset:
            x, y = cell[0][0], cell[0][1]
            if (x, y) != (rx, ry):
                if ((rx-radius) <= x <= (rx+radius)) and ((ry-radius) <= y <= (ry+radius)):
                    if (x != ((rx+radius) or (rx-radius))) and (y != ((ry+radius) or (ry-radius))):
                        neighbor_cell_data.append(cell)
        return neighbor_cell_data
    
    def start_loop(self): self.root.after(self.loop_interval, self.loop)
    #Returns a generated tribe-code for dendrite-trees
    def gen_tribe_code(self):
        code_characters = ["F", "H", "A", "C", "Q", 0, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        key1, key2, key3, key4 = random.choice(code_characters), random.choice(code_characters), random.choice(code_characters), random.choice(code_characters)
        return f"{key1}{key2}{key3}{key4}"
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
        print() #better debug visual
        for neuron_data in NeuronSim.tempset:
            # time.sleep(0.02)
            x, y = neuron_data[0][0], neuron_data[0][1] #Coordinates extracted from tempset
            part, tribe, origin, energy = neuron_data[1], neuron_data[2], neuron_data[3], neuron_data[4] #Neuron_data extracted from tempset
            print(x, y, part, f"[t:{tribe} Origin:{origin}] {energy}e") #Calculation Step Vis
            
            used_coords: list[tuple[int, int]] = self.extract_coord(NeuronSim.tempset) #all used coords
            radius_coords = self.radius_surrounding_coords(x, y) #coords (radius=1)
            free_coords = [coords for coords in radius_coords if coords not in used_coords] #free space coords (radius=1)
            used_radius_coords = [coords for coords in radius_coords if coords in used_coords] #used coords (radius=1)

            print(free_coords, used_radius_coords) #debug
            print(NeuronSim.tribes_data) #debug
            print() #debug better visual

            #* Nucleus Formation (color=purple)
            if part == "N":
                #create bigger nucleus if energy is given
                if radius_coords == free_coords and energy == 1.0:
                    energy_portion = self.energy_split(energy, len(free_coords)+1) #Energy split (9) -> 8 Radius around itself + itself
                    self.manage_cell(NeuronSim.nucleus_color, [(x, y), part, tribe, origin, energy_portion]) #Change energy level 
                    for coords in free_coords:
                        self.manage_cell(NeuronSim.nucleus_color, [coords, part, tribe, origin, energy_portion]) #Create more nucleus cells
                    continue
                        
                #create soma shell if nucleus is structured
                if free_coords != [] and energy >= 0.1:
                    for coords in free_coords:
                        if random.randint(0, NeuronSim.mutation_threshold) == 0: self.manage_cell(NeuronSim.nucleus_color, [coords, "N", tribe, origin, energy]) #create nucleus instead of soma for mutation
                        else: self.manage_cell(NeuronSim.soma_color, [coords, "S", tribe, origin, 0]) #create soma but with no energy
                    continue
            
            #* Soma Formation (color=orange)
            if part == "S":
                dendrites_build = any(self.get_cell_data(coords[0], coords[1])[1] == "D" for coords in used_radius_coords) #check if dendrite is already developed (searching for dendrite in range(1))
                if not dendrites_build and free_coords != []: self.manage_cell(NeuronSim.dendrite_color, [random.choice(free_coords), "D", self.gen_tribe_code(), origin, 0.2]) #create dendrite if not already developed
                continue

            #* Dendrite Formation (color=yellow)
            if part == "D":
                if energy >= 0.05 and free_coords != []: #dendrite is able to grow
                    for _ in range(NeuronSim.dendrite_formation_speed):
                        random_coords_choose = random.choice(free_coords)
                        range_check = self.radius_surrounding_coords(random_coords_choose[0], random_coords_choose[1])
                        found_used = sum(1 for coords in range_check if coords in used_coords) #amount of structures found in range of random chosen coord
                        multiplier = NeuronSim.dendrite_formation_threshold #threshold setting for energy level decrease when formatting dendrite
                        #Dendrite tree growth 
                        if found_used == 1: 
                            self.manage_cell(NeuronSim.dendrite_color, [(x, y), "D", tribe, origin, energy * (1-multiplier)]) #changing energy level from origin dendrite
                            self.manage_cell(NeuronSim.dendrite_color, [random_coords_choose, "D", tribe, origin, energy * multiplier]) #enlarge dendrite tree
                            break
                        #Dendrite tribes and origins connecting and creating a terminal
                        else:
                            for coords in range_check:
                                if coords in used_coords:
                                    cell_data = self.get_cell_data(coords[0], coords[1])
                                    if cell_data[2] != tribe and cell_data[3] != origin:
                                        self.manage_cell(NeuronSim.dendrite_color, [(x, y), "D", tribe, origin, energy * (1-multiplier)]) #changing energy level from origin dendrite
                                        self.manage_cell(NeuronSim.terminal_color, [random_coords_choose, "D", tribe, origin, energy * 0]) #creating terminal connection
                                        #Add tribes with terminal to origin list (self)
                                        if origin in NeuronSim.tribes_data.keys(): NeuronSim.tribes_data[origin].append(tribe)
                                        else: NeuronSim.tribes_data[origin] = [tribe]
                                        #Add tribes with terminal to origin list (neighbor)
                                        if cell_data[3] in NeuronSim.tribes_data.keys(): NeuronSim.tribes_data[cell_data[3]].append(cell_data[2])
                                        else: NeuronSim.tribes_data[cell_data[3]] = [cell_data[2]]
                    continue     

        self.start_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuronSim(root)
    root.mainloop()
