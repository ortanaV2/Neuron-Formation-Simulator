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
    S = Soma (Cell-Body)
    __________________________
    > tempset structure:

    [(x, y), structure_type, tribe, origin, energy_level, visualized]
    [(int, int),  str,       int,    int,    float,          bool]

    Tribes -> Separates different dendrite branches
    Origin -> Separates different neurons
    Energy_level -> How much energy there is for structure distribution
    __________________________
    """

    tempset = [[(230, 150), "N", 0, 1, 1.0, False], [(230, 151), "D", 0, 1, 1.0, False]] #Simulation Starting Point Structure
    first_text = True #program logic (ignore)
    text = None #program logic (ignore)

    def __init__(self, root):
        self.root = root
        self.root.title("NeuronGrowthSim")
        self.root.configure(bg="#0f0f0f")

        self.canvas = tk.Canvas(root, width=900, height=600, borderwidth=0, highlightthickness=0, bg="#0f0f0f")
        self.canvas.pack(expand=True, anchor="center")

        self.cell_width = 2
        self.cell_height = 2

        self.loop_interval = 500 #loop sleep speed
        self.start_loop()

    #Draws a pixel on the canvas and raises the title text 
    def draw_gridbox(self, x, y, color):
        x1 = x * self.cell_width
        y1 = y * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color) #Create pixel

        # Upper right title text
        if NeuronSim.first_text:
            text_x = 850
            text_y = 20
            NeuronSim.text = self.canvas.create_text(text_x, text_y, text="NGS-v2", font=("Consolas", 12), fill="white")
            NeuronSim.first_text = False
        else:
            self.canvas.tag_raise(NeuronSim.text, rect) #raise text over pixels

    #Returns the raw neuron_data from neighbors in a specific radius (radius=quadratic with rounded corners)
    def neighbor_in_radius(self, rx, ry, radius):
        neighbor_cell_data = []
        for cell in NeuronSim.tempset:
            x, y = cell[0][0], cell[0][1]
            if (x, y) != (rx, ry):
                if ((rx-radius) <= x <= (rx+radius)) and ((ry-radius) <= y <= (ry+radius)):
                    if (x != ((rx+radius) or (rx-radius))) and (y != ((ry+radius) or (ry-radius))):
                        neighbor_cell_data.append(cell)
        return neighbor_cell_data
    
    #Returns the coords of the radius (1) around the cell
    def radius_parimeter_coords(self, x, y): return [(x+i, y+j) for i in range(-1, 2) for j in range(-1, 2)]
    #Extracts coords from raw neuron_data and only returns a list of coord-tuples
    def extract_coord(self, neuron_data): return [(data[0][0], data[0][1]) for data in neuron_data]
    def start_loop(self): self.root.after(self.loop_interval, self.loop)

    #Main simulation loop for developing neurons
    def loop(self):
        print()
        for neuron_data in NeuronSim.tempset:
            x, y = neuron_data[0][0], neuron_data[0][1] #Coordinates extracted from tempset
            part, tribe, origin, energy, is_visualized = neuron_data[1], neuron_data[2], neuron_data[3], neuron_data[4], neuron_data[5] #Neuron_data extracted from tempset
            print(x, y, part, f"[t:{tribe} Origin:{origin}] {energy}e", is_visualized) #Calculation Step Vis
            
            #Nucleus Calculation
            if part == "N": 
                neighbor_data = self.neighbor_in_radius(x, y, 2)
                used_cells = self.extract_coord(neighbor_data)
                print(neighbor_data)
                print(used_cells)

                #! CHECKPOINT            
                #Nucleus building formation using energy
                #energy used to build neuronal structure
                #electric input axons for simulation stability and realism (digital technology based)

        self.start_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuronSim(root)
    root.mainloop()
