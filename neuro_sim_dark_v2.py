import tkinter as tk
import random
import pickle

tribes = 1 #change not recommended
coord_vis = False
tribe_vis = False
cell_size = 4 #zoom (1 recommended for full view)
nucleus_belonging_range = (-9, 10)
max_neuron = 100
max_cells = 10

def kill_cell(coord):
    del grid_data[coord]

def get_used(): #get all used cells
    space = []
    for keys in grid_data.keys():
        space.append(keys)
    return space

def get_neighbours(coord): #get all neighbours of a cell
    x, y = coord
    neighbours = []
    for x_offset in range(-1, 2):
        for y_offset in range(-1, 2):
            if x_offset == 0 and y_offset == 0:
                continue
            neighbours.append((x + x_offset, y + y_offset))
    return neighbours

def get_soma_amount_range2(coord): #5x5 quadrant range
    x, y = coord
    amount = 0
    for x_offset in range(-2, 3):
        for y_offset in range(-2, 3):
            if x_offset == 0 and y_offset == 0:
                continue
            if (x + x_offset, y + y_offset) in grid_data:
                if grid_data[(x + x_offset, y + y_offset)]["state"] == 2:
                    amount += 1
    return amount

def get_dendrite_amount_range2(coord): #5x5 quadrant range
    x, y = coord
    amount = 0
    for x_offset in range(-2, 3):
        for y_offset in range(-2, 3):
            if x_offset == 0 and y_offset == 0:
                continue
            if (x + x_offset, y + y_offset) in grid_data:
                if grid_data[(x + x_offset, y + y_offset)]["state"] == 3:
                    amount += 1
    return amount

def nucleus_radius(coord): #quadrant range (nucleus_belonging_range)
    x, y = coord
    for x_offset in range(nucleus_belonging_range[0], nucleus_belonging_range[1]):
        for y_offset in range(nucleus_belonging_range[0], nucleus_belonging_range[1]):
            if x_offset == 0 and y_offset == 0:
                continue
            if (x + x_offset, y + y_offset) in grid_data:
                if grid_data[(x + x_offset, y + y_offset)]["state"] == 1:
                    return (x + x_offset, y + y_offset)
    return False

def raydev(coord):
    val = random.randint(0, 50)
    if val == 34: kill_cell(coord)

