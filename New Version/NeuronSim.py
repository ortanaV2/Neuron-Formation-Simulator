import tkinter as tk
import random

class NeuronSim:
    first_text = True
    text = None
    def __init__(self, root):
        self.root = root
        self.root.title("NeuronGrowthSim")

        self.canvas = tk.Canvas(root, width=900, height=600, borderwidth=0, highlightthickness=0, bg="#0f0f0f")
        self.canvas.pack(expand=True, anchor="center")

        self.rows = 500
        self.columns = 800
        self.cell_width = 2
        self.cell_height = 2

        self.loop_interval = 1
        self.start_loop()

    def draw_gridbox(self, x, y, color):
        x1 = x * self.cell_width
        y1 = y * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color)

        # Upper right Text  
        if NeuronSim.first_text:
            text_x = 840
            text_y = 20
            NeuronSim.text = self.canvas.create_text(text_x, text_y, text="Text unterhalb", font=("Bahnschrift", 12), fill="white")
            NeuronSim.first_text = False
        else:
            self.canvas.tag_raise(NeuronSim.text, rect) 

    def start_loop(self):
        self.root.after(self.loop_interval, self.loop)

    def loop(self):
        self.draw_gridbox(random.randint(0, 800), random.randint(0, 500), "blue")
        self.start_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuronSim(root)
    root.mainloop()