def update_visualization():
    canvas.delete("all")
    for coord, data in grid_data.items():
        x, y = coord
        color = "#ffeb3b" if data["process"] == 1 else color_mapping.get(data["state"], "white") #CYAN
        canvas.create_oval(
            x * cell_size,
            y * cell_size,
            (x + 1) * cell_size,
            (y + 1) * cell_size,
            fill=color,
            outline=""
        )
        if coord_vis:
            canvas.create_text(
                (x + 0.5) * cell_size,
                (y + 0.5) * cell_size,
                text=f"({x}|{y})",
                fill="black"
            )
        if tribe_vis:
            canvas.create_text(
                (x + 0.5) * cell_size,
                (y + 0.5) * cell_size,
                text=f"{data['belonging']}",
                fill="white"
            )
    
    #simulation-calculations
    used = get_used()
    sim_count = 0
    for coord in used:
        sim_count += 1
        global tribes

        data = grid_data[coord]
        neighbours = get_neighbours(coord)

        free_space = []
        for cell in neighbours:
            if cell not in used:
                free_space.append(cell)
        
        len_used = len(used)
        if tribes is not None:
            if tribes == max_neuron: #crash prevention
                with open("neuromodel.pickle", "wb") as file:
                    pickle.dump(grid_data, file)
                print("Max neurons reached")
                break
        if max_cells is not None:
            if len_used == max_cells: #crash prevention
                print("Max cells reached")
                break
        #logging
        print("-"*20)
        print(f"Evolution_Cycle: {sim_count}/{len_used}")
        print("Cells: "+str(len_used))
        print(f"Neurons: {tribes}")

        if data["state"] == 1 and data["type"] == 0: #nucleus (dead)
            for space in neighbours:
                if space in used:
                    if grid_data[space]["state"] != 1:
                        grid_data[space] = {
                            "type": 1,
                            "state": 2,
                            "process": 0,
                            "belonging": data["belonging"]
                        }
                else:
                    grid_data[space] = {
                            "type": 1,
                            "state": 2,
                            "process": 0,
                            "belonging": data["belonging"]
                        }
            data["type"] = 1
        
        if data["state"] == 1 and data["type"] == 1 and data["process"] == 1:
            nucleus_count = 0
            for cell in neighbours:
               if grid_data[cell]["state"] == 1:
                    nucleus_count += 1
            if nucleus_count == 0:
                for cell in neighbours:
                    grid_data[cell] = {
                        "type": 0,
                        "state": 1,
                        "process": 0,
                        "belonging": data["belonging"]
                    }

        if data["state"] == 2 and data["type"] == 1:
            if len(free_space) != 0:
                random_coord = random.choice(neighbours)
                if get_dendrite_amount_range2(random_coord) == 0:
                    nearest_nucleus = nucleus_radius(coord)
                    belonging = grid_data[nearest_nucleus]["belonging"]
                    grid_data[random_coord] = {
                        "type": 1,
                        "state": 3,
                        "process": 0,
                        "belonging":belonging
                    }
            for cell in neighbours:
                if cell in used:
                    if grid_data[cell]["state"] == 3:
                        tribe_read = grid_data[cell]["belonging"]
                        if tribe_read != data["belonging"]:
                            nucleus = nucleus_radius(coord)
                            if nucleus != False:
                                grid_data[nucleus]["process"] = 1
        
        if data["state"] == 3 and data["type"] == 1:
            if nucleus_radius(coord) == False:
                tribes += 1
                grid_data[coord] = {
                    "type": 0, 
                    "state": 1,
                    "process": 0,
                    "belonging": tribes
                }
            else:
                growth_space = []
                for cell in neighbours:
                    if cell in used:
                        if grid_data[cell]["state"] == 3:
                            tribe_read = grid_data[cell]["belonging"]
                            if tribe_read != data["belonging"]:
                                growth_space.append(cell)
                        if grid_data[cell]["state"] == 2:
                            tribe_read = grid_data[cell]["belonging"]
                            if tribe_read != data["belonging"]:
                                growth_space.append(cell)

                for cell in free_space:
                    growth_space.append(cell)

                if len(growth_space) != 0:
                    random_coord = random.choice(growth_space)
                    state3amount = get_dendrite_amount_range2(random_coord)
                    if state3amount > 0 and state3amount < 5:
                        grid_data[random_coord] = {
                            "type": 1,
                            "state": 3,
                            "process": 0,
                            "belonging": data["belonging"]
                        }                
                if len(growth_space) == 0:
                    for cell in neighbours:
                        if cell in used:
                            #if neighbor is dendrite and not same tribe -> process own nucleus
                            if grid_data[cell]["state"] == 3:
                                tribe_read = grid_data[cell]["belonging"]
                                if tribe_read != data["belonging"]:
                                    nucleus = nucleus_radius(coord)
                                    if nucleus != False:
                                        grid_data[nucleus]["process"] = 1
                                    
    root.after(1, update_visualization) #refreshrate

def zoom(event):
    try:
        global cell_size
        if event.delta > 0 and cell_size < 8:
            cell_size += 1
        elif event.delta < 0 and cell_size > 1:
            cell_size -= 1
        update_visualization()
    except Exception:
        pass

#start sequence
grid_data = {
    (50, 50): { #x, y
        "type": 0,
        "state": 1,
        "process": 0,
        "belonging": 1
    }
}

color_mapping = {
    0: "white",
    1: "#4c4f4d", #purple
    2: "#363636", #yellow
    3: "#707070", #yellow-orange
    4: "#808080", #orange
    5: "#ff570f"  #red
}

root = tk.Tk()
root.title("Neuron Growth Simulation")

root.resizable(False, False)
canvas = tk.Canvas(root, width=800, height=800, bg="#0f0f0f")
canvas.pack()

update_visualization()
canvas.bind("<MouseWheel>", zoom)
root.mainloop()
